import os
import uuid
import queue
import threading
import traceback
import logging
from flask import Flask, render_template, request, jsonify
import yt_dlp
import whisper

app = Flask(__name__)

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

INPUT_DIR = "data/input"
OUTPUT_DIR = "data/output"
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ----------------------------------------------------
# 🌟 ARCHITECTURE: Background Job Queue System
# ----------------------------------------------------
jobs = {}
job_queue = queue.Queue()

current_model_name = None
current_model = None

def get_whisper_model(model_name):
    """Loads the model intelligently (caches across requests)"""
    global current_model_name, current_model
    if current_model_name != model_name or current_model is None:
        logging.info(f"Loading Whisper model: {model_name}... (this might take a second)")
        # fp16=False is VERY important for CPU performance optimization
        current_model = whisper.load_model(model_name)
        current_model_name = model_name
    return current_model

def format_timestamp(seconds: float):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def generate_srt(segments):
    """Generates standard .srt subtitle format from Whisper segments"""
    srt_content = ""
    for i, segment in enumerate(segments, start=1):
        start = format_timestamp(segment['start'])
        end = format_timestamp(segment['end'])
        text = segment['text'].strip()
        srt_content += f"{i}\n{start} --> {end}\n{text}\n\n"
    return srt_content

def process_job(job_id):
    """The brain of the operation. Runs in a dedicated background thread."""
    job = jobs[job_id]
    try:
        job['status'] = 'processing'
        model_name = job['model']
        input_type = job['type']
        
        input_path = job['input_path']
        
        if input_type == 'youtube':
            logging.info(f"[{job_id}] Downloading YouTube video: {job['url']}")
            job['message'] = 'Downloading audio from YouTube...'
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': input_path,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([job['url']])
            # the file extension is now technically .mp3 because of postprocessors!
            input_path = input_path.replace('.%(ext)s', '.mp3')
            
        logging.info(f"[{job_id}] Transcribing with model {model_name}...")
        job['message'] = f'Transcribing audio (Model: {model_name})...'
        model = get_whisper_model(model_name)
        
        # CPU optimization: fp16=False
        result = model.transcribe(input_path, fp16=False)
        text = result["text"].strip()
        srt_text = generate_srt(result["segments"])
        
        # Output saving
        txt_path = os.path.join(OUTPUT_DIR, f"{job_id}.txt")
        srt_path = os.path.join(OUTPUT_DIR, f"{job_id}.srt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(srt_text)
            
        job['text'] = text
        job['srt'] = srt_text
        job['status'] = 'completed'
        job['message'] = 'Done!'
        logging.info(f"[{job_id}] Job completed successfully.")
        
    except Exception as e:
        logging.error(f"[{job_id}] Error: {traceback.format_exc()}")
        job['status'] = 'failed'
        job['error'] = str(e)
    finally:
        # Cleanup input file to save space inside Docker!
        if 'input_path' in locals() and os.path.exists(input_path):
            try:
                os.remove(input_path)
            except:
                pass

def worker_thread():
    """Forever loop that processes queue sequentially to prevent CPU overload"""
    while True:
        job_id = job_queue.get()
        if job_id is None: break
        process_job(job_id)
        job_queue.task_done()

# Start background worker
threading.Thread(target=worker_thread, daemon=True).start()

# ----------------------------------------------------
# 🌐 ROUTES
# ----------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/transcribe/upload", methods=["POST"])
def transcribe_upload():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    model_name = request.form.get("model", "base")
    
    file_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1]
    input_path = os.path.join(INPUT_DIR, f"{file_id}{ext}")
    file.save(input_path)
    
    jobs[file_id] = {
        'id': file_id,
        'type': 'upload',
        'status': 'queued',
        'input_path': input_path,
        'model': model_name,
        'message': 'Queued in background...'
    }
    job_queue.put(file_id)
    logging.info(f"Queued upload job {file_id}")
    return jsonify({"job_id": file_id})

@app.route("/transcribe/youtube", methods=["POST"])
def transcribe_youtube():
    data = request.json
    url = data.get("url")
    model_name = data.get("model", "base")
    
    if not url:
        return jsonify({"error": "No URL provided"}), 400
        
    file_id = str(uuid.uuid4())
    input_path = os.path.join(INPUT_DIR, f"{file_id}.%(ext)s")
    
    jobs[file_id] = {
        'id': file_id,
        'type': 'youtube',
        'status': 'queued',
        'url': url,
        'input_path': input_path,
        'model': model_name,
        'message': 'Queued in background...'
    }
    job_queue.put(file_id)
    logging.info(f"Queued YouTube job {file_id}")
    return jsonify({"job_id": file_id})

@app.route("/status/<job_id>", methods=["GET"])
def get_status(job_id):
    if job_id not in jobs:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(jobs[job_id])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

import os
import uuid
import whisper
from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)
# Assuming we run from whisper-video-transcriber root
INPUT_DIR = "data/input"
OUTPUT_DIR = "data/output"
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load model globally (loads on startup)
print("Loading Whisper model (base)... please wait.")
model = whisper.load_model("base")

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
    
    # Save file
    file_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1]
    input_path = os.path.join(INPUT_DIR, f"{file_id}{ext}")
    file.save(input_path)
    
    try:
        # Transcribe
        result = model.transcribe(input_path)
        text = result["text"].strip()
        
        # Save output
        output_path = os.path.join(OUTPUT_DIR, f"{file_id}.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
            
        return jsonify({"success": True, "text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/transcribe/youtube", methods=["POST"])
def transcribe_youtube():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400
        
    file_id = str(uuid.uuid4())
    input_path = os.path.join(INPUT_DIR, f"{file_id}.%(ext)s")
    
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
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        # The actual file will be an mp3 as specified in postprocessors
        actual_input_path = os.path.join(INPUT_DIR, f"{file_id}.mp3")
        
        # Transcribe
        result = model.transcribe(actual_input_path)
        text = result["text"].strip()
        
        # Save output
        output_path = os.path.join(OUTPUT_DIR, f"{file_id}.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
            
        return jsonify({"success": True, "text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

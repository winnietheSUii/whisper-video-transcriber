# Whisper Video Transcriber (Web UI)

A dynamic web application to extract text (subtitles/transcripts) from video files or YouTube links locally using OpenAI's [Whisper](https://github.com/openai/whisper) model.

**100% Free**. Powered by Local AI.

## Features
- **Upload Local Files**: Drag and drop any video or audio file.
- **Transcribe YouTube videos**: Paste a YouTube URL and we'll download the audio via `yt-dlp` and transcribe it.
- **Premium Interface**: A modern, sleek dark-mode glassmorphism UI.

## Prerequisites
1. **Python 3.8+**
2. **FFmpeg**: Whisper and `yt-dlp` require FFmpeg. 
   - **Windows**: Install via `winget install ffmpeg` 

## Installation

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Open your browser and navigate to `http://127.0.0.1:5000`
3. Upload a file or paste a YouTube URL and click Transcribe!

## Project Structure
- `app.py`: Flask web server with YouTube downloading and Whisper transcription.
- `templates/`: HTML markup for the interface.
- `static/`: CSS for the dynamic UI.
- `transcribe.py`: (Optional) CLI helper script to transcribe a folder of files.
- `requirements.txt`: Python dependencies.

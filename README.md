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

## Installation & Usage (Docker - Recommended!)⚡

Using Docker completely eliminates the need to install FFmpeg or manage Python virtual environments.

1. Ensure [Docker](https://www.docker.com/) is installed.
2. In your terminal, run:
   ```bash
   docker-compose up -d --build
   ```
3. Open your browser and navigate to `http://localhost:5000`

*That's it!* 

> Note: The first time you transcribe a file, the AI model will download to a persistent Docker volume, so subsequent uses will occur instantly.
3. Upload a file or paste a YouTube URL and click Transcribe!

## Project Structure
- `app.py`: Flask web server with YouTube downloading and Whisper transcription.
- `templates/`: HTML markup for the interface.
- `static/`: CSS for the dynamic UI.
- `transcribe.py`: (Optional) CLI helper script to transcribe a folder of files.
- `requirements.txt`: Python dependencies.

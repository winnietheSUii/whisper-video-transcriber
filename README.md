# Whisper Video Transcriber

A simple Python project to extract text (subtitles/transcripts) from video files locally using OpenAI's [Whisper](https://github.com/openai/whisper) model. 

Since this runs the open-source Whisper models on your local machine, it is **100% free**.

## Prerequisites
1. **Python 3.8+**
2. **FFmpeg**: Whisper requires FFmpeg to process audio and video files. 
   - **Windows**: Install via `winget install ffmpeg` or download it from the official site and add it to your PATH.
   - **Mac**: `brew install ffmpeg`
   - **Linux**: `sudo apt update && sudo apt install ffmpeg`

## Installation

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Place your video files (e.g., `.mp4`, `.mkv`) inside the `data/input/` folder.
2. Run the transcription script:
   ```bash
   python transcribe.py
   ```
3. The transcribed text will be saved in the `data/output/` folder with the same name as the video file (as a `.txt` file).

## Project Structure
- `transcribe.py`: The main script that runs the Whisper model.
- `requirements.txt`: Python package dependencies.
- `data/input/`: Directory for input videos (ignored by Git).
- `data/output/`: Directory for output text (ignored by Git).

# Use official Python image based on Debian
FROM python:3.10-slim

# Install FFmpeg (Required for Whisper and yt-dlp)
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /app

# Copy python dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 5000 for the web server
EXPOSE 5000

# Start the Flask app
CMD ["python", "app.py"]

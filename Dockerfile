FROM python:3.10-slim

# Install system dependencies (ffmpeg and curl for healthcheck)
RUN apt-get update && \
    apt-get install -y ffmpeg libgl1 curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]

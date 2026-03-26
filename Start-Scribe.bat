@echo off
title Scribe AI Transcriber
color 0B

echo ========================================================
echo    🚀 Scribe AI Video Transcriber
echo    Starting the engine... please wait a moment.
echo ========================================================
echo.

:: Check for virtual environment and create if missing
IF NOT EXIST "venv\Scripts\activate.bat" (
    echo [1/3] Setting up Python environment for the first time...
    python -m venv venv
)

echo [2/3] Activating Python environment...
call venv\Scripts\activate.bat

echo [3/3] Ensuring required packages are installed...
pip install -r requirements.txt --quiet

echo.
echo ✅ Server is starting!
echo 🌐 Your web browser will open automatically in just a moment...
echo.
echo ========================================================
echo DO NOT CLOSE THIS BLACK WINDOW WHILE USING THE APP
echo To stop the app, press Ctrl+C in this window.
echo ========================================================

:: Wait for 3 seconds to let Python server spin up, then open browser
timeout /t 3 /nobreak > NUL
start "" http://127.0.0.1:5000

:: Start the Flask app
python app.py

pause

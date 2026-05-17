@echo off
REM Complaint Priority Management System - Windows Setup Script
REM Run this script to set up the backend automatically

echo.
echo ============================================================
echo  Complaint Priority Management System - Backend Setup
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/6] Python detected: 
python --version
echo.

REM Create virtual environment
echo [2/6] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created successfully
) else (
    echo Virtual environment already exists
)
echo.

REM Activate virtual environment and install dependencies
echo [3/6] Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt
echo.

REM Check if .env exists
echo [4/6] Checking environment configuration...
if not exist ".env" (
    echo .env file not found. Creating from template...
    copy .env.example .env
    echo.
    echo ============================================================
    echo  IMPORTANT: Please edit .env file with your credentials
    echo ============================================================
    echo.
    echo You need to configure:
    echo   - EMAIL_ADDRESS: Your Gmail address
    echo   - EMAIL_PASSWORD: Your Gmail App Password
    echo   - DB_PASSWORD: Your MySQL password
    echo.
    echo Press any key to open .env file in notepad...
    pause >nul
    notepad .env
) else (
    echo .env file already exists
)
echo.

REM Database initialization prompt
echo [5/6] Database initialization...
echo.
set /p INIT_DB="Do you want to initialize the database now? (y/n): "
if /i "%INIT_DB%"=="y" (
    python init_db.py
) else (
    echo Skipping database initialization
    echo You can run it later with: python init_db.py
)
echo.

REM Final instructions
echo [6/6] Setup complete!
echo.
echo ============================================================
echo  Next Steps:
echo ============================================================
echo.
echo 1. Make sure MySQL is running
echo 2. Verify .env file has correct credentials
echo 3. If not done, run: python init_db.py
echo 4. Start the server with: python app.py
echo.
echo For frontend setup, see SETUP_GUIDE.md
echo.
echo ============================================================
echo.

set /p START_NOW="Do you want to start the backend server now? (y/n): "
if /i "%START_NOW%"=="y" (
    echo.
    echo Starting backend server...
    echo Press Ctrl+C to stop the server
    echo.
    python app.py
) else (
    echo.
    echo To start the server later, run: python app.py
    echo.
)

pause

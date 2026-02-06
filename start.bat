@echo off
REM Causal Chat Analysis Dashboard - Windows Startup Script

echo.
echo ============================================================
echo  Causal Chat Analysis Dashboard
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org
    pause
    exit /b 1
)

echo [1/4] Checking dependencies...
python -c "import flask; print('  OK: Flask')" >nul 2>&1
if errorlevel 1 (
    echo [!] Flask not found, installing dependencies...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    echo  OK: Flask
)

python -c "import flask_cors; print('  OK: Flask-CORS')" >nul 2>&1
if errorlevel 1 (
    echo [!] Flask-CORS not found, installing...
    pip install flask-cors
)

echo.
echo [2/4] All dependencies installed
echo.

echo [3/4] Starting Flask API server...
echo   http://localhost:5000
echo.

REM Start Flask API and dashboard
python api.py

if errorlevel 1 (
    echo.
    echo Error: Failed to start server
    pause
    exit /b 1
)

pause

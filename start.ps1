# Causal Chat Analysis Dashboard - PowerShell Startup Script

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Causal Chat Analysis Dashboard" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[✓] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[✗] Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "    Please install from https://www.python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[1/3] Checking dependencies..." -ForegroundColor Yellow

# Check Flask
try {
    python -c "import flask" 2>&1 | Out-Null
    Write-Host "  [✓] Flask" -ForegroundColor Green
} catch {
    Write-Host "  [✗] Flask not found" -ForegroundColor Red
    Write-Host ""
    Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to install dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Check Flask-CORS
try {
    python -c "import flask_cors" 2>&1 | Out-Null
    Write-Host "  [✓] Flask-CORS" -ForegroundColor Green
} catch {
    Write-Host "  [✗] Flask-CORS not found, installing..." -ForegroundColor Yellow
    pip install flask-cors
}

Write-Host ""
Write-Host "[2/3] All dependencies installed" -ForegroundColor Green
Write-Host ""

Write-Host "[3/3] Starting Flask API server..." -ForegroundColor Yellow
Write-Host "   http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start Flask API
python api.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Error: Failed to start server" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

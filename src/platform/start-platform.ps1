# Start Deployment Metrics Platform
# This script starts the backend server

Write-Host "Starting Deployment Metrics Platform..." -ForegroundColor Green

# Navigate to backend directory
$BackendDir = Join-Path $PSScriptRoot "backend"
Set-Location $BackendDir

# Check if venv exists
if (-not (Test-Path "venv")) {
    Write-Host "Virtual environment not found. Creating..." -ForegroundColor Yellow
    python -m venv venv
    
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
}

# Activate venv
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
.\venv\Scripts\Activate.ps1

# Process any queued metrics
Write-Host "Processing queued metrics..." -ForegroundColor Cyan
python -c "from metrics_queue import process_queued_deployments; from app import app; process_queued_deployments()"

# Start server
Write-Host "`nBackend API starting on http://localhost:5001" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop`n" -ForegroundColor Yellow

python app.py
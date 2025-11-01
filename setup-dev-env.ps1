# ETEx - Development Environment Setup Script (Windows PowerShell)
# Run this script to set up your development environment

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ETEx Development Environment Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "[1/8] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.12+ from https://www.python.org" -ForegroundColor Red
    exit 1
}

# Check Node.js installation
Write-Host "`n[2/8] Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not found in PATH" -ForegroundColor Red
    Write-Host "Please install Node.js 20+ LTS from https://nodejs.org" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "`n[3/8] Creating Python virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "`n[4/8] Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Install Python dependencies
Write-Host "`n[5/8] Installing Python dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip
pip install -r requirements.txt
Write-Host "✓ Python dependencies installed" -ForegroundColor Green

# Create .env file if it doesn't exist
Write-Host "`n[6/8] Setting up environment variables..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
} else {
    Copy-Item ".env.example" ".env"
    Write-Host "✓ .env file created from template" -ForegroundColor Green
    Write-Host "⚠  Please edit .env and add your API keys" -ForegroundColor Yellow
}

# Install spaCy language models
Write-Host "`n[7/8] Installing spaCy language models..." -ForegroundColor Yellow
Write-Host "Installing German model..."
python -m spacy download de_core_news_sm
Write-Host "Installing English model..."
python -m spacy download en_core_web_sm
Write-Host "✓ spaCy models installed" -ForegroundColor Green

# Create data directories
Write-Host "`n[8/8] Creating data directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "data\database" | Out-Null
New-Item -ItemType Directory -Force -Path "data\uploads" | Out-Null
New-Item -ItemType Directory -Force -Path "data\cache" | Out-Null
New-Item -ItemType Directory -Force -Path "logs" | Out-Null
Write-Host "✓ Data directories created" -ForegroundColor Green

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Setup Complete! 🎉" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Edit .env file with your API keys" -ForegroundColor White
Write-Host "2. Install frontend dependencies: cd src\frontend && npm install" -ForegroundColor White
Write-Host "3. Initialize database: cd src\backend && alembic upgrade head" -ForegroundColor White
Write-Host "4. Start backend: cd src\backend && uvicorn main:app --reload" -ForegroundColor White
Write-Host "5. Start frontend: cd src\frontend && npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "Documentation: See README.md" -ForegroundColor Cyan
Write-Host ""

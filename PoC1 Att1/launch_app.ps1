# Fabricator.ai MVP - Launch Script
# This script activates the virtual environment and launches the Streamlit app

Write-Host "🔧 Fabricator.ai MVP - Launch Script" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "app.py")) {
    Write-Host "❌ Error: app.py not found in current directory" -ForegroundColor Red
    Write-Host "Please run this script from the 'PoC1 Attempt1' folder" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if virtual environment exists
$venvPath = "..\fabenv\Scripts\Activate.ps1"
$pythonPath = "..\fabenv\Scripts\python.exe"
if (-not (Test-Path $venvPath)) {
    Write-Host "❌ Error: Virtual environment not found at $venvPath" -ForegroundColor Red
    Write-Host "Please ensure the fabenv folder exists in the parent directory" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

if (-not (Test-Path $pythonPath)) {
    Write-Host "❌ Error: Python not found in virtual environment at $pythonPath" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Found virtual environment" -ForegroundColor Green
Write-Host ""

# Activate virtual environment
Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
try {
    & $venvPath
    Write-Host "✅ Virtual environment activated" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to activate virtual environment: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if required modules are available
Write-Host "🔍 Checking required modules..." -ForegroundColor Yellow
try {
    & $pythonPath -c "import ezdxf" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ ezdxf module available" -ForegroundColor Green
    } else {
        throw "Module not found"
    }
} catch {
    Write-Host "❌ ezdxf module not available. Installing dependencies..." -ForegroundColor Yellow
    & $pythonPath -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "🚀 Launching Fabricator.ai MVP..." -ForegroundColor Green
Write-Host "The application will open in your browser at: http://localhost:8501" -ForegroundColor Cyan
Write-Host "To stop the application, press Ctrl+C in this window" -ForegroundColor Yellow
Write-Host ""

# Launch Streamlit using the virtual environment's Python
Write-Host "🔧 Using virtual environment Python for Streamlit..." -ForegroundColor Yellow
try {
    & $pythonPath -m streamlit run app.py
} catch {
    Write-Host "❌ Failed to launch Streamlit: $_" -ForegroundColor Red
    Write-Host "Please ensure Streamlit is installed: $pythonPath -m pip install streamlit" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Application stopped" -ForegroundColor Green
Write-Host "Thank you for using Fabricator.ai MVP!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Read-Host "Press Enter to exit"

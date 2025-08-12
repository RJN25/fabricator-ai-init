@echo off
title Fabricator.ai MVP - Launch
color 0A

echo.
echo ========================================
echo    🔧 Fabricator.ai MVP Launcher
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "app.py" (
    echo ❌ Error: app.py not found in current directory
    echo Please run this script from the 'PoC1 Attempt1' folder
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "..\fabenv\Scripts\activate.bat" (
    echo ❌ Error: Virtual environment not found
    echo Please ensure the fabenv folder exists in the parent directory
    echo.
    pause
    exit /b 1
)

echo ✅ Found virtual environment
echo.

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call ..\fabenv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ Failed to activate virtual environment
    echo.
    pause
    exit /b 1
)

echo ✅ Virtual environment activated
echo.

REM Check if ezdxf is available
echo 🔍 Checking required modules...
python -c "import ezdxf" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  ezdxf module not available. Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Failed to install dependencies
        echo.
        pause
        exit /b 1
    )
    echo ✅ Dependencies installed
)

echo.
echo 🚀 Launching Fabricator.ai MVP...
echo The application will open in your browser at: http://localhost:8501
echo To stop the application, press Ctrl+C in this window
echo.

REM Launch Streamlit using the virtual environment's Python
REM This ensures all modules are available
echo 🔧 Using virtual environment Python for Streamlit...
..\fabenv\Scripts\python.exe -m streamlit run app.py

echo.
echo ========================================
echo    Application stopped
echo ========================================
echo Thank you for using Fabricator.ai MVP!
echo.
pause

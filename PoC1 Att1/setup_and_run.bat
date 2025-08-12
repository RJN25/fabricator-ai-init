@echo off
title Fabricator.ai MVP - Setup and Launch
color 0A

echo.
echo ========================================
echo    🔧 Fabricator.ai MVP Launcher
echo ========================================
echo.
echo This script will:
echo 1. Check Python installation
echo 2. Activate virtual environment
echo 3. Install required dependencies
echo 4. Generate sample test data
echo 5. Run system tests
echo 6. Launch the Streamlit application
echo.
echo Press any key to continue...
pause >nul

echo.
echo ========================================
echo    Step 1: Checking Python Installation
echo ========================================
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Python found
    python --version
)

echo.
echo ========================================
echo    Step 2: Activating Virtual Environment
echo ========================================
echo Activating virtual environment...
call ..\fabenv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ Failed to activate virtual environment
    echo Please ensure fabenv folder exists in parent directory
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Virtual environment activated
    echo Current Python: 
    where python
)

echo.
echo ========================================
echo    Step 3: Installing Dependencies
echo ========================================
echo Installing required packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    echo Please check your internet connection and try again
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Dependencies installed successfully
)

echo.
echo ========================================
echo    Step 4: Generating Sample Data
echo ========================================
echo Creating test images for validation...
python sample_data.py
if %errorlevel% neq 0 (
    echo ⚠️  Warning: Sample data generation failed
    echo Continuing without sample data...
) else (
    echo ✅ Sample data created successfully
)

echo.
echo ========================================
echo    Step 5: Running System Tests
echo ========================================
echo Testing core functionality...
python test_mvp.py
if %errorlevel% neq 0 (
    echo ⚠️  Warning: Some tests failed
    echo The application may not work correctly
    echo.
    echo Press any key to continue anyway...
    pause >nul
) else (
    echo ✅ All tests passed successfully
)

echo.
echo ========================================
echo    Step 6: Launching Fabricator.ai
echo ========================================
echo.
echo 🎉 Setup complete! Launching Fabricator.ai MVP...
echo.
echo The application will open in your browser at:
echo    http://localhost:8501
echo.
echo Features available:
echo    📝 Text-to-DXF conversion
echo    ✏️  Sketch-to-DXF conversion  
echo    ⚙️  Adjustable precision (1-10)
echo    📊 Real-time processing metrics
echo    📥 Downloadable DXF files
echo.
echo To stop the application, press Ctrl+C in this window
echo.
echo ========================================
echo    🚀 Starting Fabricator.ai...
echo ========================================
echo.

streamlit run app.py

echo.
echo ========================================
echo    Application stopped
echo ========================================
echo.
echo Thank you for using Fabricator.ai MVP!
echo.
pause

@echo off
echo ========================================
echo    Fabricator.ai - MVP Launcher
echo ========================================
echo.
echo Starting Fabricator.ai application...
echo.
echo This will:
echo 1. Install required dependencies
echo 2. Launch the Streamlit web interface
echo 3. Open your browser to localhost:8501
echo.
echo Press any key to continue...
pause >nul

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Launching Fabricator.ai...
echo.
echo The application will open in your browser at:
echo http://localhost:8501
echo.
echo To stop the application, press Ctrl+C in this window
echo.
streamlit run app.py

echo.
echo Application stopped. Press any key to exit...
pause >nul

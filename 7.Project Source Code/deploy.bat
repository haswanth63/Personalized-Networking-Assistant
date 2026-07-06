@echo off
echo ========================================
echo 🚀 Personalized Networking Assistant
echo Local Deployment
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

echo 📌 Activating virtual environment...
call venv\Scripts\activate.bat
echo ✅ Virtual environment activated!
echo.

echo ========================================
echo 📌 Starting Backend Server (FastAPI)
echo ========================================
echo Backend will run at: http://127.0.0.1:8000
echo API Docs: http://127.0.0.1:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start backend in a new window
start "FastAPI Backend" cmd /k "call venv\Scripts\activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo 📌 Starting Frontend Server (Streamlit)
echo ========================================
echo Frontend will run at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start frontend in a new window
start "Streamlit Frontend" cmd /k "call venv\Scripts\activate && streamlit run frontend/streamlit_app.py"

echo.
echo ========================================
echo ✅ Deployment Complete!
echo ========================================
echo.
echo 📊 Access your application:
echo    Frontend: http://localhost:8501
echo    Backend API: http://127.0.0.1:8000
echo    API Docs: http://127.0.0.1:8000/docs
echo.
echo 💡 Press Ctrl+C in each window to stop the servers
echo.
pause
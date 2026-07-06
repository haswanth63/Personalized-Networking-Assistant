@echo off
setlocal enabledelayedexpansion

echo ========================================
echo 🚀 Personalised Networking Assistant
echo Setting up your project...
echo ========================================
echo.

REM ============================================
REM STEP 1: Check Python Installation
REM ============================================
echo 📌 Step 1: Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.11+ from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)
python --version
echo ✅ Python found!
echo.

REM ============================================
REM STEP 2: Check requirements.txt exists
REM ============================================
echo 📌 Step 2: Checking for requirements.txt...
if not exist "requirements.txt" (
    echo ❌ requirements.txt not found!
    echo.
    echo Please create requirements.txt in the project folder.
    echo The file should contain all project dependencies.
    echo.
    pause
    exit /b 1
)
echo ✅ requirements.txt found!
echo.

REM ============================================
REM STEP 3: Create Virtual Environment
REM ============================================
echo 📌 Step 3: Creating virtual environment...
if exist "venv" (
    echo ⚠️ Virtual environment already exists. Removing old one...
    rmdir /s /q venv
)
python -m venv venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment!
    pause
    exit /b 1
)
echo ✅ Virtual environment created!
echo.

REM ============================================
REM STEP 4: Activate Virtual Environment
REM ============================================
echo 📌 Step 4: Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment!
    pause
    exit /b 1
)
echo ✅ Virtual environment activated!
echo.

REM ============================================
REM STEP 5: Upgrade pip
REM ============================================
echo 📌 Step 5: Upgrading pip...
python -m pip install --upgrade pip
echo.

REM ============================================
REM STEP 6: Install Dependencies
REM ============================================
echo 📌 Step 6: Installing dependencies...
echo This may take 5-10 minutes depending on your internet speed...
echo.
echo 📦 Installing packages from requirements.txt...
echo.

pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ❌ Failed to install some dependencies!
    echo.
    echo Try installing manually:
    echo   1. Activate virtual environment: venv\Scripts\activate
    echo   2. Install packages individually
    echo.
    pause
    exit /b 1
)
echo.
echo ✅ All dependencies installed successfully!
echo.

REM ============================================
REM STEP 7: Verify Installation
REM ============================================
echo 📌 Step 7: Verifying installations...
echo.
python -c "import fastapi; print('✅ FastAPI installed')" 2>nul || echo ❌ FastAPI missing
python -c "import streamlit; print('✅ Streamlit installed')" 2>nul || echo ❌ Streamlit missing
python -c "import transformers; print('✅ Transformers installed')" 2>nul || echo ❌ Transformers missing
python -c "import torch; print('✅ PyTorch installed')" 2>nul || echo ❌ PyTorch missing
python -c "import wikipedia; print('✅ Wikipedia-API installed')" 2>nul || echo ❌ Wikipedia-API missing
python -c "import requests; print('✅ Requests installed')" 2>nul || echo ❌ Requests missing
python -c "import pandas; print('✅ Pandas installed')" 2>nul || echo ❌ Pandas missing
python -c "import pytest; print('✅ Pytest installed')" 2>nul || echo ❌ Pytest missing
echo.

REM ============================================
REM STEP 8: Create Data Directory
REM ============================================
echo 📌 Step 8: Creating data directory...
if not exist "data" (
    mkdir data
    echo ✅ Data directory created!
) else (
    echo ✅ Data directory already exists.
)
echo.

REM ============================================
REM STEP 9: Create Backend Directories
REM ============================================
echo 📌 Step 9: Creating backend directories...
if not exist "backend" (
    mkdir backend
    echo ✅ Backend directory created!
) else (
    echo ✅ Backend directory already exists.
)

if not exist "frontend" (
    mkdir frontend
    echo ✅ Frontend directory created!
) else (
    echo ✅ Frontend directory already exists.
)
echo.

REM ============================================
REM STEP 10: Final Summary
REM ============================================
echo ========================================
echo ✅ SETUP COMPLETE!
echo ========================================
echo.
echo 📊 Installation Summary:
echo    Python:        Found ✓
echo    Virtual Env:   Created ✓
echo    Dependencies:  Installed ✓
echo    Data Folder:   Created ✓
echo.
echo ========================================
echo 🚀 How to Run the Application:
echo ========================================
echo.
echo 1️⃣ Start the Backend (FastAPI):
echo    ----------------------------------------
echo    venv\Scripts\activate
echo    cd backend
echo    python main.py
echo    ----------------------------------------
echo    The API will run at: http://localhost:8000
echo    API Docs at:        http://localhost:8000/docs
echo.
echo 2️⃣ Start the Frontend (Streamlit):
echo    ----------------------------------------
echo    [Open a NEW Command Prompt]
echo    venv\Scripts\activate
echo    cd frontend
echo    streamlit run app.py
echo    ----------------------------------------
echo    The UI will run at: http://localhost:8501
echo.
echo ========================================
echo 💡 Tips:
echo ========================================
echo    - Keep both terminals open while running
echo    - Press Ctrl+C to stop the server
echo    - Check the /docs endpoint for API testing
echo.
pause
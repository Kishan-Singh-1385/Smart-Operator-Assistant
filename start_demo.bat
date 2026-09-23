@echo off
setlocal

echo ===================================================
echo Smart Operator Assistant - End-to-End Startup
echo ===================================================

echo [1/5] Checking Database Configuration...
if not exist ".env" (
    echo [INFO] .env not found. Copying .env.example...
    copy .env.example .env
    echo [WARNING] Please update the DATABASE_URL in .env before running this script if you haven't already.
    echo If your local postgres is running on postgres:postgres@localhost:5432/smart_operator_db, it will work automatically.
)

echo [2/5] Setting up Python Backend...
if not exist ".venv" (
    echo [INFO] Creating Python virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate

echo [INFO] Installing Python dependencies (this may take a moment)...
:retry_pip
pip install -r backend\requirements.txt
if %ERRORLEVEL% neq 0 (
    echo [ERROR] pip install failed (possibly due to network timeout). Retrying in 3 seconds...
    timeout /t 3 >nul
    goto retry_pip
)

echo [3/5] Training ML Models...
echo [INFO] Training Task Prediction Model...
python ml\src\task_prediction.py
echo [INFO] Training Anomaly Detection Model...
python ml\src\anomaly_detection.py

echo [4/5] Seeding Database...
python backend\seed.py

echo [5/5] Setting up Node Frontend...
cd frontend

echo [INFO] Installing NPM dependencies...
:retry_npm
call npm install
if %ERRORLEVEL% neq 0 (
    echo [ERROR] npm install failed (possibly due to network timeout). Retrying in 3 seconds...
    timeout /t 3 >nul
    goto retry_npm
)

echo ===================================================
echo [SUCCESS] All systems ready!
echo ===================================================
echo Starting FastAPI Backend (Port 8000)...
start "FastAPI Backend" cmd /c "cd .. && call .venv\Scripts\activate && uvicorn backend.app.main:app --reload"

echo Starting React Frontend (Port 5173)...
start "React Frontend" cmd /c "npm run dev"

echo.
echo The backend is running in a new terminal window.
echo The frontend is running in another terminal window.
echo You can access the dashboard at http://localhost:5173
echo.

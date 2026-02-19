@echo off
REM Development environment setup for Windows

echo 🚀 Setting up Fingerprint Enhancer Development Environment...

REM Backend setup
echo 📦 Setting up backend...
cd backend
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

pip install --upgrade pip
pip install -r requirements.txt

REM Create .env file
if not exist .env (
    copy .env.example .env
    echo ✅ Created .env file
)

cd ..

REM Frontend setup
echo 📦 Setting up frontend...
cd fingerprint-web\client
call npm install
cd ..\..

REM Final message
echo.
echo ✅ Development environment setup complete!
echo.
echo To start developing:
echo   1. Backend: cd backend ^&^& python run.py
echo   2. Frontend: cd fingerprint-web\client ^&^& npm start
echo.
echo Or use Docker Compose:
echo   docker-compose up

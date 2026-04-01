@echo off
echo Setting up Library Management System...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH!
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Create a MySQL database named 'library_db'
echo 2. Run the application: python app.py
echo 3. Open http://localhost:5000 in your browser
echo.
pause

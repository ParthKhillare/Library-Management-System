@echo off
set -e

echo 🚀 Starting Library Management System MySQL deployment...

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

REM Create .env file if it doesn't exist
if not exist .env (
    echo 📝 Creating .env file from production template...
    copy .env.production .env >nul
    echo ⚠️  Please edit .env file with your production MySQL settings.
    echo    Current settings use default MySQL credentials.
    echo    Make sure MySQL is accessible or update credentials.
    pause
    exit /b 1
)

REM Build and start application
echo 🔨 Building Docker images...
docker-compose build

echo 🗄️  Waiting for MySQL to start...
docker-compose up -d mysql

echo ⏳ Waiting 15 seconds for MySQL to be ready...
timeout /t 15 >nul

echo 📚 Importing sample data into MySQL...
docker-compose run --rm web python import_mysql_data.py

echo 🚀 Starting web application...
docker-compose up -d

echo ✅ MySQL deployment complete!
echo.
echo 🌐 Application is running at: http://localhost:5000
echo 🗄️  MySQL database at: localhost:3306
echo 🔧 Database admin at: http://localhost:8080
echo.
echo 📊 Check logs with: docker-compose logs -f
echo 🛑 Stop with: docker-compose down
echo.
echo 👤 Default login credentials:
echo    Admin: admin@library.com / admin123
echo    Student: john@student.com / student123
pause

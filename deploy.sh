#!/bin/bash

# Production Deployment Script for Library Management System with MySQL

set -e

echo "🚀 Starting Library Management System MySQL deployment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from production template..."
    cp .env.production .env
    echo "⚠️  Please edit .env file with your production MySQL settings before running again."
    echo "   Current settings use default MySQL credentials."
    echo "   Make sure MySQL is accessible or update credentials."
    exit 1
fi

echo "🔨 Building Docker images..."
docker-compose build

echo "🗄️  Waiting for MySQL to start..."
docker-compose up -d mysql

echo "⏳ Waiting 15 seconds for MySQL to be ready..."
sleep 15

echo "📚 Importing sample data into MySQL..."
docker-compose run --rm web python import_mysql_data.py

echo "🚀 Starting web application..."
docker-compose up -d

echo "✅ MySQL deployment complete!"
echo ""
echo "🌐 Application is running at: http://localhost:5000"
echo "🗄️  MySQL database at: localhost:3306"
echo "🔧 Database admin at: http://localhost:8080"
echo ""
echo "📊 Check logs with: docker-compose logs -f"
echo "🛑 Stop with: docker-compose down"
echo ""
echo "👤 Default login credentials:"
echo "   Admin: admin@library.com / admin123"
echo "   Student: john@student.com / student123"

#!/bin/bash

echo "Setting up Library Management System..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed!"
    echo "Please install Python from https://python.org"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo
echo "Setup complete!"
echo
echo "Next steps:"
echo "1. Create a MySQL database named 'library_db'"
echo "2. Run the application: python app.py"
echo "3. Open http://localhost:5000 in your browser"
echo

#!/bin/bash
# THIS FILE DOES NOT WORK JUST FOR SHOW 'LOL!'
# Setup script for Customer Support Chatbot

# Exit on any error
set -e

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
echo "Installing project dependencies..."
pip install -r requirements.txt

# Set up environment variables
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please edit .env file with your actual credentials"
fi

# Optional: Run initial database migrations or setup
# Uncomment and modify as needed
# python src/database/initialize.py

# Optional: Run tests to ensure everything is working
echo "Running initial tests..."
python -m pytest tests/

echo "Setup complete! Activate the virtual environment with 'source venv/bin/activate'"
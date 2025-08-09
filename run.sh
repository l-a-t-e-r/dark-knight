#!/bin/bash

# Instagram Username Auto Claimer - Linux Launcher
# Made by Later.lol (c) 2025

clear
echo "===================================="
echo " Instagram Username Auto Claimer"
echo " Made by Later.lol (c) 2025"
echo "===================================="
echo

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.6+ using your package manager:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  CentOS/RHEL:   sudo yum install python3 python3-pip"
    echo "  Arch:          sudo pacman -S python python-pip"
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 is not installed"
    echo "Please install pip3 using your package manager"
    exit 1
fi

# Install dependencies if needed
if [ ! -f "requirements_installed.flag" ]; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -eq 0 ]; then
        touch requirements_installed.flag
        echo "Dependencies installed successfully!"
    else
        echo "Failed to install dependencies"
        exit 1
    fi
    echo
fi

# Check if usernames.txt has actual usernames
if ! grep -v '^#' usernames.txt | grep -q '^[^[:space:]]*[^[:space:]]'; then
    echo "WARNING: No usernames found in usernames.txt"
    echo "Please edit usernames.txt and add usernames to check"
    echo "Remove the # from the beginning of lines to activate them"
    echo
    read -p "Press Enter to continue anyway or Ctrl+C to exit..."
fi

# Make script executable if it isn't
chmod +x "$0"

echo "Starting Instagram Username Checker..."
echo "Press Ctrl+C to stop"
echo

python3 instagram_claimer.py

echo
echo "Instagram Username Checker stopped."
read -p "Press Enter to exit..."
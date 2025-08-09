@echo off
title Instagram Username Auto Claimer
echo.
echo ====================================
echo  Instagram Username Auto Claimer
echo  Made by Later.lol (c) 2025
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.6+ from https://python.org
    pause
    exit /b 1
)

REM Install dependencies if needed
if not exist "requirements_installed.flag" (
    echo Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% equ 0 (
        echo. > requirements_installed.flag
        echo Dependencies installed successfully!
    ) else (
        echo Failed to install dependencies
        pause
        exit /b 1
    )
    echo.
)

REM Check if usernames.txt has actual usernames
findstr /v /c:"#" usernames.txt | findstr /r "." >nul
if %errorlevel% neq 0 (
    echo WARNING: No usernames found in usernames.txt
    echo Please edit usernames.txt and add usernames to check
    echo Remove the # from the beginning of lines to activate them
    echo.
    pause
)

echo Starting Instagram Username Checker...
echo Press Ctrl+C to stop
echo.

python instagram_claimer.py

echo.
echo Instagram Username Checker stopped.
pause
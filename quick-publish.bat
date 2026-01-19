@echo off
title Quick Publish Tool

echo.
echo ========================================
echo Quick Publish Tool
echo ========================================
echo.

echo [Step 1] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found
    echo Please install Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python is installed
echo.

echo [Step 2] Running publish script...
python 快速发布.py

echo.
echo Press any key to exit...
pause >nul

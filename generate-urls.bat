@echo off
title Generate Image URLs

echo.
echo ========================================
echo Generate Image URLs
echo ========================================
echo.

echo [Step 1] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not installed
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python is installed
echo.

echo [Step 2] Generating URLs...
python generate_urls.py

echo.
echo Press any key to exit...
pause >nul

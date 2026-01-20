@echo off
chcp 65001 >nul
title Add Article by Date

echo.
echo ========================================
echo Add Article to Mini Program by Date
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

echo [Step 2] Enter date (format: 20260120)
set /p date_folder="Date: "

echo.
echo [Step 3] Generating URLs for %date_folder%...
python generate_urls_by_date.py %date_folder%

echo.
echo Press any key to exit...
pause >nul

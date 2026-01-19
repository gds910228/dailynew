@echo off
title Upload Images via GitHub API

echo.
echo ========================================
echo Upload Images via GitHub API
echo ========================================
echo.
echo This tool uploads images directly to GitHub
echo without using git push (bypasses network issues)
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not installed
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Starting upload...
echo.

python upload_images_api.py

echo.
pause

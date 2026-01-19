@echo off
title 一键发布工具 - Upload & Publish

echo.
echo ========================================
echo   One-Click Publish Tool
echo ========================================
echo.
echo This tool will:
echo   1. Upload images to GitHub
echo   2. Generate image URLs
echo   3. Open Web Admin (URLs pre-filled)
echo.
echo ========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not installed
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if images directory exists
if not exist "assets\images" (
    echo.
    echo Creating images directory...
    mkdir "assets\images"
    echo.
    echo Please add your images to: assets\images\
    echo.
    pause
    exit /b 0
)

REM Check if there are images
dir /b "assets\images\*.jpg" "assets\images\*.png" "assets\images\*.jpeg" "assets\images\*.gif" >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: No images found in assets\images\
    echo.
    echo Please add images first, then run this again.
    echo.
    pause
    exit /b 0
)

echo Found images in assets\images\
echo.
echo Starting publish process...
echo.

python publish_complete.py

echo.
echo Press any key to exit...
pause >nul

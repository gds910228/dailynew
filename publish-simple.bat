@echo off
title Daily Publish - One Click

echo.
echo ========================================
echo   Daily Publish - One Click
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not installed
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Create images directory if not exists
if not exist "assets\images" mkdir "assets\images"

echo Step 1: Add images to folder
echo   Folder: assets\images\
echo.
echo Please copy your images there now.
echo.
pause

REM Check if there are images
dir /b "assets\images\*.jpg" "assets\images\*.png" >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: No images found in assets\images\
    echo Please add images first.
    pause
    exit /b 1
)

echo.
echo Step 2: Uploading images to GitHub...
echo.

git add assets/images/
git commit -m "add images" >nul 2>&1
if errorlevel 1 (
    echo INFO: No new images to commit
) else (
    echo OK: Images committed
)

git push origin main
if errorlevel 1 (
    echo ERROR: Git push failed
    echo Please check your network and GitHub settings
    pause
    exit /b 1
)

echo.
echo Step 3: Generating image URLs...
echo.

python generate_urls.py

if errorlevel 1 (
    echo WARNING: URL generation failed
    echo You can manually get URLs from GitHub
)

echo.
echo ========================================
echo   Done!
echo ========================================
echo.
echo Next steps:
echo 1. Copy the image URLs above
echo 2. Paste in Web Admin
echo 3. Fill article info
echo 4. Click submit
echo 5. Refresh mini-program
echo.
pause

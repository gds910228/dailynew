@echo off
title 按日期添加文章

echo.
echo ========================================
echo 按日期添加文章到小程序
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

echo [Step 2] 输入日期（格式：20260120）
set /p date_folder="请输入日期: "

echo.
echo [Step 3] Generating URLs for %date_folder%...
python generate_urls_by_date.py %date_folder%

echo.
echo Press any key to exit...
pause >nul

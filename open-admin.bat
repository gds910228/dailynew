@echo off
title Open Web Admin

echo.
echo ========================================
echo Open Web Admin Panel
echo ========================================
echo.

set "CURRENT_DIR=%~dp0"
set "ADMIN_FILE=%CURRENT_DIR%admin\index.html"

if not exist "%ADMIN_FILE%" (
    echo [ERROR] Admin file not found
    echo Path: %ADMIN_FILE%
    pause
    exit /b 1
)

echo [INFO] Opening web admin...
echo.

start "" "%ADMIN_FILE%"

echo [OK] Web admin opened in browser
echo.
echo If browser does not open, visit:
echo file:///%ADMIN_FILE:\=/%
echo.
timeout /t 3 >nul

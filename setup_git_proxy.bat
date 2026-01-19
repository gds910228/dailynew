@echo off
title Setup Git Proxy

echo.
echo ========================================
echo Git Proxy Configuration
echo ========================================
echo.
echo This script helps you configure Git proxy for GitHub access.
echo.

REM 显示当前配置
echo Current proxy settings:
echo.
git config --global --get http.proxy
git config --global --get https.proxy
echo.

echo ========================================
echo Common Proxy Ports:
echo ========================================
echo.
echo Clash/V2ray clients usually use:
echo   - HTTP Proxy:  127.0.0.1:7890
echo   - SOCKS5 Proxy: 127.0.0.1:7891
echo.
echo V2rayN usually uses:
echo   - HTTP Proxy:  127.0.0.1:10809
echo   - SOCKS5 Proxy: 127.0.0.1:10808
echo.
echo ========================================
echo.

echo Please check your proxy software settings to find the correct port.
echo.
set /p PROXY_PORT="Enter your proxy port (or press Enter to skip): "

if "%PROXY_PORT%"=="" (
    echo.
    echo [INFO] Skipping proxy configuration
    echo.
    choice /C YN /M "Remove existing proxy settings"
    if errorlevel 2 goto :end
    if errorlevel 1 goto :remove_proxy
)

echo.
echo Setting proxy to: http://127.0.0.1:%PROXY_PORT%
git config --global http.proxy http://127.0.0.1:%PROXY_PORT%
git config --global https.proxy http://127.0.0.1:%PROXY_PORT%

echo.
echo [OK] Proxy configured!
echo.
echo Testing connection...
git ls-remote https://github.com/ HEAD
if errorlevel 1 (
    echo.
    echo [WARNING] Connection test failed!
    echo Please verify:
    echo   1. Proxy software is running
    echo   2. Port number is correct
    echo   3. Proxy allows HTTP tunneling
) else (
    echo.
    echo [OK] GitHub connection successful!
)
goto :end

:remove_proxy
echo.
echo Removing proxy settings...
git config --global --unset http.proxy
git config --global --unset https.proxy
echo [OK] Proxy settings removed
goto :end

:end
echo.
pause

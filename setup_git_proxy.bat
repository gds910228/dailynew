@echo off
title Setup Git Proxy

echo.
echo ========================================
echo Git代理配置工具
echo ========================================
echo.

echo 如果你有VPN/代理，可以使用此工具配置git代理
echo.
echo 常见代理地址:
echo   - Clash: 127.0.0.1:7890
echo   - V2Ray: 127.0.0.1:10809
echo   - 其他: 请查看你的代理软件设置
echo.

echo ========================================
echo 选择操作:
echo ========================================
echo.
echo 1. 设置代理
echo 2. 取消代理
echo 3. 查看当前代理设置
echo 4. 退出
echo.

set /p choice="请选择 (1-4): "

if "%choice%"=="1" goto SET_PROXY
if "%choice%"=="2" goto UNSET_PROXY
if "%choice%"=="3" goto VIEW_PROXY
if "%choice%"=="4" goto END

:SET_PROXY
echo.
set /p proxy_addr="请输入代理地址 (例如: 127.0.0.1:7890): "

echo.
echo 设置HTTP代理: %proxy_addr%
git config --global http.proxy http://%proxy_addr%

echo 设置HTTPS代理: %proxy_addr%
git config --global https.proxy http://%proxy_addr%

echo.
echo ✅ 代理设置完成！
echo.
echo 现在可以重试上传图片了
goto END

:UNSET_PROXY
echo.
echo 取消HTTP代理...
git config --global --unset http.proxy

echo 取消HTTPS代理...
git config --global --unset https.proxy

echo.
echo ✅ 代理已取消
goto END

:VIEW_PROXY
echo.
echo 当前代理设置:
echo.
echo HTTP代理:
git config --global --get http.proxy
if errorlevel 1 echo   (未设置)

echo.
echo HTTPS代理:
git config --global --get https.proxy
if errorlevel 1 echo   (未设置)
goto END

:END
echo.
pause

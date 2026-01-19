@echo off
title Test URL Auto-fill

echo.
echo ========================================
echo Test URL Auto-fill Feature
echo ========================================
echo.

python -c "import base64, urllib.parse, webbrowser, os; urls = ['https://test1.jpg', 'https://test2.jpg', 'https://test3.jpg']; text = '\n'.join(urls); b64 = base64.b64encode(text.encode('utf-8')).decode('utf-8'); safe = urllib.parse.quote(b64); admin_path = os.path.abspath('admin/test_autofill.html'); file_url = admin_path.replace('\\', '/'); full_url = f'file:///{file_url}?urls={safe}'; print(f'Opening: {full_url}'); webbrowser.open(full_url)"

echo.
echo Check browser console (F12) for debug info
echo.
pause

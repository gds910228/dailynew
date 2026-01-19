#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试 os.startfile 打开带参数的URL"""

import os
import base64
import urllib.parse

# 模拟生成URL
urls = [
    "https://raw.githubusercontent.com/gds910228/dailynew/main/assets/images/test1.jpg",
    "https://raw.githubusercontent.com/gds910228/dailynew/main/assets/images/test2.jpg"
]

urls_text = '\n'.join(urls)
urls_b64 = base64.b64encode(urls_text.encode('utf-8')).decode('utf-8')
urls_b64_safe = urllib.parse.quote(urls_b64)

admin_path = os.path.abspath("admin/index.html")
file_url = admin_path.replace('\\', '/')
file_url = f'file:///{file_url}'
full_url = f'{file_url}?urls={urls_b64_safe}'

print("="*70)
print("测试 os.startfile 打开带参数的URL")
print("="*70)
print(f"\n完整URL:")
print(full_url)
print(f"\nURL长度: {len(full_url)} 字符")
print(f"\n准备打开浏览器...")

try:
    os.startfile(full_url)
    print("✅ 浏览器已打开")
    print("\n请检查：")
    print("1. 浏览器是否打开了admin页面")
    print("2. 图片URL框是否自动填充了测试URL")
    print("3. 按F12查看控制台日志")
except Exception as e:
    print(f"❌ 错误: {e}")

print("\n" + "="*70)
input("按回车退出...")

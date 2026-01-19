#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试URL生成"""

import os
import base64
import urllib.parse

# 模拟生成URL
urls = [
    "https://raw.githubusercontent.com/gds910228/dailynew/main/assets/images/test1.jpg",
    "https://raw.githubusercontent.com/gds910228/dailynew/main/assets/images/test2.jpg"
]

# 方法1：直接Base64编码
urls_text = '\n'.join(urls)
urls_b64 = base64.b64encode(urls_text.encode('utf-8')).decode('utf-8')

# 方法2：URL安全的Base64编码
import urllib.parse
urls_b64_urlsafe = urllib.parse.quote(urls_b64)

admin_path = os.path.abspath("admin/index.html")

print("="*70)
print("测试URL生成")
print("="*70)
print(f"\nAdmin路径: {admin_path}")
print(f"\n编码后的URL: {urls_b64[:100]}...")
print(f"\nURL安全编码: {urls_b64_urlsafe[:100]}...")

# Windows文件路径转换
if os.name == 'nt':
    # Windows: 将反斜杠转换为正斜杠，并添加 file:/// 前缀
    file_url = admin_path.replace('\\', '/')
    file_url = f'file:///{file_url}'
else:
    file_url = f'file://{admin_path}'

print(f"\n文件URL: {file_url}")
print(f"\n完整URL: {file_url}?urls={urls_b64_urlsafe}")

print("\n" + "="*70)

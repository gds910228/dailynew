#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成正确的图片URL（支持中文文件名）
"""

import os
import urllib.parse
import webbrowser

def generate_image_urls():
    """生成所有图片的正确URL"""
    images_dir = "assets/images"

    if not os.path.exists(images_dir):
        print(f"[ERROR] Directory not found: {images_dir}")
        return []

    urls = []
    image_files = []

    # 获取所有图片文件
    for filename in os.listdir(images_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            image_files.append(filename)

    if not image_files:
        print("[INFO] No images found")
        return []

    # 按文件名排序
    image_files.sort()

    print("\n" + "="*70)
    print(" Image URLs (Copy and Paste to Web Admin):")
    print("="*70)

    for i, filename in enumerate(image_files, 1):
        # URL编码文件名
        encoded_filename = urllib.parse.quote(filename)

        # 生成URL
        url = f"https://raw.githubusercontent.com/gds910228/dailynew/main/assets/images/{encoded_filename}"

        urls.append(url)

        # 显示结果
        print(f"\n{i}. {filename}")
        print(f"   {url}")

    print("\n" + "="*70)

    return urls

def check_chinese_filename(filename):
    """检查文件名是否包含中文字符"""
    return any('\u4e00' <= char <= '\u9fff' for char in filename)

def main():
    print("\n" + "="*70)
    print(" Image URL Generator - Supports Chinese Filenames")
    print("="*70 + "\n")

    # 检查目录
    images_dir = "assets/images"
    if not os.path.exists(images_dir):
        print(f"[ERROR] Please create directory: {images_dir}")
        print("Usage:")
        print("  1. Create folder: assets/images")
        print("  2. Put your images there")
        print("  3. Run this script again")
        return

    # 生成URL
    urls = generate_image_urls()

    if not urls:
        print("\n[INFO] No images found in assets/images/")
        print("Please add images and try again.")
        return

    # 检查是否有中文文件名
    print("\n[TIP] Filename Analysis:")
    has_chinese = False
    for filename in os.listdir(images_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            if check_chinese_filename(filename):
                has_chinese = True
                try:
                    print(f"  [WARNING] {filename} - Contains Chinese characters (URL encoded)")
                except:
                    print(f"  [WARNING] Filename contains Chinese characters (URL encoded)")
            else:
                try:
                    print(f"  [OK] {filename} - English filename (recommended)")
                except:
                    print(f"  [OK] English filename (recommended)")

    if has_chinese:
        print("\n" + "="*70)
        print(" Recommendation: Use English Filenames")
        print("="*70)
        print("\nTo avoid URL encoding issues, rename your files to:")
        print("  - 20250119001.jpg")
        print("  - 20250119002.jpg")
        print("  - gl-17-openai-marketing.jpg")
        print("\nThis makes URLs shorter and more reliable.")

    # 询问是否打开Web后台
    print("\n" + "="*70)
    choice = input("\nOpen Web Admin? (y/n): ").lower().strip()

    if choice == 'y':
        admin_path = os.path.abspath("admin/index.html")
        if os.path.exists(admin_path):
            webbrowser.open(f'file:///{admin_path}')
            print(f"\n[OK] Web Admin opened")
        else:
            print(f"\n[ERROR] File not found: {admin_path}")

    print("\n" + "="*70)
    print(" Next Steps:")
    print("="*70)
    print("1. Copy the image URLs above")
    print("2. Open Web Admin (or it's already opened)")
    print("3. Paste URLs in Web Admin (one URL per line)")
    print("4. Fill article information")
    print("5. Click submit")
    print("6. Refresh mini-program to view")
    print("\nDone! 🎉\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] Cancelled by user")
    except Exception as e:
        print(f"\n[ERROR] {e}")

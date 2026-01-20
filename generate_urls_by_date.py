#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按日期生成图片URL（支持子文件夹结构）
用法：python generate_urls_by_date.py 20260120
"""

import os
import sys
import urllib.parse
import subprocess

def generate_urls_for_date(date_folder):
    """生成指定日期文件夹的图片URL"""
    images_dir = f"assets/images/{date_folder}"

    if not os.path.exists(images_dir):
        print(f"[ERROR] Date folder not found: {images_dir}")
        print(f"\nAvailable date folders:")
        base_dir = "assets/images"
        if os.path.exists(base_dir):
            for item in os.listdir(base_dir):
                item_path = os.path.join(base_dir, item)
                if os.path.isdir(item_path):
                    print(f"  - {item}")
        return []

    urls = []
    image_files = []

    # 只扫描指定日期文件夹
    for filename in os.listdir(images_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            image_files.append(filename)

    if not image_files:
        print(f"[INFO] No images found in {images_dir}")
        return []

    # 按文件名排序
    image_files.sort()

    print("\n" + "="*70)
    print(f" Image URLs for {date_folder}")
    print("="*70)

    for i, filename in enumerate(image_files, 1):
        # 构建相对路径（包含日期文件夹）
        rel_path = f"{date_folder}/{filename}"
        # URL编码
        encoded_path = urllib.parse.quote(rel_path)

        # 生成URL
        url = f"https://raw.githubusercontent.com/gds910228/dailynew/main/assets/images/{encoded_path}"

        urls.append(url)

        # 显示结果
        print(f"\n{i}. {filename}")
        print(f"   {url}")

    print("\n" + "="*70)
    print(f" Total: {len(urls)} images")
    print("="*70)

    return urls

def upload_images(date_folder):
    """上传指定日期的图片到GitHub"""
    print("\n" + "="*70)
    print(f" Uploading Images for {date_folder}")
    print("="*70)

    images_path = f"assets/images/{date_folder}"

    # Git add
    print(f"\n[Step 1/3] Adding {images_path} to git...")
    result = subprocess.run(['git', 'add', images_path],
                          capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] Git add failed")
        return False

    # Git commit
    print(f"[Step 2/3] Committing images...")
    result = subprocess.run(['git', 'commit', '-m', f'Add images for {date_folder}'],
                          capture_output=True, text=True)
    if result.returncode != 0:
        if "nothing to commit" in result.stdout or "no changes added" in result.stdout:
            print("[INFO] No new images to commit")
        else:
            print(f"[ERROR] Git commit failed")
            return False
    else:
        print("[OK] Images committed")

    # Git push
    print("[Step 3/3] Pushing to GitHub...")
    result = subprocess.run(['git', 'push', 'origin', 'main'],
                          capture_output=True, text=True)

    if result.returncode != 0:
        print(f"[ERROR] Git push failed")
        return False

    print("[OK] Images uploaded to GitHub!")
    return True

def main():
    if len(sys.argv) < 2:
        print("\n" + "="*70)
        print(" Image URL Generator - By Date Folder")
        print("="*70)
        print("\nUsage: python generate_urls_by_date.py <date_folder>")
        print("\nExample:")
        print("  python generate_urls_by_date.py 20260120")
        print("\nAvailable date folders:")
        base_dir = "assets/images"
        if os.path.exists(base_dir):
            for item in sorted(os.listdir(base_dir)):
                item_path = os.path.join(base_dir, item)
                if os.path.isdir(item_path):
                    print(f"  - {item}")
        print("\n" + "="*70)
        return

    date_folder = sys.argv[1]

    # 验证日期格式（8位数字）
    if not date_folder.isdigit() or len(date_folder) != 8:
        print(f"[ERROR] Invalid date format: {date_folder}")
        print("Expected format: 20260120 (YYYYMMDD)")
        return

    print("\n" + "="*70)
    print(f" Processing Date: {date_folder}")
    print("="*70)

    # 生成URL
    urls = generate_urls_for_date(date_folder)

    if not urls:
        print(f"\n[INFO] No images found for {date_folder}")
        return

    # 将URL保存到文件（方便复制）
    urls_file = f"urls_{date_folder}.txt"
    with open(urls_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(urls))
    print(f"\n[OK] URLs saved to: {urls_file}")

    # 询问是否上传图片
    print("\n" + "="*70)
    upload_choice = input(f"\nUpload {date_folder} images to GitHub? (y/n): ").lower().strip()

    if upload_choice == 'y':
        if not upload_images(date_folder):
            print("\n[WARNING] Image upload failed")
            choice = input("\nContinue anyway? (y/n): ").lower().strip()
            if choice != 'y':
                return

    print("\n" + "="*70)
    print(" Next Steps:")
    print("="*70)
    print(f"1. URLs copied to {urls_file}")
    print("2. Open admin/index.html in browser")
    print("3. Paste URLs into the image URL field")
    print("4. Fill in article information:")
    print(f"   - Title: 2026年X月X日 (parse from {date_folder})")
    print("   - Description: Brief summary")
    print("   - Publish Date: Corresponding date")
    print("5. Click submit to generate articles.json")
    print("6. Push articles.json to GitHub:")
    print("   git add data/articles.json")
    print(f"   git commit -m 'Add article for {date_folder}'")
    print("   git push origin main")
    print("\nDone!\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] Cancelled by user")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()

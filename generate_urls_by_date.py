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
import webbrowser
import re
from datetime import datetime

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

def generate_title_with_weekday(date_folder):
    """生成带星期几的标题，格式：2026-1-24周六 政策、热点与机会"""
    try:
        year = int(date_folder[:4])
        month = int(date_folder[4:6])
        day = int(date_folder[6:8])

        # 计算星期几
        date_obj = datetime(year, month, day)
        weekday_map = {
            0: '周一',
            1: '周二',
            2: '周三',
            3: '周四',
            4: '周五',
            5: '周六',
            6: '周日'
        }
        weekday = weekday_map[date_obj.weekday()]

        # 格式化日期，去掉前导零
        formatted_date = f"{year}-{month}-{day}{weekday}"

        # 生成完整标题
        title = f"{formatted_date} 政策、热点与机会"

        return title
    except Exception as e:
        print(f"[WARNING] Failed to generate title with weekday: {e}")
        # 如果计算失败，使用默认格式
        year = date_folder[:4]
        month = date_folder[4:6]
        day = date_folder[6:8]
        return f"{year}年{month}月{day}日"

def create_temp_admin_html(urls, date_folder):
    """创建临时的admin HTML文件，URL已经预填充"""
    admin_template_path = "admin/index.html"
    temp_admin_path = "admin/index_temp.html"

    if not os.path.exists(admin_template_path):
        print(f"[WARNING] Admin template not found: {admin_template_path}")
        return None

    # 读取原始HTML
    with open(admin_template_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 将URL列表转换为JavaScript字符串，转义换行符
    urls_escaped = '\\n'.join(urls)

    # 使用新函数生成标题（包含星期几）
    default_title = generate_title_with_weekday(date_folder)

    # 在HTML中注入预填充数据（在app.js加载之前）
    inject_script = f'''
    <script>
    // 预填充数据 - 在app.js加载之前执行
    window.__PRELOAD_URLS__ = `{urls_escaped}`;
    window.__PRELOAD_DATE__ = `{date_folder}`;
    window.__PRELOAD_TITLE__ = `{default_title}`;
    console.log('✅ URLs pre-loaded:', {len(urls)}, 'URLs');
    console.log('✅ Date: {date_folder}');
    console.log('✅ Title: {default_title}');
    </script>
    ''' + '''
    <!-- 加载配置文件 -->
    <script src="config.local.js" onerror="this.src='config.js'"></script>
    <!-- 加载app.js -->
    <script src="app.js"></script>
    <script>
    // app.js加载完成后，检查是否有预填充的URL
    window.addEventListener('load', function() {
        if (window.__PRELOAD_URLS__) {
            setTimeout(function() {
                // 填充URL
                const textarea = document.getElementById('imageUrl');
                if (textarea && !textarea.value) {
                    textarea.value = window.__PRELOAD_URLS__;
                    // 触发input事件以更新预览
                    textarea.dispatchEvent(new Event('input', { bubbles: true }));
                    console.log('✅ URLs auto-filled to textarea');
                }

                // 填充标题
                const titleInput = document.getElementById('title');
                if (titleInput && !titleInput.value && window.__PRELOAD_TITLE__) {
                    titleInput.value = window.__PRELOAD_TITLE__;
                    console.log('✅ Title auto-filled:', window.__PRELOAD_TITLE__);
                }

                // 填充日期
                const dateInput = document.getElementById('publishDate');
                if (dateInput && !dateInput.value && window.__PRELOAD_DATE__) {
                    // 格式化日期为 YYYY-MM-DD
                    const dateStr = window.__PRELOAD_DATE__;
                    const formattedDate = dateStr.substring(0, 4) + '-' +
                                        dateStr.substring(4, 6) + '-' +
                                        dateStr.substring(6, 8);
                    dateInput.value = formattedDate;
                    console.log('✅ Date auto-filled:', formattedDate);
                }

                // 填充视频号ID（如果为空）
                const videoIdInput = document.getElementById('videoId');
                if (videoIdInput && !videoIdInput.value) {
                    videoIdInput.value = '每日新知识汇';
                    console.log('✅ Video ID auto-filled: 每日新知识汇');
                }

                // 显示提示消息
                const messageDiv = document.getElementById('message');
                if (messageDiv) {
                    const urlCount = window.__PRELOAD_URLS__.split('\\n').filter(u => u.trim()).length;
                    messageDiv.textContent = `✅ 已自动加载 ${urlCount} 个图片URL (日期: ${window.__PRELOAD_DATE__})`;
                    messageDiv.className = 'message show success';
                    setTimeout(() => {
                        messageDiv.className = 'message';
                    }, 5000);
                }
            }, 100); // 延迟100ms确保app.js初始化完成
        }
    });
    </script>
    </head>'''

    # 找到并替换原有的script加载部分
    # 找到"</head>"并在它之前插入我们的脚本
    html_content = html_content.replace('</head>', inject_script)

    # 移除原有的script加载逻辑（因为我们要自定义）
    # 找到并移除从 "// 优先加载本地配置文件" 到该 script 标签结束的部分
    pattern = r'<script>\s*// 优先加载本地配置文件[\s\S]*?document\.body\.appendChild\(configScript\);\s*\}\)\(\);[\s\S]*?</script>'
    html_content = re.sub(pattern, '', html_content, flags=re.DOTALL)

    # 写入临时文件
    with open(temp_admin_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return temp_admin_path

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
            choice = input("\nContinue to open Web Admin anyway? (y/n): ").lower().strip()
            if choice != 'y':
                return

    # 询问是否打开Web后台
    print("\n" + "="*70)
    choice = input(f"\nOpen Web Admin with auto-filled URLs? (y/n): ").lower().strip()

    if choice == 'y':
        # 创建临时HTML文件
        temp_file = create_temp_admin_html(urls, date_folder)

        if temp_file and os.path.exists(temp_file):
            admin_path = os.path.abspath(temp_file)
            if os.name == 'nt':
                try:
                    os.startfile(admin_path)
                except:
                    subprocess.Popen(['cmd', '/c', 'start', '', admin_path], shell=True)
            else:
                webbrowser.open(admin_path)

            print(f"\n[OK] Web Admin opened with {len(urls)} URLs pre-filled")
            print(f"[INFO] Using temp file: {temp_file}")
            print(f"[INFO] Title auto-filled as: {default_title}")
            print(f"[INFO] Date auto-filled as: {date_folder[:4]}-{date_folder[4:6]}-{date_folder[6:8]}")
        else:
            print(f"\n[ERROR] Failed to create temp admin file")
            print(f"[INFO] You can manually copy URLs from {urls_file}")

    print("\n" + "="*70)
    print(" Next Steps:")
    print("="*70)
    print("1. Review the auto-filled information in Web Admin")
    print("2. Modify title/description if needed")
    print("3. Click submit to update articles.json")
    print("4. Push articles.json to GitHub:")
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

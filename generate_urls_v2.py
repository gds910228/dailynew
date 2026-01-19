#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成正确的图片URL（支持中文文件名）
备用方案：使用临时HTML文件传递URL
"""

import os
import urllib.parse
import webbrowser
import shutil
import subprocess

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

def create_temp_admin_html(urls):
    """创建临时的admin HTML文件，URL已经预填充"""
    admin_template_path = "admin/index.html"
    temp_admin_path = "admin/index_temp.html"

    if not os.path.exists(admin_template_path):
        return None

    # 读取原始HTML
    with open(admin_template_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 将URL列表转换为JavaScript字符串，转义换行符
    urls_escaped = '\\n'.join(urls)

    # 在HTML中注入预填充数据（在app.js加载之前）
    inject_script = f'''
    <script>
    // 预填充数据 - 在app.js加载之前执行
    window.__PRELOAD_URLS__ = `{urls_escaped}`;
    console.log('✅ URLs pre-loaded:', {len(urls)}, 'URLs');
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
                const textarea = document.getElementById('imageUrl');
                if (textarea && !textarea.value) {
                    textarea.value = window.__PRELOAD_URLS__;
                    // 触发input事件以更新预览
                    textarea.dispatchEvent(new Event('input', { bubbles: true }));
                    console.log('✅ URLs auto-filled to textarea');

                    // 显示提示消息
                    const messageDiv = document.getElementById('message');
                    if (messageDiv) {
                        const urlCount = window.__PRELOAD_URLS__.split('\\n').filter(u => u.trim()).length;
                        messageDiv.textContent = `✅ 已自动加载 ${urlCount} 个图片URL`;
                        messageDiv.className = 'message show success';
                        setTimeout(() => {
                            messageDiv.className = 'message';
                        }, 3000);
                    }
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
    # 找到并移除从 "// 优先加载本地配置文件" 到 "</script>" 的部分
    import re
    pattern = r'<script>\s*// 优先加载本地配置文件.*?</script>'
    html_content = re.sub(pattern, '', html_content, flags=re.DOTALL)

    # 写入临时文件
    with open(temp_admin_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return temp_admin_path

def upload_images():
    """上传图片到GitHub"""
    print("\n" + "="*70)
    print(" Uploading Images to GitHub")
    print("="*70)

    # 检查是否是git仓库
    if not os.path.exists('.git'):
        print("\n[ERROR] Not a git repository")
        print("Please run: git init")
        return False

    # Git add
    print("\n[Step 1/3] Adding images to git...")
    result = subprocess.run(['git', 'add', 'assets/images/'],
                          capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] Git add failed")
        return False

    # Git commit
    print("[Step 2/3] Committing images...")
    result = subprocess.run(['git', 'commit', '-m', 'Add images'],
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
        print("\nPlease check:")
        print("1. Git credentials are configured")
        print("2. 'origin' remote points to your GitHub repo")
        print("3. Network connection is working")
        return False

    print("[OK] Images uploaded to GitHub!")
    return True

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

    # 询问是否上传图片到GitHub
    print("\n" + "="*70)
    upload_choice = input("\nUpload images to GitHub first? (y/n): ").lower().strip()

    if upload_choice == 'y':
        if not upload_images():
            print("\n[WARNING] Image upload failed")
            choice = input("\nContinue to generate URLs anyway? (y/n): ").lower().strip()
            if choice != 'y':
                return

    # 询问是否打开Web后台
    print("\n" + "="*70)
    choice = input("\nOpen Web Admin? (y/n): ").lower().strip()

    if choice == 'y':
        # 创建临时HTML文件
        temp_file = create_temp_admin_html(urls)

        if temp_file and os.path.exists(temp_file):
            admin_path = os.path.abspath(temp_file)
            if os.name == 'nt':
                try:
                    os.startfile(admin_path)
                except:
                    import subprocess
                    subprocess.Popen(['cmd', '/c', 'start', '', admin_path], shell=True)
            else:
                webbrowser.open(admin_path)

            print(f"\n[OK] Web Admin opened with {len(urls)} URLs pre-filled")
            print(f"[INFO] Using temp file: {temp_file}")
        else:
            print(f"\n[ERROR] Failed to create temp admin file")

    print("\n" + "="*70)
    print(" Next Steps:")
    print("="*70)
    print("1. The Web Admin is already opened with URLs pre-filled")
    print("2. Fill in other article information")
    print("3. Click submit")
    print("4. Refresh mini-program to view")
    print("\nDone! 🎉\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] Cancelled by user")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()

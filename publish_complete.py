#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键发布工具：上传图片到GitHub -> 生成URL -> 打开后台管理
"""

import os
import subprocess
import urllib.parse
import webbrowser

def check_git():
    """检查git是否可用"""
    try:
        subprocess.run(['git', '--version'], capture_output=True, check=True)
        return True
    except:
        return False

def upload_images_to_github():
    """上传图片到GitHub"""
    images_dir = "assets/images"

    if not os.path.exists(images_dir):
        print(f"[ERROR] Directory not found: {images_dir}")
        return False

    # 检查是否有图片
    images = []
    for filename in os.listdir(images_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            images.append(filename)

    if not images:
        print("[INFO] No images found in assets/images/")
        return False

    print(f"\n[INFO] Found {len(images)} image(s)")

    # 检查是否是git仓库
    if not os.path.exists('.git'):
        print("[ERROR] Not a git repository. Please run: git init")
        return False

    # Git add
    print("\n[Step 1/3] Adding images to git...")
    result = subprocess.run(['git', 'add', 'assets/images/'],
                          capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] Git add failed: {result.stderr}")
        return False

    # Git commit
    print("[Step 2/3] Committing images...")
    result = subprocess.run(['git', 'commit', '-m', 'Add images'],
                          capture_output=True, text=True)
    if result.returncode != 0:
        if "nothing to commit" in result.stdout or "no changes added" in result.stdout:
            print("[INFO] No new images to commit (already up to date)")
        else:
            print(f"[ERROR] Git commit failed: {result.stderr}")
            return False
    else:
        print("[OK] Images committed")

    # Git push
    print("[Step 3/3] Pushing to GitHub...")
    print("This may take a while depending on your image sizes...")
    result = subprocess.run(['git', 'push', 'origin', 'main'],
                          capture_output=True, text=True)

    if result.returncode != 0:
        print(f"[ERROR] Git push failed: {result.stderr}")
        print("\nTroubleshooting:")
        print("1. Check if you have configured git credentials")
        print("2. Check if 'origin' remote points to your GitHub repo")
        print("3. Check your network connection")
        print("4. Try running manually: git push origin main")
        return False
    else:
        print("[OK] Images pushed to GitHub successfully!")

    return True

def generate_image_urls():
    """生成图片URL"""
    images_dir = "assets/images"
    urls = []
    image_files = []

    for filename in os.listdir(images_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            image_files.append(filename)

    image_files.sort()

    print("\n" + "="*70)
    print(" Generated Image URLs:")
    print("="*70)

    for i, filename in enumerate(image_files, 1):
        encoded_filename = urllib.parse.quote(filename)
        url = f"https://raw.githubusercontent.com/gds910228/dailynew/main/assets/images/{encoded_filename}"
        urls.append(url)
        print(f"\n{i}. {filename}")
        print(f"   {url}")

    print("\n" + "="*70)
    return urls

def create_temp_admin_html(urls):
    """创建临时的admin HTML文件，URL已经预填充"""
    admin_template_path = "admin/index.html"
    temp_admin_path = "admin/index_temp.html"

    if not os.path.exists(admin_template_path):
        return None

    with open(admin_template_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    urls_escaped = '\\n'.join(urls)

    inject_script = f'''
    <script>
    window.__PRELOAD_URLS__ = `{urls_escaped}`;
    console.log('✅ URLs pre-loaded:', {len(urls)}, 'URLs');
    </script>
    ''' + '''
    <script src="config.local.js" onerror="this.src='config.js'"></script>
    <script src="app.js"></script>
    <script>
    window.addEventListener('load', function() {
        if (window.__PRELOAD_URLS__) {
            setTimeout(function() {
                const textarea = document.getElementById('imageUrl');
                if (textarea && !textarea.value) {
                    textarea.value = window.__PRELOAD_URLS__;
                    textarea.dispatchEvent(new Event('input', { bubbles: true }));
                    console.log('✅ URLs auto-filled to textarea');

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
            }, 100);
        }
    });
    </script>
    </head>'''

    html_content = html_content.replace('</head>', inject_script)

    import re
    pattern = r'<script>\s*// 优先加载本地配置文件.*?</script>'
    html_content = re.sub(pattern, '', html_content, flags=re.DOTALL)

    with open(temp_admin_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return temp_admin_path

def main():
    print("\n" + "="*70)
    print(" 一键发布工具 - 完整流程")
    print("="*70)
    print("\n功能：")
    print("1. 上传图片到GitHub (git push)")
    print("2. 生成图片URL")
    print("3. 打开后台管理（URL自动填充）")

    # 检查git
    if not check_git():
        print("\n[ERROR] Git not installed or not in PATH")
        print("Please install Git from: https://git-scm.com/downloads")
        input("\nPress Enter to exit...")
        return

    # 询问是否继续
    print("\n" + "="*70)
    choice = input("\nContinue? (y/n): ").lower().strip()

    if choice != 'y':
        print("\n[INFO] Cancelled by user")
        return

    # Step 1: 上传图片
    print("\n" + "="*70)
    print(" Step 1: Uploading Images to GitHub")
    print("="*70)

    if not upload_images_to_github():
        print("\n[WARNING] Image upload failed or skipped")
        print("You can still generate URLs and continue...")
        choice2 = input("\nContinue anyway? (y/n): ").lower().strip()
        if choice2 != 'y':
            return

    # Step 2: 生成URL
    print("\n" + "="*70)
    print(" Step 2: Generating Image URLs")
    print("="*70)

    urls = generate_image_urls()

    if not urls:
        print("\n[ERROR] No images found")
        input("Press Enter to exit...")
        return

    # Step 3: 打开后台管理
    print("\n" + "="*70)
    print(" Step 3: Opening Web Admin")
    print("="*70)

    choice3 = input("\nOpen Web Admin with URLs pre-filled? (y/n): ").lower().strip()

    if choice3 == 'y':
        temp_file = create_temp_admin_html(urls)

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
        else:
            print(f"\n[ERROR] Failed to create temp admin file")

    # 总结
    print("\n" + "="*70)
    print(" Summary")
    print("="*70)
    print("\n✅ Images uploaded to GitHub")
    print("✅ Image URLs generated")
    print("✅ Web Admin opened (if you chose to)")

    print("\nNext steps:")
    print("1. In the opened Web Admin:")
    print("   - Image URLs are already filled")
    print("   - Date is set to today")
    print("2. Fill in:")
    print("   - Article title *")
    print("   - Article description *")
    print("   - Other optional fields")
    print("3. Click 'Submit' to save to data/articles.json")
    print("4. Refresh mini-program to view")

    print("\n" + "="*70)
    print("Done! 🎉\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] Cancelled by user")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")

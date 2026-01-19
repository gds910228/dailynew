#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用GitHub API直接上传图片到仓库
不依赖git push，绕过网络限制
"""

import os
import base64
import json
import urllib.parse

def load_config():
    """加载配置"""
    config_file = "admin/config.local.js"
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 使用简单的正则提取配置
        import re
        token_match = re.search(r"githubToken:\s*['\"]([^'\"]+)['\"]", content)
        owner_match = re.search(r"githubOwner:\s*['\"]([^'\"]+)['\"]", content)
        repo_match = re.search(r"githubRepo:\s*['\"]([^'\"]+)['\"]", content)
        branch_match = re.search(r"branch:\s*['\"]([^'\"]+)['\"]", content)

        return {
            'token': token_match.group(1) if token_match else '',
            'owner': owner_match.group(1) if owner_match else '',
            'repo': repo_match.group(1) if repo_match else '',
            'branch': branch_match.group(1) if branch_match else 'main'
        }
    except Exception as e:
        print(f"错误：无法加载配置 - {e}")
        return None

def check_file_exists(config, file_path):
    """检查文件是否已存在"""
    import urllib.request

    url = f"https://api.github.com/repos/{config['owner']}/{config['repo']}/contents/{file_path}?ref={config['branch']}"

    request = urllib.request.Request(url)
    request.add_header('Authorization', f"token {config['token']}")
    request.add_header('User-Agent', 'Python-Script')

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                return True, data.get('sha')
        return False, None
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False, None
        raise
    except Exception as e:
        print(f"检查文件失败: {e}")
        return False, None

def upload_file_to_github(config, file_path, commit_message="Upload file"):
    """上传文件到GitHub"""
    import urllib.request

    # 读取文件内容
    with open(file_path, 'rb') as f:
        content = f.read()

    # Base64编码
    content_b64 = base64.b64encode(content).decode('utf-8')

    # 构造API URL
    rel_path = file_path.replace('\\', '/')
    url = f"https://api.github.com/repos/{config['owner']}/{config['repo']}/contents/{rel_path}"

    # 检查文件是否已存在
    exists, sha = check_file_exists(config, rel_path)

    # 构造请求数据
    data = {
        'message': commit_message,
        'content': content_b64,
        'branch': config['branch']
    }

    if exists:
        data['sha'] = sha
        print(f"  更新已存在的文件")
    else:
        print(f"  上传新文件")

    request = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'))
    request.add_header('Authorization', f"token {config['token']}")
    request.add_header('Content-Type', 'application/json')
    request.add_header('User-Agent', 'Python-Script')

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode())
            if response.status == 200 or response.status == 201:
                return True, result
            return False, result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        try:
            error_data = json.loads(error_body)
            return False, error_data
        except:
            return False, {'message': error_body}
    except Exception as e:
        return False, {'message': str(e)}

def upload_images_directory():
    """上传assets/images目录下的所有图片"""
    print("\n" + "="*70)
    print("使用GitHub API上传图片")
    print("="*70)

    # 加载配置
    print("\n[步骤1] 加载配置...")
    config = load_config()
    if not config:
        print("❌ 无法加载配置文件")
        return False

    if not config['token']:
        print("❌ GitHub Token未配置")
        print("请编辑 admin/config.local.js 设置 githubToken")
        return False

    print(f"✅ 配置加载成功")
    print(f"   仓库: {config['owner']}/{config['repo']}")
    print(f"   分支: {config['branch']}")

    # 检查目录
    images_dir = "assets/images"
    if not os.path.exists(images_dir):
        print(f"\n❌ 目录不存在: {images_dir}")
        return False

    # 获取所有图片文件
    images = []
    for filename in os.listdir(images_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            images.append(filename)

    if not images:
        print(f"\n❌ 未找到图片文件")
        return False

    print(f"\n[步骤2] 找到 {len(images)} 个图片文件")

    # 上传文件
    print(f"\n[步骤3] 开始上传...")
    success_count = 0
    failed_files = []

    for i, filename in enumerate(images, 1):
        file_path = os.path.join(images_dir, filename)
        print(f"\n[{i}/{len(images)}] 上传: {filename}")

        success, result = upload_file_to_github(
            config,
            file_path,
            f"Upload image: {filename}"
        )

        if success:
            success_count += 1
            print(f"  ✅ 成功")
        else:
            failed_files.append(filename)
            error_msg = result.get('message', '未知错误')
            print(f"  ❌ 失败: {error_msg}")

    # 总结
    print("\n" + "="*70)
    print("上传结果")
    print("="*70)
    print(f"\n成功: {success_count}/{len(images)}")

    if failed_files:
        print(f"\n失败的文件:")
        for f in failed_files:
            print(f"  - {f}")

    if success_count > 0:
        print(f"\n✅ 图片已上传到GitHub")
        print(f"   查看地址: https://github.com/{config['owner']}/{config['repo']}/tree/{config['branch']}/assets/images")
        return True
    else:
        print(f"\n❌ 所有文件上传失败")
        return False

def main():
    try:
        success = upload_images_directory()

        if success:
            print("\n" + "="*70)
            print("下一步:")
            print("="*70)
            print("\n运行 generate-urls-v2.bat")
            print("选择 'n' 跳过git上传（因为已通过API上传）")
            print("\n")

        input("按回车退出...")

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        input("按回车退出...")

if __name__ == '__main__':
    main()

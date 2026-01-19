#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""诊断GitHub连接问题"""

import subprocess
import socket
import sys

print("="*70)
print("GitHub连接诊断工具")
print("="*70)

# 1. 检查网络连接
print("\n[检查1] 测试网络连接...")
try:
    socket.create_connection(("github.com", 443), timeout=5)
    print("✅ 可以连接到 github.com:443")
except socket.timeout:
    print("❌ 无法连接到 github.com:443 (超时)")
    print("   原因：可能被防火墙阻止或需要代理")
except Exception as e:
    print(f"❌ 连接失败: {e}")

# 2. 检查git配置
print("\n[检查2] Git远程配置...")
try:
    result = subprocess.run(['git', 'remote', '-v'],
                          capture_output=True, text=True, check=True)
    print("当前Git远程仓库:")
    print(result.stdout)
except:
    print("❌ 无法获取git配置")

# 3. 检查是否配置了代理
print("\n[检查3] Git代理配置...")
try:
    result = subprocess.run(['git', 'config', '--global', '--get', 'http.proxy'],
                          capture_output=True, text=True)
    if result.stdout.strip():
        print(f"HTTP代理: {result.stdout.strip()}")
    else:
        print("HTTP代理: 未配置")

    result = subprocess.run(['git', 'config', '--global', '--get', 'https.proxy'],
                          capture_output=True, text=True)
    if result.stdout.strip():
        print(f"HTTPS代理: {result.stdout.strip()}")
    else:
        print("HTTPS代理: 未配置")
except:
    print("无法检查代理配置")

# 4. ping测试
print("\n[检查4] Ping测试...")
try:
    if sys.platform == 'win32':
        result = subprocess.run(['ping', '-n', '2', 'github.com'],
                              capture_output=True, text=True, timeout=10)
    else:
        result = subprocess.run(['ping', '-c', '2', 'github.com'],
                              capture_output=True, text=True, timeout=10)

    if "TTL" in result.stdout or "ttl=" in result.stdout:
        print("✅ Ping github.com 成功")
    else:
        print("⚠️ Ping github.com 可能失败")
except:
    print("❌ Ping测试失败")

print("\n" + "="*70)
print("解决方案")
print("="*70)

print("""
问题：无法连接到GitHub (port 443)

可能原因：
1. 网络防火墙阻止
2. 需要使用代理/VPN
3. DNS解析问题

解决方案：
""")

solutions = [
    {
        "name": "方案1：使用代理（如果你有VPN/代理）",
        "steps": [
            "1. 找到你的代理地址和端口，例如：127.0.0.1:7890",
            "2. 运行命令设置git代理:",
            "   git config --global http.proxy http://127.0.0.1:7890",
            "   git config --global https.proxy http://127.0.0.1:7890",
            "3. 然后重试上传",
            "4. 如果以后不需要代理，取消:",
            "   git config --global --unset http.proxy",
            "   git config --global --unset https.proxy"
        ]
    },
    {
        "name": "方案2：使用SSH代替HTTPS",
        "steps": [
            "1. 生成SSH密钥（如果还没有）:",
            "   ssh-keygen -t rsa -C \"your_email@example.com\"",
            "2. 复制公钥到GitHub:",
            "   - 打开 C:\\Users\\你的用户名\\.ssh\\id_rsa.pub",
            "   - 复制全部内容",
            "   - GitHub -> Settings -> SSH keys -> New SSH key",
            "3. 修改git远程地址:",
            "   git remote set-url origin git@github.com:gds910228/dailynew.git",
            "4. 重试上传"
        ]
    },
    {
        "name": "方案3：手动上传图片（最简单）",
        "steps": [
            "1. 访问 https://github.com/gds910228/dailynew",
            "2. 进入 assets/images/ 目录",
            "3. 点击 \"Upload files\"",
            "4. 拖拽图片文件上传",
            "5. 填写commit信息，点击 Commit changes",
            "6. 然后运行 generate-urls-v2.bat（选择n跳过上传）"
        ]
    },
    {
        "name": "方案4：检查防火墙/杀毒软件",
        "steps": [
            "1. 临时关闭防火墙",
            "2. 检查杀毒软件是否阻止git",
            "3. 检查公司网络是否限制GitHub访问",
            "4. 尝试使用手机热点测试"
        ]
    }
]

for i, solution in enumerate(solutions, 1):
    print(f"\n{'='*70}")
    print(solution['name'])
    print('='*70)
    for step in solution['steps']:
        print(step)

print("\n" + "="*70)
print("推荐：先试方案3（手动上传），最简单直接")
print("="*70)

input("\n按回车退出...")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查GitHub配置"""

print("="*70)
print("GitHub配置检查")
print("="*70)

# 读取config.local.js
config_file = "admin/config.local.js"
try:
    with open(config_file, 'r', encoding='utf-8') as f:
        content = f.read()

    print("\n✅ 找到配置文件:", config_file)

    # 检查Token
    import re
    token_match = re.search(r"githubToken:\s*['\"]([^'\"]+)['\"]", content)
    if token_match:
        token = token_match.group(1)
        print(f"\n📋 GitHub Token: {token[:10]}...{token[-4:]}")

        # 检查是否是默认/示例Token
        if token == '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' or len(token) < 10:
            print("\n❌ 问题：Token可能是示例Token或已过期！")
            print("\n🔧 解决方法：")
            print("1. 访问：https://github.com/settings/tokens")
            print("2. 点击 'Generate new token (classic)'")
            print("3. 勾选 'repo' 权限")
            print("4. 生成Token并复制")
            print("5. 编辑 admin/config.local.js，更新 githubToken 的值")
        else:
            print("\n✅ Token看起来有效")
    else:
        print("\n❌ 未找到githubToken配置")

    # 检查仓库信息
    owner_match = re.search(r"githubOwner:\s*['\"]([^'\"]+)['\"]", content)
    repo_match = re.search(r"githubRepo:\s*['\"]([^'\"]+)['\"]", content)

    if owner_match and repo_match:
        owner = owner_match.group(1)
        repo = repo_match.group(1)
        print(f"\n📋 GitHub仓库: {owner}/{repo}")

except FileNotFoundError:
    print(f"\n❌ 配置文件不存在: {config_file}")
    print("请确保文件存在并已正确配置")

except Exception as e:
    print(f"\n❌ 错误: {e}")

print("\n" + "="*70)
print("其他问题诊断")
print("="*70)

print("\n如果点击提交按钮没反应，请检查：")
print("1. 打开浏览器开发者工具（F12）")
print("2. 切换到 Console 标签")
print("3. 点击提交按钮")
print("4. 查看是否有错误信息")
print("\n常见错误：")
print("- '请先在 config.local.js 中配置 GitHub Token' -> 需要更新Token")
print("- '请先在 config.local.js 中配置 GitHub 用户名' -> 需要配置用户名")
print("- Network error -> 检查网络连接")

print("\n" + "="*70)
input("按回车退出...")

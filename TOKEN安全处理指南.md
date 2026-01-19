# 🚨 GitHub Token泄露处理指南

## ⚠️ 重要提醒

你的GitHub Token已经在代码仓库中暴露！必须立即按照以下步骤处理。

---

## ✅ 已完成的修复措施

1. ✅ 创建了 `admin/config.local.js` 作为安全的配置文件（已加入.gitignore）
2. ✅ 清空了 `admin/config.js` 中的Token
3. ✅ 更新了 `.gitignore` 防止再次提交config.js
4. ✅ 修改了 `admin/index.html` 优先加载本地配置

---

## 🚨 必须立即执行的步骤

### 第1步：撤销泄露的Token（最重要！）

1. 访问：https://github.com/settings/tokens
2. 找到名为Token（或者查看token的最后几位：`...32HoEBq`）
3. 点击 **Delete** 或 **Revoke** 删除它
4. 确认删除

**⚠️ 不要跳过这一步！Token已经暴露，必须撤销！**

### 第2步：生成新的Token

1. 访问：https://github.com/settings/tokens/new
2. 设置Token名称：例如 `dailynew-admin-token`
3. 选择权限（Scopes）：
   - ✅ **repo** （完整的仓库控制权限）
4. 点击 **Generate token**
5. **立即复制Token**（只显示一次！）
6. 保存到安全的地方

### 第3步：配置新的Token到本地文件

编辑 `admin/config.local.js` 文件：

```javascript
const CONFIG = {
    // 将下面的YOUR_GITHUB_TOKEN_HERE替换为你的新Token
    githubToken: 'ghp_你的新Token粘贴到这里',

    // 其他配置保持不变...
    githubOwner: 'gds910228',
    githubRepo: 'dailynew',
    branch: 'main',
    dataFilePath: 'data/articles.json',
};
```

**保存文件！**

### 第4步：清理Git历史记录（可选但推荐）

由于config.js已经被提交到Git，需要从历史记录中彻底删除：

#### 方法1：使用git filter-repo（推荐）

```bash
# 安装git-filter-repo（如果还没有）
pip install git-filter-repo

# 从历史记录中删除config.js中的敏感信息
git filter-repo --invert-paths --path admin/config.js

# 强制推送到远程仓库（⚠️ 谨慎操作！）
git push origin --force --all
git push origin --force --tags
```

#### 方法2：使用BFG Repo-Cleaner

```bash
# 下载BFG: https://rtyley.github.io/bfg-repo-cleaner/

# 清理config.js中的敏感内容
bfg --replace-text passwords.txt

# passwords.txt内容格式：
# ghlp_[a-zA-Z0-9]{36}==>

# 然后运行
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push origin --force --all
```

#### 方法3：创建新的干净仓库（最简单）

```bash
# 1. 本地创建一个干净的分支
git checkout --orphan clean_branch
git add -A
git commit -m "Initial clean commit"

# 2. 删除原main分支并重命名
git branch -D main
git branch -m main

# 3. 删除GitHub上的旧仓库
# 访问：https://github.com/gds910228/dailynew/settings
# 点击"Delete this repository"

# 4. 创建同名新仓库
# 访问：https://github.com/new
# 仓库名：dailynew
# 设为Public

# 5. 推送新代码
git remote remove origin
git remote add origin https://github.com/gds910228/dailynew.git
git push -u origin main
```

**⚠️ 注意：这会丢失所有提交历史，但最安全！**

### 第5步：验证修复

1. 打开 Web管理后台：双击 `admin/index.html`
2. 打开浏览器开发者工具（F12）
3. 切换到Console标签
4. 查看是否有配置错误提示
5. 测试提交一篇文章，确认Token工作正常

---

## 🔒 安全最佳实践

### ✅ 正确做法

- ✅ 使用 `config.local.js` 存储敏感信息（已在.gitignore中）
- ✅ 从不提交Token到Git仓库
- ✅ Token只在本地开发环境使用
- ✅ 定期更换Token（建议每3个月）
- ✅ 使用最小权限原则（只给必要的权限）

### ❌ 错误做法

- ❌ 将Token硬编码在代码中
- ❌ 将Token提交到Git仓库
- ❌ 在公开仓库中包含任何凭证
- ❌ Token权限过大（不要给admin权限）
- ❌ Token长期不更换

---

## 📊 当前配置文件说明

| 文件 | 是否提交到Git | 用途 | 安全性 |
|------|--------------|------|--------|
| `admin/config.local.js` | ❌ 否（.gitignore） | 存储真实Token和配置 | ✅ 安全 |
| `admin/config.js` | ❌ 否（.gitignore） | 模板文件，不包含真实Token | ✅ 安全 |
| `.gitignore` | ✅ 是 | 告诉Git哪些文件不提交 | ✅ 安全 |

---

## 🤔 如果将来需要部署到生产环境

当前架构只适合**个人使用**或**团队内部使用**，因为：

1. Web管理后台运行在浏览器中
2. Token存储在本地配置文件中
3. 每个使用者都需要自己的Token

**如果需要多用户协作或公开发布，需要：**

### 方案1：使用后端服务器（推荐）

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│  任何用户   │ ──────▶ │  你的后端API  │ ──────▶ │  GitHub API  │
│  (无Token)  │         │  (持有Token)  │         │             │
└─────────────┘         └──────────────┘         └─────────────┘
```

**免费后端方案：**
- 腾讯云开发（微信小程序推荐）
- Vercel + Node.js
- Cloudflare Workers
- Netlify Functions

### 方案2：使用GitHub Actions

创建自动化工作流，无需Token在前端：
```yaml
# .github/workflows/update-data.yml
name: Update Articles
on:
  workflow_dispatch:
    inputs:
      title:
        required: true
      description:
        required: true
jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Update data
        run: |
          # 更新articles.json
          git config user.name "Bot"
          git config user.email "bot@example.com"
          git add data/articles.json
          git commit -m "Update articles"
          git push
```

---

## 📞 需要帮助？

如果遇到问题：

1. **Token不工作**：检查Token权限是否包含`repo`
2. **提交失败**：检查网络连接和GitHub服务状态
3. **Git清理失败**：考虑使用方法3（创建新仓库）
4. **其他问题**：查看项目README.md或提Issue

---

## ✅ 完成检查清单

完成以下所有项后才算是彻底解决：

- [ ] 已撤销旧的Token
- [ ] 已生成新的Token
- [ ] 已将新Token配置到 `admin/config.local.js`
- [ ] 已从Git历史中删除敏感信息（或创建新仓库）
- [ ] 已测试Web管理后台能正常提交文章
- [ ] 已确认 `.gitignore` 包含 `admin/config.js` 和 `admin/config.local.js`
- [ ] 小程序端数据加载正常（不需要Token）

---

**最后提醒：** 永远不要将任何Token、密码、密钥等敏感信息提交到Git仓库！

生成时间：2026-01-19

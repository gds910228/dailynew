# 每日新知识汇 - 部署说明

## 项目概述

这是一个基于微信小程序的财经资讯整理工具，使用GitHub作为数据源，完全免费，无需服务器。

**架构特点：**
- ✅ 完全免费（GitHub托管 + 免费图床）
- ✅ 无需服务器和云数据库
- ✅ 每日更新无需审核
- ✅ 支持Web后台管理

---

## 📋 前置准备

### 1. GitHub仓库准备
1. 登录GitHub，创建新仓库（例如：`dailynew`）
2. 将本项目代码推送到该仓库
3. 将`data`目录中的文件提交到仓库

### 2. 获取GitHub Token
1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 勾选权限：
   - `repo` (Full control of private repositories)
4. 生成并复制Token（**只显示一次，请妥善保存**）

### 3. 获取免费图床Token（可选）
如果使用图片上传功能：
1. 访问 https://sm.ms/home/apitoken
2. 注册并获取API Token
3. 复制Token

---

## 🚀 部署步骤

### 步骤1：配置小程序API

打开 `utils/api.js`，修改GitHub数据源URL：

```javascript
const CONFIG = {
  // 替换为你的实际GitHub地址
  dataUrl: 'https://raw.githubusercontent.com/你的用户名/dailynew/main/data/articles.json'
};
```

**测试数据源：**
在浏览器访问上述URL，确保能看到JSON数据。

---

### 步骤2：配置Web管理后台

打开 `admin/config.js`，填写配置：

```javascript
const CONFIG = {
  // GitHub Token（从步骤2获取）
  githubToken: 'ghp_xxxxxxxxxxxxxxxxxxxx',

  // GitHub仓库信息
  githubOwner: '你的GitHub用户名',
  githubRepo: 'dailynew',      // 仓库名
  branch: 'main',              // 分支名

  // 数据文件路径（通常不需要改）
  dataFilePath: 'data/articles.json',

  // 图床Token（可选）
  imageHostToken: '你的SM.MS Token'
};
```

---

### 步骤3：准备图标资源

在小程序中创建图标目录和图标：

```bash
mkdir -p assets/icons
```

**需要的图标文件（建议尺寸 64x64 px）：**
```
assets/icons/
├── home.png           # 首页图标（tabbar未选中）
├── home-active.png    # 首页图标（tabbar选中）
├── profile.png        # 我的图标（tabbar未选中）
├── profile-active.png # 我的图标（tabbar选中）
├── search.png         # 搜索图标
├── close.png          # 关闭/清除图标
├── download.png       # 下载图标
├── heart.png          # 收藏图标（未收藏）
├── heart-active.png   # 收藏图标（已收藏）
├── share.png          # 分享图标
├── video.png          # 视频图标
├── empty.png          # 空状态图标
├── empty-favorite.png # 空收藏图标
├── empty-history.png  # 空历史图标
├── delete.png         # 删除图标
└── app-icon.png       # 应用图标
```

**图标资源获取：**
- 推荐：https://www.iconfont.cn/
- 或使用：https://fontawesome.com/
- 下载PNG格式，重命名为上述文件名

---

### 步骤4：微信小程序配置

#### 4.1 创建小程序
1. 登录 [微信公众平台](https://mp.weixin.qq.com/)
2. 注册小程序（个体工商户主体）
3. 完善小程序信息

#### 4.2 配置小程序信息
在微信公众平台填写：
- **小程序名称**：每日新知识汇
- **小程序简介**：每日整理前沿财经资讯，以图文形式分享行业动态与核心观点
- **小程序类目**：工具 > 信息查询
- **服务类目**：科技 > 软件服务提供商

#### 4.3 配置项目
打开微信开发者工具：
1. 导入项目（选择`dailynew`目录）
2. 填写AppID（在微信公众平台获取）
3. 修改`project.config.json`中的`appid`

#### 4.4 开通域名白名单
在微信公众平台：
1. 进入"开发" → "开发管理" → "开发设置"
2. 在"服务器域名"中添加：
   ```
   request合法域名：
   https://raw.githubusercontent.com
   https://api.github.com
   https://sm.ms
   ```

---

### 步骤5：测试小程序

1. 在微信开发者工具中点击"编译"
2. 测试首页加载（确保能看到示例文章）
3. 测试详情页、收藏、下载等功能
4. 在真机上测试图片下载功能

---

## 📝 日常使用流程

### 方式1：使用Web后台（推荐）

1. **部署Web后台**
   ```bash
   cd admin
   # 使用任意静态服务器，例如：
   python -m http.server 8000
   ```
   或使用 VSCode 的 Live Server 插件

2. **访问管理后台**
   - 打开浏览器访问：http://localhost:8000
   - 填写表单添加新文章
   - 点击"提交文章"按钮
   - 系统会自动提交到GitHub

3. **小程序更新**
   - 用户下拉刷新即可看到新内容
   - 无需重新审核！

### 方式2：手动编辑JSON

1. 访问GitHub仓库
2. 编辑 `data/articles.json` 文件
3. 添加新文章数据（参考现有格式）
4. 提交更改
5. 小程序下拉刷新获取最新数据

---

## 🔧 故障排查

### 问题1：小程序无法加载数据
**原因**：域名未白名单
**解决**：在微信公众平台添加 `raw.githubusercontent.com` 到request合法域名

### 问题2：Web后台提交失败
**原因**：GitHub Token无效或权限不足
**解决**：
1. 检查Token是否正确复制
2. 确保Token有`repo`权限
3. 检查用户名和仓库名是否正确

### 问题3：图片上传失败
**原因**：图床Token无效或图片过大
**解决**：
1. 检查SM.MS Token是否有效
2. 确保图片小于5MB
3. 或直接使用图片URL字段

### 问题4：小程序审核被拒
**原因**：包含金融敏感词
**解决**：
1. 检查内容中是否包含"股票""投资""证券"等词汇
2. 检查小程序名称、描述是否合规
3. 确保类目选择"工具-信息查询"

---

## 📊 数据结构说明

### articles.json 格式
```json
{
  "meta": {
    "version": "1.0.0",
    "lastUpdate": "2025-01-18",
    "totalCount": 10
  },
  "categories": ["半导体", "AI硬件", "存储芯片"],
  "articles": [
    {
      "id": "20250118001",
      "title": "文章标题",
      "description": "文章简述",
      "imageUrl": "https://example.com/image.jpg",
      "thumbnailUrl": "https://example.com/thumb.jpg",
      "tags": ["半导体", "AI"],
      "category": "半导体",
      "publishDate": "2025-01-18",
      "videoId": "",
      "author": "每日新知识汇",
      "viewCount": 0,
      "downloadCount": 0,
      "favoriteCount": 0
    }
  ]
}
```

---

## 💡 成本说明

| 项目 | 费用 | 说明 |
|------|------|------|
| GitHub仓库 | 免费 | 公开仓库完全免费 |
| 图床（SM.MS） | 免费 | 每月5GB流量 |
| 微信小程序 | 免费 | 认证费30元/年（个体户） |
| Web后台托管 | 免费 | 本地运行或GitHub Pages |
| **总计** | **30元/年** | 仅微信认证费用 |

---

## 📈 扩展功能建议

### 1. 自动发布到GitHub Pages
将Web后台部署到GitHub Pages，实现云端管理：
```bash
cd admin
# 初始化Git仓库
git init
git add .
git commit -m "Initial commit"
git push origin main
# 在GitHub设置中启用GitHub Pages
```

### 2. 添加评论功能
使用微信云开发的云数据库实现评论功能（需小额费用）

### 3. 数据统计
集成微信统计或自建统计系统

---

## 📞 技术支持

如遇到问题，请检查：
1. GitHub Token是否有效
2. 域名是否已白名单
3. 网络连接是否正常
4. JSON格式是否正确

---

**祝您使用愉快！**

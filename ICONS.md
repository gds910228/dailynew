# 图标资源说明

本项目需要以下图标文件，请将它们放在 `assets/icons/` 目录下。

## 📋 所需图标列表

### TabBar 图标（必需）
| 文件名 | 尺寸 | 说明 | 推荐颜色 |
|--------|------|------|---------|
| home.png | 81x81 px | 首页图标（未选中） | 灰色 #666 |
| home-active.png | 81x81 px | 首页图标（选中） | 紫色 #667eea |
| profile.png | 81x81 px | 我的图标（未选中） | 灰色 #666 |
| profile-active.png | 81x81 px | 我的图标（选中） | 紫色 #667eea |

### 功能图标（必需）
| 文件名 | 尺寸 | 说明 |
|--------|------|------|
| search.png | 32x32 px | 搜索图标 |
| close.png | 32x32 px | 关闭/清除图标 |
| download.png | 32x32 px | 下载图标 |
| heart.png | 32x32 px | 收藏图标（未收藏） |
| heart-active.png | 32x32 px | 收藏图标（已收藏） |
| share.png | 32x32 px | 分享图标 |
| video.png | 32x32 px | 视频图标 |

### 状态图标（必需）
| 文件名 | 尺寸 | 说明 |
|--------|------|------|
| empty.png | 200x200 px | 空状态图标 |
| empty-favorite.png | 160x160 px | 空收藏图标 |
| empty-history.png | 160x160 px | 空历史图标 |
| delete.png | 32x32 px | 删除图标 |

### 应用图标（必需）
| 文件名 | 尺寸 | 说明 |
|--------|------|------|
| app-icon.png | 120x120 px | 应用图标 |

## 🎨 图标资源获取方式

### 方式1：图标字体库（推荐）
- **iconfont**：https://www.iconfont.cn/
  - 搜索关键词：home, user, search, download, heart等
  - 下载PNG格式
  - 选择合适尺寸（2x或3x）

- **Font Awesome**：https://fontawesome.com/
  - 下载免费版本
  - 导出PNG格式

### 方式2：在线设计工具
- **Canva**：https://www.canva.com/
- **Figma**：https://www.figma.com/

### 方式3：AI生成
使用AI图像生成工具创建统一风格的图标

## 📥 快速开始

### 步骤1：创建图标目录
```bash
mkdir -p assets/icons
```

### 步骤2：下载图标
访问 iconfont.cn，搜索并下载以下图标：
- 首页：home
- 我的：user
- 搜索：search
- 下载：download
- 收藏：heart
- 分享：share
- 视频：play-circle
- 关闭：close
- 删除：delete

### 步骤3：重命名和调整
1. 将图标重命名为上述文件名
2. 确保背景透明（PNG格式）
3. 统一颜色（灰色和紫色）

## 🎯 图标设计建议

### 配色方案
- 未选中状态：`#999999` 或 `#666666`
- 选中状态：`#667eea`（主题紫色）
- 白色图标用于深色背景

### 风格统一
- 使用线性图标（Line Icons）
- 线条粗细一致（2-3px）
- 圆角风格（更友好）

## 💡 临时方案

如果暂时没有图标，可以使用纯色方块代替：

```javascript
// 在代码中临时使用背景色代替图标
.icon {
  background: #667eea;
  width: 32px;
  height: 32px;
  border-radius: 4px;
}
```

或使用纯色占位图：

```bash
# 使用在线占位图服务
https://via.placeholder.com/64
```

## ✅ 检查清单

在运行小程序前，确保以下图标已准备：

- [ ] home.png
- [ ] home-active.png
- [ ] profile.png
- [ ] profile-active.png
- [ ] search.png
- [ ] close.png
- [ ] download.png
- [ ] heart.png
- [ ] heart-active.png
- [ ] share.png
- [ ] video.png
- [ ] empty.png
- [ ] empty-favorite.png
- [ ] empty-history.png
- [ ] delete.png
- [ ] app-icon.png

---

**提示**：所有图标必须是PNG格式，建议使用透明背景。

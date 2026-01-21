# 每日新知识汇 - 图标设计说明

## 📱 图标文件列表

### 1. **app-icon-new.svg** - 书本日历风格（推荐）
- **设计理念**：打开的书本 + 日期标记，象征"每日知识"
- **配色**：深黑背景 + 电光蓝强调色
- **风格**：杂志编辑风格，简约现代
- **适用场景**：主要推荐，完美匹配整体设计

### 2. **app-icon-v2.svg** - 知识灯泡风格
- **设计理念**：灯泡（灵感）+ 书本（知识），强调知识带来的启发
- **配色**：渐变深黑背景 + 电光蓝
- **风格**：创意、现代、科技感
- **适用场景**：适合突出"创新"和"智慧"定位

### 3. **app-icon-v3.svg** - 杂志封面风格
- **设计理念**：模拟杂志封面排版，标题+装饰+徽章
- **配色**：白色背景 + 黑色文字 + 蓝色点缀
- **风格**：复古杂志感、经典、优雅
- **适用场景**：适合强调"媒体"和"资讯"属性

### 4. **app-icon-minimal.svg** - 极简几何风格
- **设计理念**：3D书本立体效果 + 中心强调点
- **配色**：纯黑+纯白+电光蓝
- **风格**：极简、现代、几何美学
- **适用场景**：适合追求极简和高级感

---

## 🎨 使用指南

### 方案一：直接使用 SVG（推荐用于开发调试）
微信小程序支持 SVG 图标，但建议转换为 PNG 以获得最佳兼容性。

### 方案二：转换为 PNG（推荐用于生产环境）

#### 方法 A：使用在线工具（最简单）
1. 访问 https://convertio.co/zh/svg-png/ 或 https://cloudconvert.com/svg-to-png
2. 上传 SVG 文件
3. 设置尺寸：
   - **小程序图标**：144×144px 或 512×512px
   - **Tab 图标**：81×81px
4. 下载 PNG 文件

#### 方法 B：使用命令行工具
```bash
# 安装 ImageMagick（如果未安装）
# Windows: choco install imagemagick
# Mac: brew install imagemagick

# 转换为 144x144 PNG
magick convert -background none -resize 144x144 app-icon-new.svg app-icon-144.png

# 转换为 512x512 PNG（高清版本）
magick convert -background none -resize 512x512 app-icon-new.svg app-icon-512.png

# 转换为 81x81 PNG（Tab 图标）
magick convert -background none -resize 81x81 app-icon-new.svg tab-icon.png
```

#### 方法 C：使用 Figma/Sketch 等设计工具
1. 打开设计工具
2. 导入 SVG 文件
3. 导出为 PNG，设置所需尺寸

---

## 📐 尺寸规范参考

| 用途 | 尺寸 | 说明 |
|------|------|------|
| 小程序 Logo | 144×144px | 主体占 72%（约 104×104px）|
| Tab 图标 | 81×81px | 底部导航栏图标 |
| 分享图标 | 120×120px | 小于 10KB |
| 应用商店 | 512×512px | 高清版本 |
| favico | 16×16px, 32×32px | 网页图标 |

---

## 🎯 推荐使用方案

### 配置文件更新
将选中的图标（PNG 格式）放入对应位置：

```javascript
// project.config.json
{
  "appid": "your-appid",
  "projectname": "每日新知识汇",
  "iconPath": "assets/icons/app-icon-144.png" // 更新这里
}
```

### 页面头像更新
```xml
<!-- pages/profile/profile.wxml -->
<image class="avatar" src="/assets/icons/app-icon-144.png" mode="aspectFit"></image>
```

---

## 🎨 设计一致性

所有图标都遵循相同的设计系统：
- ✅ **主色**：电光蓝 #0066ff
- ✅ **背景**：深黑 #1a1a1a
- ✅ **风格**：杂志编辑风格
- ✅ **圆角**：44px（图标） / 16-24px（内部元素）

---

## 📝 注意事项

1. **文件大小控制**：
   - PNG 图标应控制在 50KB 以内
   - 整个小程序包不超过 2MB
   - 使用 TinyPNG（https://tinypng.com）压缩 PNG 文件

2. **视觉检查**：
   - 在手机实际效果预览
   - 检查白色和黑色背景下的显示效果
   - 确认图标在小尺寸下仍清晰可辨

3. **多尺寸准备**：
   - 建议准备 144px 和 512px 两个版本
   - 144px 用于小程序
   - 512px 用于其他推广材料

---

## 🚀 下一步

1. 选择一个最喜欢的图标设计
2. 转换为 PNG 格式（建议 144×144px）
3. 压缩图片文件（使用 TinyPNG）
4. 更新小程序配置
5. 提交审核

---

**设计时间**：2026-01-21
**设计风格**：杂志编辑风格（Editorial Magazine）
**设计师**：Claude Code

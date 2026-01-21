# 图标转换快速指南

## 🎯 你选择了：app-icon-v3（杂志封面风格）

### 方案 A：在线转换（最简单，5 分钟完成）⭐

#### 步骤 1：访问在线转换工具
推荐以下任一网站：
- https://convertio.co/zh/svg-png/ （支持中文）
- https://cloudconvert.com/svg-to-png
- https://www.aconvert.com/cn/image/svg-to-png/

#### 步骤 2：上传文件
- 上传：`app-icon-v3.svg`

#### 步骤 3：设置尺寸（按顺序转换）

**1️⃣ 小程序主图标（144×144px）**
- 宽度：144
- 高度：144
- 文件名：`app-icon-144.png`
- 下载后保存到 `assets/icons/`

**2️⃣ Tab 图标（81×81px）**
- 宽度：81
- 高度：81
- 文件名：`tab-icon.png`
- 下载后保存到 `assets/icons/`

**3️⃣ 高清版本（512×512px）**
- 宽度：512
- 高度：512
- 文件名：`app-icon-512.png`
- 下载后保存到 `assets/icons/`

#### 步骤 4：压缩图片（可选但推荐）
访问：https://tinypng.com/
- 上刚下载的 PNG 文件
- 下载压缩后的版本（可减小 50-70% 文件大小）

---

### 方案 B：使用命令行工具（开发者推荐）

#### Node.js 版本：
```bash
cd assets/icons
npm install sharp
node convert-icon.js
```

#### Python 版本：
```bash
cd assets/icons
pip install cairosvg
python convert-icon.py
```

---

### 方案 C：使用设计软件

#### Figma（免费）：
1. 创建新文件（200×200px）
2. 拖入 `app-icon-v3.svg`
3. 导出为 PNG，选择所需尺寸
4. 下载：https://figma.com

#### Sketch（Mac）：
1. 打开 Sketch
2. 导入 SVG
3. File > Export > 选择尺寸
4. 导出为 PNG

---

## ✅ 转换完成后的下一步

### 1. 替换图标文件

将转换好的 PNG 文件重命名并移动：

```bash
# 主图标
app-icon-v3-icon-144.png → app-icon.png

# Tab 图标（如果需要）
app-icon-v3-icon-81.png → tab-icon.png
```

### 2. 更新项目配置

在微信开发者工具中：
1. 打开 `project.config.json`
2. 找到 `iconPath` 字段
3. 更新为：`assets/icons/app-icon.png`

### 3. 查看效果
- 重新编译项目
- 查看 App 图标是否更新
- 在真机上预览效果

---

## 📐 尺寸对照表

| 文件名 | 尺寸 | 用途 | 文件大小限制 |
|--------|------|------|--------------|
| app-icon-144.png | 144×144px | 小程序主图标 | < 50KB |
| tab-icon.png | 81×81px | Tab 导航图标 | < 20KB |
| app-icon-512.png | 512×512px | 高清版本/宣传 | < 200KB |
| app-icon-120.png | 120×120px | 分享图标 | < 10KB |

---

## 🎨 设计亮点说明

**app-icon-v3（杂志封面风格）**

- ✅ **白色背景**：在深色导航栏中更突出
- ✅ **中文排版**："每日知识" 四个大字
- ✅ **红色"新"字徽章**：强调"每日更新"
- ✅ **书本图标**：直观表达知识属性
- ✅ **经典杂志感**：复古优雅，权威感强

---

## 💡 常见问题

**Q: 为什么推荐在线转换？**
A: 最简单快捷，不需要安装任何软件，5 分钟搞定。

**Q: 转换后的图片模糊怎么办？**
A: 使用 512×512px 的高清版本，或者在设计工具中导出时选择 2x/3x 倍率。

**Q: 文件太大怎么办？**
A: 使用 TinyPNG（https://tinypng.com）压缩，通常能减小 50-70%。

**Q: 需要透明背景吗？**
A: 小程序图标不需要透明背景，因为会显示在白色圆角框中。

---

## 🚀 现在开始

推荐使用 **方案 A（在线转换）**，最快 5 分钟完成！

步骤：
1. 打开 https://convertio.co/zh/svg-png/
2. 上传 `app-icon-v3.svg`
3. 设置 144×144px
4. 下载并保存

就这么简单！

# 数据文件说明

## 文件结构

```
data/
├── articles.json      # 文章数据主文件
└── README.md         # 本说明文档
```

## articles.json 数据结构

### meta 元数据
```json
{
  "meta": {
    "version": "1.0.0",        // 数据版本号
    "lastUpdate": "2025-01-18", // 最后更新日期
    "totalCount": 10            // 文章总数
  }
}
```

### categories 分类列表
所有可用的文章分类，用于筛选和标签。

### articles 文章列表
每篇文章包含以下字段：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 唯一标识，格式：YYYYMMDD + 序号 |
| title | string | 是 | 文章标题 |
| description | string | 是 | 文章简述（1-2句话） |
| imageUrl | string | 是 | 原图URL（用于详情页展示和下载） |
| thumbnailUrl | string | 是 | 缩略图URL（用于列表页展示） |
| tags | array | 是 | 标签数组，如["半导体", "AI"] |
| category | string | 是 | 分类，必须在categories列表中 |
| publishDate | string | 是 | 发布日期，格式：YYYY-MM-DD |
| videoId | string | 否 | 关联的视频号ID |
| author | string | 是 | 作者 |
| viewCount | number | 是 | 浏览次数 |
| downloadCount | number | 是 | 下载次数 |
| favoriteCount | number | 是 | 收藏次数 |

## 使用方式

### 方式1：手动编辑
1. 直接编辑 `articles.json` 文件
2. 提交到GitHub仓库
3. 小程序会自动获取最新数据

### 方式2：使用Web管理后台（推荐）
1. 访问管理后台网页
2. 填写表单添加新文章
3. 自动提交到GitHub

## 注意事项

1. **图片URL**：建议使用免费图床（如SM.MS、imgbb）或GitHub仓库作为CDN
2. **ID唯一性**：确保每篇文章的ID唯一
3. **日期格式**：统一使用 YYYY-MM-DD 格式
4. **标签规范**：使用中性标签，避免"股票""证券"等敏感词
5. **备份数据**：定期备份JSON文件

## GitHub部署

将整个 `data` 目录推送到GitHub仓库后，获取原始数据URL：

```
https://raw.githubusercontent.com/[用户名]/[仓库名]/main/data/articles.json
```

小程序将通过此URL获取数据。

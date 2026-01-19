// API配置
const CONFIG = {
  // GitHub数据源URL（请替换为你的实际地址）
  // 格式：https://raw.githubusercontent.com/[用户名]/[仓库名]/[分支]/data/articles.json
  dataUrl: 'https://raw.githubusercontent.com/gds910228/dailynew/main/data/articles.json'
};

/**
 * 获取文章列表
 */
function getArticles() {
  return new Promise((resolve, reject) => {
    wx.request({
      url: CONFIG.dataUrl,
      method: 'GET',
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(res.data);
        } else {
          reject(new Error('获取数据失败'));
        }
      },
      fail: (err) => {
        reject(err);
      }
    });
  });
}

/**
 * 根据ID获取文章详情
 */
function getArticleById(id, articles) {
  return articles.find(article => article.id === id);
}

/**
 * 根据分类筛选文章
 */
function filterByCategory(articles, category) {
  if (!category || category === '全部') return articles;
  return articles.filter(article => article.category === category);
}

/**
 * 根据标签搜索文章
 */
function searchByTags(articles, keyword) {
  if (!keyword) return articles;
  const lowerKeyword = keyword.toLowerCase();

  return articles.filter(article => {
    // 搜索标题
    if (article.title.toLowerCase().includes(lowerKeyword)) {
      return true;
    }
    // 搜索标签
    if (article.tags.some(tag => tag.toLowerCase().includes(lowerKeyword))) {
      return true;
    }
    // 搜索描述
    if (article.description.toLowerCase().includes(lowerKeyword)) {
      return true;
    }
    return false;
  });
}

/**
 * 下载图片到本地
 */
function downloadImage(imageUrl) {
  return new Promise((resolve, reject) => {
    wx.downloadFile({
      url: imageUrl,
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(res.tempFilePath);
        } else {
          reject(new Error('下载失败'));
        }
      },
      fail: (err) => {
        reject(err);
      }
    });
  });
}

/**
 * 保存图片到相册
 */
function saveImageToPhotosAlbum(filePath) {
  return new Promise((resolve, reject) => {
    wx.saveImageToPhotosAlbum({
      filePath: filePath,
      success: () => {
        wx.showToast({
          title: '已保存到相册',
          icon: 'success'
        });
        resolve();
      },
      fail: (err) => {
        if (err.errMsg.includes('auth deny')) {
          wx.showModal({
            title: '提示',
            content: '需要您授权保存图片到相册',
            showCancel: false,
            success: (res) => {
              wx.openSetting();
            }
          });
        }
        reject(err);
      }
    });
  });
}

module.exports = {
  getArticles,
  getArticleById,
  filterByCategory,
  searchByTags,
  downloadImage,
  saveImageToPhotosAlbum
};

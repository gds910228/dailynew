// API配置 - 多个备用URL
const CONFIG = {
  dataUrls: [
    'https://api.github.com/repos/gds910228/dailynew/contents/data/articles.json',
    'https://raw.githubusercontent.com/gds910228/dailynew/main/data/articles.json',
    'https://cdn.jsdelivr.net/gh/gds910228/dailynew@main/data/articles.json'
  ]
};

/**
 * 转换图片URL（开发环境使用本地路径）
 * @param {string} url - 原始图片URL（GitHub URL）
 * @returns {string} 本地路径或原始URL
 */
function convertImageUrl(url) {
  // 检测是否是开发环境
  const isDev = typeof __wxConfig !== 'undefined' &&
                (__wxConfig.envVersion === 'develop' || __wxConfig.envVersion === 'trial');

  if (!isDev) {
    // 生产环境，直接返回原URL
    return url;
  }

  // 开发环境：尝试转换为本地路径
  try {
    // GitHub URL格式:
    // https://raw.githubusercontent.com/gds910228/dailynew/main/assets/images/20260119/xxx.jpg

    // 提取文件路径部分
    const githubPrefix = 'https://raw.githubusercontent.com/gds910228/dailynew/main/assets/images/';

    if (!url.startsWith(githubPrefix)) {
      // 不是GitHub URL，直接返回
      return url;
    }

    // 提取路径：assets/images/20260119/xxx.jpg
    const imagePath = url.substring(githubPrefix.length);

    // 转换为小程序本地路径：/assets/images/20260119/xxx.jpg
    const localPath = `/assets/images/${imagePath}`;

    return localPath;

  } catch (error) {
    console.error('URL转换失败:', error);
    return url;
  }
}

/**
 * 批量转换图片URL
 */
function convertImageUrls(urls) {
  if (!Array.isArray(urls)) {
    return convertImageUrl(urls);
  }

  return urls.map(url => convertImageUrl(url));
}

/**
 * 获取文章列表（带多URL重试机制）
 */
function getArticles() {
  return new Promise((resolve, reject) => {
    let currentUrlIndex = 0;

    const tryRequest = () => {
      if (currentUrlIndex >= CONFIG.dataUrls.length) {
        reject(new Error('网络连接失败，请检查网络设置或稍后重试'));
        return;
      }

      const currentUrl = CONFIG.dataUrls[currentUrlIndex];
      console.log(`尝试加载源 ${currentUrlIndex + 1}/${CONFIG.dataUrls.length}:`, currentUrl);

      wx.request({
        url: currentUrl,
        method: 'GET',
        header: {
          'Accept': currentUrl.includes('api.github.com') ? 'application/vnd.github.v3+json' : 'application/json'
        },
        success: (res) => {
          if (res.statusCode === 200) {
            console.log(`✓ 数据源 ${currentUrlIndex + 1} 加载成功`);

            // GitHub API格式：content字段包含base64编码的内容
            if (res.data.content) {
              try {
                // GitHub API的base64内容需要移除换行符
                const base64Content = res.data.content.replace(/\n/g, '');
                console.log('Base64内容长度:', base64Content.length);

                // 解码base64 - 使用兼容微信小程序的方法
                let content = '';
                try {
                  // 方法1：标准atob + escape/unescape（支持中文）
                  content = decodeURIComponent(escape(atob(base64Content)));
                } catch (e) {
                  try {
                    // 方法2：直接atob（适合ASCII）
                    content = atob(base64Content);
                  } catch (e2) {
                    throw new Error('Base64解码失败');
                  }
                }

                console.log('解码后内容长度:', content.length);
                console.log('解码后内容预览:', content.substring(0, 50));

                // 解析JSON
                const data = JSON.parse(content);

                // 开发环境：转换图片URL为本地路径
                const isDev = typeof __wxConfig !== 'undefined' &&
                             (__wxConfig.envVersion === 'develop' || __wxConfig.envVersion === 'trial');

                if (isDev) {
                  console.log('开发环境：转换图片URL为本地路径');
                  data.articles = data.articles.map(article => {
                    const converted = {
                      ...article,
                      imageUrl: convertImageUrl(article.imageUrl),
                      imageUrls: convertImageUrls(article.imageUrls),
                      thumbnailUrl: convertImageUrl(article.thumbnailUrl)
                    };
                    return converted;
                  });
                }

                console.log('✓ 解析成功，文章数量:', data.articles.length);
                resolve(data);
              } catch (e) {
                console.error('✗ 解析数据失败', e);
                console.error('错误详情:', e.message);
                reject(new Error('数据解析失败: ' + e.message));
              }
            } else {
              // 直接返回数据（备用）
              console.log('直接返回数据（非GitHub API格式）');
              resolve(res.data);
            }
          } else {
            console.warn(`数据源 ${currentUrlIndex + 1} 返回错误:`, res.statusCode);
            currentUrlIndex++;
            tryRequest(); // 尝试下一个URL
          }
        },
        fail: (err) => {
          console.warn(`数据源 ${currentUrlIndex + 1} 请求失败:`, err.errMsg || err);
          currentUrlIndex++;
          tryRequest(); // 尝试下一个URL
        }
      });
    };

    tryRequest();
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
  saveImageToPhotosAlbum,
  convertImageUrl,
  convertImageUrls
};

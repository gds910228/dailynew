// API配置 - 多个备用URL
const CONFIG = {
  dataUrls: [
    'https://api.github.com/repos/gds910228/dailynew/contents/data/articles.json',
    'https://raw.githubusercontent.com/gds910228/dailynew/main/data/articles.json',
    'https://cdn.jsdelivr.net/gh/gds910228/dailynew@main/data/articles.json'
  ]
};

/**
 * Base64解码函数（微信小程序兼容版）
 * 优先使用微信官方API，降级到手动实现
 */
function decodeBase64(base64String) {
  // 方法1：使用微信官方API（最可靠）
  if (typeof wx !== 'undefined' && wx.base64ToArrayBuffer) {
    try {
      const arrayBuffer = wx.base64ToArrayBuffer(base64String);
      const uint8Array = new Uint8Array(arrayBuffer);
      let decoded = '';
      for (let i = 0; i < uint8Array.length; i++) {
        decoded += String.fromCharCode(uint8Array[i]);
      }
      return decoded;
    } catch (e) {
      console.warn('wx.base64ToArrayBuffer失败，尝试手动实现:', e);
    }
  }

  // 方法2：手动实现atob（备选）
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';
  let output = '';
  let buffer = 0;
  let bufferLength = 0;

  for (let i = 0; i < base64String.length; i++) {
    const char = base64String[i];
    const index = chars.indexOf(char);
    if (index === -1) continue;

    buffer = (buffer << 6) | index;
    bufferLength += 6;

    if (bufferLength >= 8) {
      output += String.fromCharCode((buffer >> (bufferLength - 8)) & 0xff);
      bufferLength -= 8;
    }
  }
  return output;
}

// 使用原生atob（如果在浏览器环境）或自定义实现
const safeAtob = typeof atob !== 'undefined' ? atob : decodeBase64;

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

                // 解码base64 - 使用更兼容的方法
                let content = '';

                try {
                  // 方法1：使用Uint8Array解码（最兼容，支持UTF-8）
                  const binaryString = safeAtob(base64Content);
                  const bytes = new Uint8Array(binaryString.length);
                  for (let i = 0; i < binaryString.length; i++) {
                    bytes[i] = binaryString.charCodeAt(i);
                  }
                  const decoder = new TextDecoder('utf-8');
                  content = decoder.decode(bytes);
                } catch (e1) {
                  console.warn('方法1失败，尝试方法2:', e1);
                  try {
                    // 方法2：escape/unescape（备选）
                    content = decodeURIComponent(escape(safeAtob(base64Content)));
                  } catch (e2) {
                    console.warn('方法2失败，尝试方法3:', e2);
                    try {
                      // 方法3：直接safeAtob（仅ASCII）
                      content = safeAtob(base64Content);
                    } catch (e3) {
                      console.error('所有解码方法都失败:', e3);
                      throw new Error('Base64解码失败，请检查网络连接');
                    }
                  }
                }

                // 清理末尾的空白字符和非法字符
                content = content.trim();

                console.log('解码后内容长度:', content.length);
                console.log('解码后内容预览:', content.substring(0, 50));
                console.log('解码后内容末尾:', content.substring(content.length - 50));

                // 解析JSON
                const data = JSON.parse(content);
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
  saveImageToPhotosAlbum
};

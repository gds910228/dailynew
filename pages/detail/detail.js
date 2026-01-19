// pages/detail/detail.js
const api = require('../../utils/api.js');
const storage = require('../../utils/storage.js');

Page({
  data: {
    article: {},             // 文章数据
    isFavorited: false,      // 是否已收藏
    currentImageIndex: 0     // 当前显示的图片索引
  },

  onLoad(options) {
    const id = options.id;
    if (id) {
      this.loadArticle(id);
    }
  },

  /**
   * 加载文章详情
   */
  async loadArticle(id) {
    try {
      wx.showLoading({ title: '加载中...' });

      // 获取所有文章
      const data = await api.getArticles();

      // 查找当前文章
      const article = api.getArticleById(id, data.articles);

      if (!article) {
        wx.hideLoading();
        wx.showToast({
          title: '文章不存在',
          icon: 'none'
        });
        return;
      }

      // 检查收藏状态
      const isFavorited = storage.isFavorited(id);

      // 记录浏览历史
      storage.addHistory(article);

      this.setData({
        article: article,
        isFavorited: isFavorited
      });

      wx.hideLoading();

    } catch (error) {
      console.error('加载文章失败', error);
      wx.hideLoading();

      wx.showToast({
        title: '加载失败',
        icon: 'none'
      });
    }
  },

  /**
   * 预览图片
   */
  onPreviewImage(e) {
    const { article } = this.data;

    // 支持多图预览
    if (article.imageUrls && article.imageUrls.length > 1) {
      const index = e.currentTarget.dataset.index || 0;
      wx.previewImage({
        current: article.imageUrls[index],
        urls: article.imageUrls
      });
    } else {
      // 单图预览（兼容旧数据）
      wx.previewImage({
        current: article.imageUrl,
        urls: [article.imageUrl]
      });
    }
  },

  /**
   * 图片切换事件
   */
  onImageChange(e) {
    this.setData({
      currentImageIndex: e.detail.current
    });
  },

  /**
   * 收藏/取消收藏
   */
  onFavorite() {
    const { article, isFavorited } = this.data;

    if (isFavorited) {
      // 取消收藏
      const result = storage.removeFavorite(article.id);
      wx.showToast({
        title: result.message,
        icon: 'none'
      });

      if (result.success) {
        this.setData({ isFavorited: false });
      }
    } else {
      // 添加收藏
      const result = storage.addFavorite(article);
      wx.showToast({
        title: result.message,
        icon: isFavorited ? 'none' : 'success'
      });

      if (result.success) {
        this.setData({ isFavorited: true });
      }
    }
  },

  /**
   * 下载原图
   */
  async onDownload() {
    const { article, currentImageIndex } = this.data;

    // 如果是多图，显示选择菜单
    if (article.imageUrls && article.imageUrls.length > 1) {
      wx.showActionSheet({
        itemList: ['下载当前图片', '下载所有图片'],
        success: async (res) => {
          if (res.tapIndex === 0) {
            // 下载当前图片
            await this.downloadSingleImage(article.imageUrls[currentImageIndex]);
          } else if (res.tapIndex === 1) {
            // 下载所有图片
            await this.downloadAllImages(article.imageUrls);
          }
        }
      });
    } else {
      // 单图直接下载
      await this.downloadSingleImage(article.imageUrl);
    }
  },

  /**
   * 下载单张图片
   */
  async downloadSingleImage(imageUrl) {
    try {
      wx.showLoading({ title: '下载中...' });

      const filePath = await api.downloadImage(imageUrl);
      await api.saveImageToPhotosAlbum(filePath);

      wx.hideLoading();

    } catch (error) {
      console.error('下载失败', error);
      wx.hideLoading();

      wx.showToast({
        title: '下载失败，请稍后重试',
        icon: 'none'
      });
    }
  },

  /**
   * 下载所有图片
   */
  async downloadAllImages(imageUrls) {
    wx.showModal({
      title: '确认下载',
      content: `将下载 ${imageUrls.length} 张图片，是否继续？`,
      success: async (res) => {
        if (res.confirm) {
          wx.showLoading({ title: '准备下载...' });

          let successCount = 0;
          let failCount = 0;

          for (let i = 0; i < imageUrls.length; i++) {
            try {
              wx.showLoading({ title: `下载 ${i + 1}/${imageUrls.length}` });

              const filePath = await api.downloadImage(imageUrls[i]);
              await api.saveImageToPhotosAlbum(filePath);

              successCount++;
            } catch (error) {
              console.error(`下载第${i + 1}张失败`, error);
              failCount++;
            }
          }

          wx.hideLoading();

          wx.showModal({
            title: '下载完成',
            content: `成功：${successCount}张\n失败：${failCount}张`,
            showCancel: false
          });
        }
      }
    });
  },

  /**
   * 分享配置
   */
  onShareAppMessage() {
    const { article } = this.data;

    return {
      title: article.title,
      path: `/pages/detail/detail?id=${article.id}`,
      imageUrl: article.thumbnailUrl
    };
  },

  /**
   * 分享到朋友圈
   */
  onShareTimeline() {
    const { article } = this.data;

    return {
      title: article.title,
      imageUrl: article.thumbnailUrl
    };
  },

  /**
   * 查看视频号内容
   */
  onWatchVideo() {
    const { article } = this.data;

    if (!article.videoId) {
      wx.showToast({
        title: '暂无视频内容',
        icon: 'none'
      });
      return;
    }

    // 这里可以跳转到视频号组件或打开链接
    wx.showModal({
      title: '提示',
      content: '请关注我们的视频号查看完整解读',
      confirmText: '去关注',
      success: (res) => {
        if (res.confirm) {
          // 这里可以添加打开视频号的逻辑
          // 例如使用 channel-live 组件或跳转
        }
      }
    });
  }
});

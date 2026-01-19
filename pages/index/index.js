// pages/index/index.js
const api = require('../../utils/api.js');
const storage = require('../../utils/storage.js');

Page({
  data: {
    articles: [],              // 所有文章
    filteredArticles: [],      // 筛选后的文章
    categories: ['全部'],      // 分类列表
    selectedCategory: '全部',  // 当前选中的分类
    searchKeyword: '',         // 搜索关键词
    loading: true,             // 加载状态
    refreshing: false          // 刷新状态
  },

  onLoad() {
    console.log('页面onLoad');
    this.loadArticles();
  },

  onShow() {
    console.log('页面onShow，当前文章数量:', this.data.articles.length);
    // 从详情页返回时，刷新收藏状态
    if (this.data.articles.length > 0) {
      this.updateArticlesFavoriteStatus();
    }
  },

  /**
   * 下拉刷新
   */
  onPullDownRefresh() {
    this.setData({ refreshing: true });
    this.loadArticles().then(() => {
      this.setData({ refreshing: false });
      wx.stopPullDownRefresh();
    });
  },

  /**
   * 加载文章数据
   */
  async loadArticles() {
    try {
      this.setData({ loading: true });

      const data = await api.getArticles();

      console.log('API返回的原始数据:', data);
      console.log('文章数量:', data.articles.length);

      // 数据规范化：确保所有必需字段都存在，并且都是简单类型
      const normalizedArticles = data.articles.map((article, index) => {
        const normalized = {
          id: String(article.id || `article_${index}`),
          title: String(article.title || '无标题'),
          description: String(article.description || ''),
          thumbnailUrl: String(article.thumbnailUrl || article.imageUrl || ''),
          publishDate: String(article.publishDate || '未知日期'),
          imageUrl: String(article.imageUrl || article.thumbnailUrl || ''),
          imageUrls: Array.isArray(article.imageUrls) ? article.imageUrls.map(url => String(url)) : [],
          viewCount: Number(article.viewCount || 0),
          downloadCount: Number(article.downloadCount || 0),
          favoriteCount: Number(article.favoriteCount || 0)
        };

        console.log(`文章${index}规范化后:`, normalized);
        return normalized;
      });

      // 按照日期降序排序（最新的在前）
      normalizedArticles.sort((a, b) => {
        return new Date(b.publishDate) - new Date(a.publishDate);
      });

      console.log('排序后的文章列表:', normalizedArticles.map(a => ({ id: a.id, title: a.title, date: a.publishDate })));

      this.setData({
        articles: normalizedArticles,
        loading: false
      });

      console.log('setData调用完成，articles长度:', this.data.articles.length);

      // 保存最后更新时间
      storage.setLastUpdate(data.meta.lastUpdate);

      // 显示成功提示
      wx.showToast({
        title: '数据加载成功',
        icon: 'success',
        duration: 1500
      });

    } catch (error) {
      console.error('加载文章失败', error);
      this.setData({ loading: false });

      // 显示详细错误信息
      wx.showModal({
        title: '数据加载失败',
        content: error.message || '网络连接失败，请检查网络设置',
        confirmText: '重试',
        cancelText: '查看帮助',
        success: (res) => {
          if (res.confirm) {
            // 重试
            this.loadArticles();
          } else if (res.cancel) {
            // 显示帮助信息
            wx.showModal({
              title: '网络问题排查',
              content: '可能的原因：\n1. 网络连接不稳定\n2. 需要关闭域名校验（开发阶段）\n3. GitHub服务暂时不可用\n\n建议：下拉刷新重试',
              showCancel: false
            });
          }
        }
      });
    }
  },

  /**
   * 搜索输入
   */
  onSearchInput(e) {
    const keyword = e.detail.value;
    this.setData({ searchKeyword: keyword });
    this.filterArticles();
  },

  /**
   * 清除搜索
   */
  onClearSearch() {
    this.setData({ searchKeyword: '' });
    this.filterArticles();
  },

  /**
   * 选择分类
   */
  onSelectCategory(e) {
    const category = e.currentTarget.dataset.category;
    this.setData({ selectedCategory: category });
    this.filterArticles();
  },

  /**
   * 筛选文章
   */
  filterArticles() {
    let { articles, selectedCategory, searchKeyword } = this.data;

    // 按分类筛选
    let filtered = api.filterByCategory(articles, selectedCategory);

    // 按关键词搜索
    if (searchKeyword.trim()) {
      filtered = api.searchByTags(filtered, searchKeyword);
    }

    this.setData({ filteredArticles: filtered });
  },

  /**
   * 点击文章卡片
   */
  onArticleTap(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/detail/detail?id=${id}`
    });
  },

  /**
   * 快速下载图片
   */
  async onQuickDownload(e) {
    const url = e.currentTarget.dataset.url;

    try {
      wx.showLoading({ title: '下载中...' });

      // 下载图片
      const filePath = await api.downloadImage(url);

      // 保存到相册
      await api.saveImageToPhotosAlbum(filePath);

      wx.hideLoading();

    } catch (error) {
      console.error('下载失败', error);
      wx.hideLoading();

      wx.showToast({
        title: '下载失败',
        icon: 'none'
      });
    }
  },

  /**
   * 更新文章收藏状态
   */
  updateArticlesFavoriteStatus() {
    const articles = this.data.articles.map(article => {
      return {
        ...article,
        isFavorited: storage.isFavorited(article.id)
      };
    });

    this.setData({ articles });
    this.filterArticles();
  }
});

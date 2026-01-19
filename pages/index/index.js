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
    this.loadArticles();
  },

  onShow() {
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

      // 提取分类
      const categorySet = new Set(['全部']);
      data.articles.forEach(article => {
        if (article.category) {
          categorySet.add(article.category);
        }
      });

      this.setData({
        articles: data.articles,
        filteredArticles: data.articles,
        categories: Array.from(categorySet),
        loading: false
      });

      // 保存最后更新时间
      storage.setLastUpdate(data.meta.lastUpdate);

    } catch (error) {
      console.error('加载文章失败', error);
      this.setData({ loading: false });

      wx.showToast({
        title: '加载失败，请稍后重试',
        icon: 'none'
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

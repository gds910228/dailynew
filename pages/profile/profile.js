// pages/profile/profile.js
const storage = require('../../utils/storage.js');
const api = require('../../utils/api.js');

Page({
  data: {
    currentTab: 0,        // 当前标签：0-收藏，1-历史
    favorites: [],        // 收藏列表
    history: [],          // 历史记录
    stats: {
      favoriteCount: 0,
      historyCount: 0
    },
    lastUpdateText: '--'  // 最后更新时间
  },

  onLoad() {
    this.loadData();
  },

  onShow() {
    // 每次显示页面时刷新数据
    this.loadData();
  },

  /**
   * 加载数据
   */
  loadData() {
    // 加载收藏
    const favorites = storage.getFavorites();
    // 加载历史
    const history = storage.getHistory();
    // 获取最后更新时间
    const lastUpdate = storage.getLastUpdate();

    this.setData({
      favorites: favorites,
      history: history,
      stats: {
        favoriteCount: favorites.length,
        historyCount: history.length
      },
      lastUpdateText: this.formatDate(lastUpdate)
    });
  },

  /**
   * 切换标签
   */
  onTabChange(e) {
    const tab = parseInt(e.currentTarget.dataset.tab);
    this.setData({ currentTab: tab });
  },

  /**
   * 点击文章
   */
  onArticleTap(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/detail/detail?id=${id}`
    });
  },

  /**
   * 取消收藏
   */
  onRemoveFavorite(e) {
    const id = e.currentTarget.dataset.id;

    wx.showModal({
      title: '提示',
      content: '确定要取消收藏吗？',
      success: (res) => {
        if (res.confirm) {
          const result = storage.removeFavorite(id);

          if (result.success) {
            wx.showToast({
              title: '已取消收藏',
              icon: 'success'
            });

            // 重新加载数据
            this.loadData();
          }
        }
      }
    });
  },

  /**
   * 清空历史记录
   */
  onClearHistory() {
    wx.showModal({
      title: '提示',
      content: '确定要清空所有浏览历史吗？',
      success: (res) => {
        if (res.confirm) {
          const result = storage.clearHistory();

          if (result.success) {
            wx.showToast({
              title: '已清空',
              icon: 'success'
            });

            // 重新加载数据
            this.loadData();
          }
        }
      }
    });
  },

  /**
   * 格式化日期
   */
  formatDate(dateString) {
    if (!dateString) return '--';

    try {
      const date = new Date(dateString);
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${month}-${day}`;
    } catch (e) {
      return '--';
    }
  },

  /**
   * 格式化时间
   */
  formatTime(timeString) {
    if (!timeString) return '';

    try {
      const date = new Date(timeString);
      const now = new Date();
      const diff = now - date;

      // 小于1小时
      if (diff < 3600000) {
        const minutes = Math.floor(diff / 60000);
        return minutes < 1 ? '刚刚' : `${minutes}分钟前`;
      }

      // 小于24小时
      if (diff < 86400000) {
        const hours = Math.floor(diff / 3600000);
        return `${hours}小时前`;
      }

      // 小于7天
      if (diff < 604800000) {
        const days = Math.floor(diff / 86400000);
        return `${days}天前`;
      }

      // 显示日期
      return this.formatDate(timeString);
    } catch (e) {
      return '';
    }
  }
});

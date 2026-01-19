/**
 * 本地存储工具类
 */

const STORAGE_KEYS = {
  FAVORITES: 'favorites',           // 收藏列表
  HISTORY: 'history',               // 浏览历史
  VIEW_COUNT: 'view_count',         // 浏览计数
  LAST_UPDATE: 'last_update'        // 最后更新时间
};

/**
 * 获取收藏列表
 */
function getFavorites() {
  try {
    const value = wx.getStorageSync(STORAGE_KEYS.FAVORITES);
    return value ? JSON.parse(value) : [];
  } catch (e) {
    console.error('获取收藏列表失败', e);
    return [];
  }
}

/**
 * 添加收藏
 */
function addFavorite(article) {
  try {
    const favorites = getFavorites();

    // 检查是否已收藏
    const exists = favorites.some(item => item.id === article.id);
    if (exists) {
      return { success: false, message: '已收藏' };
    }

    // 添加收藏时间
    favorites.unshift({
      ...article,
      favoriteTime: new Date().toISOString()
    });

    // 限制收藏数量（最多保存200条）
    if (favorites.length > 200) {
      favorites.pop();
    }

    wx.setStorageSync(STORAGE_KEYS.FAVORITES, JSON.stringify(favorites));

    return { success: true, message: '收藏成功' };
  } catch (e) {
    console.error('添加收藏失败', e);
    return { success: false, message: '收藏失败' };
  }
}

/**
 * 取消收藏
 */
function removeFavorite(articleId) {
  try {
    const favorites = getFavorites();
    const newFavorites = favorites.filter(item => item.id !== articleId);

    wx.setStorageSync(STORAGE_KEYS.FAVORITES, JSON.stringify(newFavorites));

    return { success: true, message: '已取消收藏' };
  } catch (e) {
    console.error('取消收藏失败', e);
    return { success: false, message: '操作失败' };
  }
}

/**
 * 检查是否已收藏
 */
function isFavorited(articleId) {
  const favorites = getFavorites();
  return favorites.some(item => item.id === articleId);
}

/**
 * 获取浏览历史
 */
function getHistory() {
  try {
    const value = wx.getStorageSync(STORAGE_KEYS.HISTORY);
    return value ? JSON.parse(value) : [];
  } catch (e) {
    console.error('获取浏览历史失败', e);
    return [];
  }
}

/**
 * 添加浏览历史
 */
function addHistory(article) {
  try {
    const history = getHistory();

    // 移除已存在的记录
    const newHistory = history.filter(item => item.id !== article.id);

    // 添加到最前面
    newHistory.unshift({
      ...article,
      viewTime: new Date().toISOString()
    });

    // 限制历史记录数量（最多保存100条）
    if (newHistory.length > 100) {
      newHistory.pop();
    }

    wx.setStorageSync(STORAGE_KEYS.HISTORY, JSON.stringify(newHistory));
  } catch (e) {
    console.error('添加浏览历史失败', e);
  }
}

/**
 * 清空浏览历史
 */
function clearHistory() {
  try {
    wx.removeStorageSync(STORAGE_KEYS.HISTORY);
    return { success: true, message: '已清空历史' };
  } catch (e) {
    console.error('清空历史失败', e);
    return { success: false, message: '操作失败' };
  }
}

/**
 * 记录浏览次数（本地统计）
 */
function incrementViewCount(articleId) {
  try {
    const key = `${STORAGE_KEYS.VIEW_COUNT}_${articleId}`;
    let count = wx.getStorageSync(key) || 0;
    count++;
    wx.setStorageSync(key, count);
    return count;
  } catch (e) {
    console.error('记录浏览次数失败', e);
    return 0;
  }
}

/**
 * 获取最后更新时间
 */
function getLastUpdate() {
  try {
    return wx.getStorageSync(STORAGE_KEYS.LAST_UPDATE) || null;
  } catch (e) {
    return null;
  }
}

/**
 * 设置最后更新时间
 */
function setLastUpdate(time) {
  try {
    wx.setStorageSync(STORAGE_KEYS.LAST_UPDATE, time);
  } catch (e) {
    console.error('设置更新时间失败', e);
  }
}

module.exports = {
  getFavorites,
  addFavorite,
  removeFavorite,
  isFavorited,
  getHistory,
  addHistory,
  clearHistory,
  incrementViewCount,
  getLastUpdate,
  setLastUpdate
};

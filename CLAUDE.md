# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a WeChat Mini Program (微信小程序) called "每日新知识汇" (Daily New Knowledge/Knowledge Hub). It's built using the WeChat Mini Program framework with JavaScript.

## Project Structure

```
dailynew/
├── app.js                 # Application entry point with global lifecycle hooks
├── app.json              # App configuration (pages, window settings, plugins)
├── app.wxss              # Global styles
├── pages/                # Page components (each page has .js, .json, .wxml, .wxss)
│   ├── index/           # Index/home page
│   └── logs/            # Logs page
├── utils/               # Utility modules
│   └── util.js          # Common utility functions (formatTime, etc.)
└── project.config.json  # WeChat DevTools project configuration
```

## Architecture

### WeChat Mini Program Framework
- **App Lifecycle**: Managed in `app.js` with `onLaunch()`, `onShow()`, `onHide()` hooks
- **Global Data**: Stored in `app.js` under `globalData` object, accessible via `getApp().globalData`
- **Page Structure**: Each page requires 4 files:
  - `.js` - Page logic and data
  - `.json` - Page configuration
  - `.wxml` - Page markup (similar to HTML)
  - `.wxss` - Page styles (similar to CSS)

### Page Registration
Pages are registered in `app.json` under the `pages` array. The first page is the default entry point.

### Component Framework
- Uses `glass-easel` component framework (configured in `app.json`)
- Components created using `Component()` constructor
- Pages created using `Page()` constructor

### WeChat APIs
The project uses WeChat-specific APIs prefixed with `wx.`:
- `wx.login()` - User login
- `wx.getUserProfile()` - Get user profile information
- `wx.navigateTo()` - Navigation between pages
- `wx.getStorageSync()` / `wx.setStorageSync()` - Local storage
- `wx.canIUse()` - Feature detection

## Development Setup

### Prerequisites
- WeChat DevTools (微信开发者工具)
- WeChat Developer Account

### Running the Application
1. Open WeChat DevTools
2. Import the project directory
3. Ensure the correct `appid` is set in `project.config.json`
4. The project uses `libVersion: "trial"` for development

### Code Configuration
- **ESLint**: Configured in `.eslintrc.js` with WeChat Mini Program globals (`wx`, `App`, `Page`, `Component`, etc.)
- **ES6+**: Enabled in project settings
- **Tab Size**: 2 spaces (configured in `editorSetting`)
- **Lazy Code Loading**: Enabled for performance optimization

## Important Conventions

### Data Binding
Pages use `this.setData()` to update page data and trigger view updates:
```javascript
this.setData({
  "userInfo.avatarUrl": newUrl
})
```

### User Info Handling
The app uses the new WeChat user info flow:
- Avatar selection via `bind:chooseavatar` event
- Nickname input via `<input type="nickname">` component
- Legacy `getUserProfile` API as fallback (marked as deprecated)

### Navigation
Use `wx.navigateTo()` for navigation:
```javascript
wx.navigateTo({
  url: '../logs/logs'
})
```

### Storage
Local storage uses synchronous APIs:
- `wx.getStorageSync('key')` - Read data
- `wx.setStorageSync('key', value)` - Write data

/**
 * SVG 转 PNG 转换脚本
 * 使用方法：
 * 1. npm install sharp svg2img (或 yarn add)
 * 2. node convert-icon.js
 */

const fs = require('fs');
const path = require('path');

// SVG 文件路径
const svgPath = path.join(__dirname, 'app-icon-v3.svg');

// 读取 SVG 文件
const svgContent = fs.readFileSync(svgPath, 'utf8');

// 目标尺寸
const sizes = [
  { name: 'icon-144', size: 144 },   // 小程序主图标
  { name: 'icon-81', size: 81 },     // Tab 图标
  { name: 'icon-512', size: 512 },   // 高清版本
  { name: 'icon-120', size: 120 }    // 分享图标
];

console.log('🎨 开始转换图标...\n');

// 检查是否安装了依赖
try {
  require('sharp');
  convertWithSharp();
} catch (e) {
  console.log('⚠️  未安装 sharp，请运行以下命令安装：');
  console.log('   npm install sharp');
  console.log('\n或者使用在线转换工具：');
  console.log('   https://convertio.co/zh/svg-png/\n');
  console.log('推荐尺寸：');
  sizes.forEach(({ name, size }) => {
    console.log(`   - ${name}: ${size}×${size}px`);
  });
}

function convertWithSharp() {
  const sharp = require('sharp');

  sizes.forEach(({ name, size }) => {
    const outputPath = path.join(__dirname, `app-icon-v3-${name}.png`);

    sharp(Buffer.from(svgContent))
      .resize(size, size)
      .png()
      .toFile(outputPath)
      .then(() => {
        const stats = fs.statSync(outputPath);
        const fileSize = (stats.size / 1024).toFixed(2);
        console.log(`✅ ${name}.png (${size}×${size}) - ${fileSize}KB`);
      })
      .catch(err => {
        console.error(`❌ 转换失败 ${name}:`, err.message);
      });
  });

  console.log('\n✨ 转换完成！');
}

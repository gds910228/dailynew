#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图标生成器 - 生成临时占位图标

需要安装：pip install Pillow
运行：python generate_icons.py
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    print("[OK] PIL library is installed")
except ImportError:
    print("[ERROR] Please install PIL: pip install Pillow")
    exit(1)

import os

# 创建目录
os.makedirs('assets/icons', exist_ok=True)

# 图标配置
ICONS = {
    # TabBar图标（81x81）
    'home.png': {'size': 81, 'color': '#999999', 'shape': 'house'},
    'home-active.png': {'size': 81, 'color': '#667eea', 'shape': 'house'},
    'profile.png': {'size': 81, 'color': '#999999', 'shape': 'user'},
    'profile-active.png': {'size': 81, 'color': '#667eea', 'shape': 'user'},

    # 功能图标（32x32）
    'search.png': {'size': 32, 'color': '#999999', 'shape': 'search'},
    'close.png': {'size': 32, 'color': '#999999', 'shape': 'close'},
    'download.png': {'size': 32, 'color': '#999999', 'shape': 'download'},
    'heart.png': {'size': 32, 'color': '#999999', 'shape': 'heart'},
    'heart-active.png': {'size': 32, 'color': '#ff4d4f', 'shape': 'heart'},
    'share.png': {'size': 32, 'color': '#999999', 'shape': 'share'},
    'video.png': {'size': 32, 'color': '#999999', 'shape': 'play'},
    'delete.png': {'size': 32, 'color': '#ff4d4f', 'shape': 'delete'},

    # 状态图标（200x200）
    'empty.png': {'size': 200, 'color': '#cccccc', 'shape': 'empty'},
    'empty-favorite.png': {'size': 160, 'color': '#cccccc', 'shape': 'heart'},
    'empty-history.png': {'size': 160, 'color': '#cccccc', 'shape': 'clock'},

    # 应用图标（120x120）
    'app-icon.png': {'size': 120, 'color': '#667eea', 'shape': 'app'},
}

def hex_to_rgb(hex_color):
    """转换十六进制颜色为RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def draw_house(draw, size, color):
    """画房子图标（home）"""
    w, h = size
    # 屋顶
    points = [(w//4, h//2), (w//2, h//4), (w*3//4, h//2)]
    draw.polygon(points, fill=color)
    # 房子主体
    draw.rectangle([w//4, h//2, w*3//4, h*3//4], fill=color)

def draw_user(draw, size, color):
    """画用户图标（profile）"""
    w, h = size
    # 头部
    draw.ellipse([w//3, h//4, w*2//3, h//2], fill=color)
    # 身体
    draw.ellipse([w//4, h//2, w*3//4, h*3//4], fill=color)

def draw_search(draw, size, color):
    """画搜索图标"""
    w, h = size
    # 放大镜圆形
    draw.ellipse([w//8, h//8, w*5//8, h*5//8], outline=color, width=max(2, w//8))
    # 手柄
    draw.line([w*5//8, h*5//8, w*7//8, h*7//8], fill=color, width=max(2, w//8))

def draw_close(draw, size, color):
    """画关闭图标"""
    w, h = size
    margin = w // 4
    draw.line([margin, margin, w-margin, h-margin], fill=color, width=max(2, w//8))
    draw.line([w-margin, margin, margin, h-margin], fill=color, width=max(2, w//8))

def draw_download(draw, size, color):
    """画下载图标"""
    w, h = size
    # 箭头
    draw.polygon([w//2, h*3//4, w//3, h//2, w*2//3, h//2], fill=color)
    # 横线
    draw.line([w//4, h//4, w*3//4, h//4], fill=color, width=max(2, w//8))

def draw_heart(draw, size, color):
    """画心形图标"""
    w, h = size
    # 两个圆
    draw.ellipse([w//8, h//8, w*3//8, h*3//8], fill=color)
    draw.ellipse([w*5//8, h//8, w*7//8, h*3//8], fill=color)
    # 下三角
    points = [(w//8, h//3), (w//2, h*7//8), (w*7//8, h//3)]
    draw.polygon(points, fill=color)

def draw_share(draw, size, color):
    """画分享图标"""
    w, h = size
    # 三个圆
    draw.ellipse([w*3//8, h//8, w*5//8, h*3//8], fill=color)
    draw.ellipse([w//8, h*5//8, w*3//8, h*7//8], fill=color)
    draw.ellipse([w*5//8, h*5//8, w*7//8, h*7//8], fill=color)
    # 连线
    draw.line([w//2, h//4, w//4, h*3//4], fill=color, width=1)
    draw.line([w//2, h//4, w*3//4, h*3//4], fill=color, width=1)

def draw_play(draw, size, color):
    """画播放图标"""
    w, h = size
    points = [(w//4, h//4), (w*3//4, h//2), (w//4, h*3//4)]
    draw.polygon(points, fill=color)

def draw_delete(draw, size, color):
    """画删除图标"""
    w, h = size
    # 桶身
    draw.rectangle([w//4, h//3, w*3//4, h*7//8], fill=color)
    # 桶盖
    draw.rectangle([w//5, h//4, w*4//5, h//3], fill=color)
    # 把手
    draw.line([w//2, h//8, w//2, h//4], fill=color, width=max(1, w//16))

def draw_empty(draw, size, color):
    """画空状态图标"""
    w, h = size
    # 画一个打开的盒子
    draw.rectangle([w//4, h//3, w*3//4, h*3//4], outline=color, width=max(2, w//16))

def draw_clock(draw, size, color):
    """画时钟图标"""
    w, h = size
    # 圆形
    draw.ellipse([w//8, h//8, w*7//8, h*7//8], outline=color, width=max(2, w//16))
    # 指针
    draw.line([w//2, h//2, w//2, h//3], fill=color, width=max(2, w//16))
    draw.line([w//2, h//2, w*3//5, h//2], fill=color, width=max(2, w//16))

def draw_app(draw, size, color):
    """画应用图标"""
    w, h = size
    # 渐变背景（简化为纯色）
    draw.rectangle([0, 0, w, h], fill=color)
    # 添加文字"知"
    try:
        font = ImageFont.truetype("msyh.ttc", size//2)
    except:
        font = ImageFont.load_default()
    text = "知"
    # 获取文本边界框
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((w - text_width) // 2, (h - text_height) // 2)
    draw.text(position, text, fill='white', font=font)

# 形状绘制函数映射
DRAW_FUNCTIONS = {
    'house': draw_house,
    'user': draw_user,
    'search': draw_search,
    'close': draw_close,
    'download': draw_download,
    'heart': draw_heart,
    'share': draw_share,
    'play': draw_play,
    'delete': draw_delete,
    'empty': draw_empty,
    'clock': draw_clock,
    'app': draw_app,
}

def generate_icon(filename, config):
    """生成单个图标"""
    size = config['size']
    color = hex_to_rgb(config['color'])
    shape = config['shape']

    # 创建透明背景图像
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # 绘制形状
    if shape in DRAW_FUNCTIONS:
        DRAW_FUNCTIONS[shape](draw, (size, size), color)
    else:
        # 默认画一个圆
        draw.ellipse([size//4, size//4, size*3//4, size*3//4], fill=color)

    # 保存
    filepath = f'assets/icons/{filename}'
    img.save(filepath)
    print(f"[OK] Generated: {filename}")

def main():
    print("Starting icon generation...\n")

    for filename, config in ICONS.items():
        try:
            generate_icon(filename, config)
        except Exception as e:
            print(f"[ERROR] Failed to generate {filename}: {e}")

    print(f"\n[Done] Generated {len(ICONS)} icons")
    print(f"[Path] assets/icons/")
    print("\n[TIP] These are placeholder icons, replace them with professional ones later")

if __name__ == '__main__':
    main()

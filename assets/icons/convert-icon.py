"""
SVG 转 PNG 转换脚本 (Python 版本)
使用方法：
1. pip install cairosvg
2. python convert-icon.py
"""

import cairosvg
from pathlib import Path

# SVG 文件路径
svg_path = Path(__file__).parent / 'app-icon-v3.svg'

# 读取 SVG
with open(svg_path, 'r', encoding='utf-8') as f:
    svg_content = f.read()

# 目标尺寸
sizes = [
    ('icon-144', 144),  # 小程序主图标
    ('icon-81', 81),    # Tab 图标
    ('icon-512', 512),  # 高清版本
    ('icon-120', 120),  # 分享图标
]

print('🎨 开始转换图标...\n')

for name, size in sizes:
    output_path = Path(__file__).parent / f'app-icon-v3-{name}.png'

    try:
        cairosvg.svg2png(
            bytestring=svg_content.encode('utf-8'),
            write_to=str(output_path),
            output_width=size,
            output_height=size
        )

        file_size = output_path.stat().st_size / 1024
        print(f'✅ {name}.png ({size}×{size}) - {file_size:.2f}KB')

    except Exception as e:
        print(f'❌ 转换失败 {name}: {e}')

print('\n✨ 转换完成！')

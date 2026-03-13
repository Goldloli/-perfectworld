#!/usr/bin/env python3
"""
生成 Dota 2 启动器图标
需要安装 Pillow: pip install Pillow
"""

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("请先安装 Pillow: pip install Pillow")
    exit(1)

def generate_icon():
    """生成应用图标"""
    size = 256
    img = Image.new('RGBA', (size, size), (30, 30, 46, 0))
    draw = ImageDraw.Draw(img)

    # 配色
    primary_color = (122, 162, 247)  # 蓝色
    bg_color = (30, 30, 46)          # 背景色

    # 外圈
    padding = 10
    draw.ellipse(
        [padding, padding, size - padding, size - padding],
        outline=primary_color,
        width=12
    )

    # 中心三角形（Dota 风格）
    center_x, center_y = size // 2, size // 2
    triangle_size = 65
    triangle = [
        (center_x, center_y - triangle_size),
        (center_x + int(triangle_size * 0.87), center_y + triangle_size // 2),
        (center_x - int(triangle_size * 0.87), center_y + triangle_size // 2)
    ]
    draw.polygon(triangle, fill=primary_color)

    # 中心小圆
    circle_radius = 28
    draw.ellipse(
        [center_x - circle_radius, center_y - circle_radius // 2,
         center_x + circle_radius, center_y + circle_radius * 1.5],
        fill=bg_color
    )

    # 保存为多尺寸 ICO 文件
    img.save('icon.ico', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print("✓ 图标已生成: icon.ico")

    # 同时生成一个 PNG 预览
    img.save('icon_preview.png')
    print("✓ 预览图已生成: icon_preview.png")

if __name__ == "__main__":
    generate_icon()

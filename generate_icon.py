#!/usr/bin/env python3
"""
生成 Dota 2 风格启动器图标
需要安装 Pillow: pip install Pillow
"""

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("Please install Pillow: pip install Pillow")
    exit(1)

def generate_icon():
    """生成 Dota 2 风格图标"""
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Dota 2 配色
    red_color = (178, 34, 34)      # 深红色
    dark_red = (139, 0, 0)         # 暗红色
    black = (10, 10, 10)           # 黑色背景
    gray = (40, 40, 40)            # 灰色

    center_x, center_y = size // 2, size // 2

    # 背景圆形（黑色底）
    padding = 8
    draw.ellipse(
        [padding, padding, size - padding, size - padding],
        fill=black,
        outline=red_color,
        width=6
    )

    # 绘制抽象龙/恶魔头像（Dota 2 风格）
    # 头部轮廓 - 使用多边形绘制
    head_points = [
        # 头顶
        (center_x, center_y - 70),
        # 右侧角
        (center_x + 55, center_y - 50),
        (center_x + 70, center_y - 30),
        # 右脸颊
        (center_x + 60, center_y + 10),
        (center_x + 50, center_y + 40),
        # 下巴
        (center_x + 20, center_y + 65),
        (center_x, center_y + 70),
        (center_x - 20, center_y + 65),
        # 左脸颊
        (center_x - 50, center_y + 40),
        (center_x - 60, center_y + 10),
        # 左侧角
        (center_x - 70, center_y - 30),
        (center_x - 55, center_y - 50),
    ]
    draw.polygon(head_points, fill=red_color)

    # 眼睛（发光的白色/浅色）
    eye_color = (255, 200, 100)  # 金色眼睛
    # 左眼
    left_eye_points = [
        (center_x - 35, center_y - 15),
        (center_x - 15, center_y - 10),
        (center_x - 20, center_y + 5),
        (center_x - 40, center_y),
    ]
    draw.polygon(left_eye_points, fill=eye_color)

    # 右眼
    right_eye_points = [
        (center_x + 35, center_y - 15),
        (center_x + 15, center_y - 10),
        (center_x + 20, center_y + 5),
        (center_x + 40, center_y),
    ]
    draw.polygon(right_eye_points, fill=eye_color)

    # 额头装饰线
    draw.line([
        (center_x, center_y - 60),
        (center_x, center_y - 25)
    ], fill=dark_red, width=4)

    # 鼻孔
    draw.ellipse([center_x - 8, center_y + 35, center_x - 3, center_y + 42], fill=dark_red)
    draw.ellipse([center_x + 3, center_y + 35, center_x + 8, center_y + 42], fill=dark_red)

    # 保存为多尺寸 ICO 文件（用于窗口图标）
    img.save('icon.ico', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print("[OK] Icon generated: icon.ico")

    # 同时生成 dota2.png（用于界面显示）
    img.save('dota2.png', 'PNG')
    print("[OK] PNG generated: dota2.png")

    # 生成预览图
    img.save('icon_preview.png')
    print("[OK] Preview generated: icon_preview.png")

if __name__ == "__main__":
    generate_icon()

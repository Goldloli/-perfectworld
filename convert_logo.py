#!/usr/bin/env python3
"""
将 Dota 2 logo 转换为应用图标
使用方法：
1. 准备 logo.png（Dota 2 logo 图片）
2. 运行 python convert_logo.py
3. 生成 icon.ico
"""

try:
    from PIL import Image
except ImportError:
    print("请先安装 Pillow: pip install Pillow")
    exit(1)

def convert_logo():
    """将 logo.png 转换为 icon.ico"""
    try:
        # 打开 logo 图片
        img = Image.open('dota2.png')

        # 转换为 RGBA 模式（如果不是）
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # 裁剪为正方形（从中心）
        width, height = img.size
        size = min(width, height)
        left = (width - size) // 2
        top = (height - size) // 2
        right = left + size
        bottom = top + size
        img = img.crop((left, top, right, bottom))

        # 调整尺寸
        img = img.resize((256, 256), Image.LANCZOS)

        # 保存为多尺寸 ICO
        img.save('icon.ico', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
        print("[OK] icon.ico 生成成功")

    except FileNotFoundError:
        print("[错误] 未找到 logo.png，请将 Dota 2 logo 图片放在当前目录并命名为 logo.png")
    except Exception as e:
        print(f"[错误] {e}")

if __name__ == "__main__":
    convert_logo()

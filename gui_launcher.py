#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dota 2 国服启动器 - 现代扁平化设计
"""

import os
import sys
import re
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None

# Dota 2 AppID
DOTA2_APPID = "570"

# 配色方案 - Dota 2 红黑色调（优化可读性）
COLORS = {
    "bg_primary": "#333333",       # 主背景 (深灰色)
    "bg_secondary": "#2d2d2d",     # 次级背景
    "bg_card": "#3d3d3d",          # 卡片背景
    "accent": "#b71c1c",           # 强调色 (Dota红)
    "accent_hover": "#d32f2f",     # 强调色悬停 (亮红)
    "success": "#2e7d32",          # 成功色 (绿色)
    "success_hover": "#4caf50",    # 成功色悬停
    "text_primary": "#ffffff",     # 主文字 (白色)
    "text_secondary": "#ffffff",   # 次级文字 (白色)
    "text_muted": "#888888",       # 灰色文字
    "border": "#5c0000",           # 边框色 (深红)
    "radio_selected": "#ff1744",   # 单选选中色 (亮红)
}


class ModernButton(tk.Canvas):
    """现代圆角按钮"""
    def __init__(self, parent, text, command=None, width=160, height=42,
                 bg_color=None, hover_color=None, text_color=None, **kwargs):
        self.bg_color = bg_color or COLORS["accent"]
        self.hover_color = hover_color or COLORS["accent_hover"]
        self.text_color = text_color or "#1e1e2e"
        self.corner_radius = 8

        super().__init__(parent, width=width, height=height,
                        highlightthickness=0, bg=parent["bg"], **kwargs)

        self.text = text
        self.command = command
        self.is_hovered = False
        self.is_pressed = False

        self.draw_button()

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_click)

    def draw_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """绘制圆角矩形"""
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def draw_button(self):
        self.delete("all")

        if self.is_pressed:
            color = self._darken_color(self.hover_color)
            offset = 1
        else:
            color = self.hover_color if self.is_hovered else self.bg_color
            offset = 0

        # 绘制阴影
        if not self.is_pressed:
            self.draw_rounded_rect(2, 3, self.winfo_reqwidth(), self.winfo_reqheight()+1,
                                  self.corner_radius, fill="#0f0f1a", outline="")

        # 绘制按钮主体
        self.draw_rounded_rect(0, offset, self.winfo_reqwidth()-2, self.winfo_reqheight()-2+offset,
                              self.corner_radius, fill=color, outline="")

        # 绘制文字
        self.create_text(self.winfo_reqwidth()//2-1, self.winfo_reqheight()//2+offset,
                        text=self.text, fill=self.text_color,
                        font=("Microsoft YaHei", 12, "bold"))

    def _darken_color(self, color):
        """将颜色变暗"""
        # 简单的颜色变暗处理
        return color

    def on_enter(self, event):
        self.is_hovered = True
        self.draw_button()
        self.config(cursor="hand2")

    def on_leave(self, event):
        self.is_hovered = False
        self.is_pressed = False
        self.draw_button()
        self.config(cursor="")

    def on_press(self, event):
        self.is_pressed = True
        self.draw_button()

    def on_click(self, event):
        self.is_pressed = False
        self.draw_button()
        if self.command and self.is_hovered:
            self.command()


class RadioOption(tk.Frame):
    """现代单选卡片"""
    def __init__(self, parent, title, subtitle, value, variable, **kwargs):
        super().__init__(parent, bg=COLORS["bg_card"], **kwargs)

        self.value = value
        self.variable = variable
        self.selected = False

        # 添加边框效果
        self.config(highlightbackground=COLORS["border"], highlightthickness=1)

        # 内边距容器
        inner_frame = tk.Frame(self, bg=COLORS["bg_card"], padx=24, pady=20)
        inner_frame.pack(fill=tk.BOTH, expand=True)

        # 左侧选择指示器
        self.indicator = tk.Canvas(inner_frame, width=20, height=20, bg=COLORS["bg_card"],
                                   highlightthickness=0)
        self.indicator.pack(side=tk.LEFT, padx=(0, 16))
        self.draw_indicator()

        # 文字区域
        text_frame = tk.Frame(inner_frame, bg=COLORS["bg_card"])
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 标题行（包含标签）
        title_frame = tk.Frame(text_frame, bg=COLORS["bg_card"])
        title_frame.pack(fill=tk.X)

        # 标题
        self.title_label = tk.Label(title_frame, text=title, bg=COLORS["bg_card"],
                                   fg=COLORS["text_primary"], font=("Microsoft YaHei", 13, "bold"),
                                   anchor="w")
        self.title_label.pack(side=tk.LEFT)

        # 服务器标签
        if value == "perfectworld":
            tag_text = "推荐"
            tag_color = COLORS["success"]
            tag_fg = "#ffffff"
        else:
            tag_text = "不推荐"
            tag_color = None  # 无背景
            tag_fg = COLORS["text_muted"]  # 灰色文字

        self.tag_label = tk.Label(title_frame, text=tag_text, bg=tag_color,
                                 fg=tag_fg, font=("Microsoft YaHei", 9, "bold"),
                                 padx=8, pady=2)
        self.tag_label.pack(side=tk.LEFT, padx=(10, 0))

        # 副标题
        self.subtitle_label = tk.Label(text_frame, text=subtitle, bg=COLORS["bg_card"],
                                      fg=COLORS["text_muted"], font=("Microsoft YaHei", 11),
                                      anchor="w", wraplength=450, justify=tk.LEFT)
        self.subtitle_label.pack(fill=tk.X, pady=(6, 0))

        # 绑定点击事件
        for widget in [self, inner_frame, self.indicator, text_frame,
                      self.title_label, self.subtitle_label, title_frame, self.tag_label]:
            widget.bind("<Button-1>", self.select)
            widget.bind("<Enter>", self.on_enter)
            widget.bind("<Leave>", self.on_leave)

        # 跟踪变量变化
        self.variable.trace_add("write", self.update_state)

    def draw_indicator(self):
        self.indicator.delete("all")
        selected = self.variable.get() == self.value

        # 外圈
        self.indicator.create_oval(2, 2, 18, 18, outline=COLORS["radio_selected"] if selected else COLORS["border"],
                                  width=2 if selected else 2)

        # 内圆（选中时显示）
        if selected:
            self.indicator.create_oval(6, 6, 14, 14, fill=COLORS["radio_selected"], outline="")

    def select(self, event=None):
        self.variable.set(self.value)

    def update_state(self, *args):
        self.draw_indicator()
        selected = self.variable.get() == self.value

        if selected:
            self.config(highlightbackground=COLORS["radio_selected"], highlightthickness=2)
        else:
            self.config(highlightbackground=COLORS["border"], highlightthickness=1)
        # 标题始终使用白色
        self.title_label.config(fg=COLORS["text_primary"])

    def on_enter(self, event):
        self.config(cursor="hand2")
        if self.variable.get() != self.value:
            self.config(highlightbackground=COLORS["accent"], highlightthickness=1)

    def on_leave(self, event):
        self.config(cursor="")
        self.update_state()


class Dota2Launcher:
    def __init__(self, root):
        self.root = root
        self.root.title("Dota 2 国服启动器")
        self.root.geometry("760x600")
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS["bg_primary"])

        # 设置窗口图标
        self.set_window_icon()

        # 居中窗口
        self.center_window()

        self.steam_path = None
        self.find_steam_path()

        # 选中的服务器类型
        self.server_type = tk.StringVar(value="perfectworld")

        self.create_ui()

    def get_resource_path(self, filename):
        """获取资源文件路径（兼容 PyInstaller 打包）"""
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller 打包后的临时目录
            return os.path.join(sys._MEIPASS, filename)
        else:
            # 开发环境
            return os.path.join(os.path.dirname(__file__), filename)

    def set_window_icon(self):
        """设置窗口图标"""
        try:
            # 加载 icon.ico 作为窗口图标
            icon_path = self.get_resource_path("icon.ico")
            if os.path.exists(icon_path) and Image and ImageTk:
                icon_img = Image.open(icon_path)
                icon_tk = ImageTk.PhotoImage(icon_img)
                self.root.iconphoto(True, icon_tk)
                self.icon_img = icon_tk  # 保持引用防止被垃圾回收
        except Exception as e:
            print(f"[警告] 无法设置窗口图标: {e}")

    def center_window(self):
        """窗口居中"""
        self.root.update_idletasks()
        width = 760
        height = 600
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_ui(self):
        """创建现代扁平化界面"""
        # 主容器
        main_container = tk.Frame(self.root, bg=COLORS["bg_primary"])
        main_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

        # 顶部标题区域
        header_frame = tk.Frame(main_container, bg=COLORS["bg_primary"])
        header_frame.pack(fill=tk.X, pady=(0, 24))

        # 图标 + 标题（居中）
        title_row = tk.Frame(header_frame, bg=COLORS["bg_primary"])
        title_row.pack(anchor="center")

        # Dota 2 Logo（优先使用 dota2.png，更可靠）
        logo_loaded = False
        try:
            # 优先尝试 dota2.png
            png_path = self.get_resource_path("dota2.png")
            if os.path.exists(png_path) and Image and ImageTk:
                logo_img = Image.open(png_path)
                logo_img = logo_img.resize((48, 48), Image.LANCZOS)
                logo_tk = ImageTk.PhotoImage(logo_img)
                logo_label = tk.Label(title_row, image=logo_tk, bg=COLORS["bg_primary"])
                logo_label.image = logo_tk  # 保持引用
                logo_label.pack(side=tk.LEFT, padx=(0, 16))
                logo_loaded = True
        except Exception as e:
            print(f"[警告] 无法加载 dota2.png: {e}")

        if not logo_loaded:
            try:
                # 备用：尝试 icon.ico
                icon_path = self.get_resource_path("icon.ico")
                if os.path.exists(icon_path) and Image and ImageTk:
                    logo_img = Image.open(icon_path)
                    logo_img = logo_img.resize((48, 48), Image.LANCZOS)
                    logo_tk = ImageTk.PhotoImage(logo_img)
                    logo_label = tk.Label(title_row, image=logo_tk, bg=COLORS["bg_primary"])
                    logo_label.image = logo_tk
                    logo_label.pack(side=tk.LEFT, padx=(0, 16))
                    logo_loaded = True
            except Exception as e:
                print(f"[警告] 无法加载 icon.ico: {e}")


        # 标题文字
        title_col = tk.Frame(title_row, bg=COLORS["bg_primary"])
        title_col.pack(side=tk.LEFT)

        title = tk.Label(title_col, text="Dota 2", bg=COLORS["bg_primary"],
                        fg=COLORS["text_primary"], font=("Microsoft YaHei", 30, "bold"))
        title.pack(anchor="w")

        subtitle = tk.Label(title_col, text="国服启动器", bg=COLORS["bg_primary"],
                           fg=COLORS["text_primary"], font=("Microsoft YaHei", 15, "bold"))
        subtitle.pack(anchor="w")

        # 分隔线
        separator = tk.Frame(main_container, bg=COLORS["border"], height=1)
        separator.pack(fill=tk.X, pady=(0, 20))

        # 选择提示
        hint = tk.Label(main_container, text="选择服务器：",
                       bg=COLORS["bg_primary"], fg=COLORS["text_primary"],
                       font=("Microsoft YaHei", 12))
        hint.pack(anchor="w", pady=(0, 12))

        # 选项区域
        options_frame = tk.Frame(main_container, bg=COLORS["bg_primary"])
        options_frame.pack(fill=tk.X, pady=(0, 20))

        # 国服选项
        self.option_pw = RadioOption(
            options_frame,
            title="Perfect World 国服",
            subtitle="在低延迟的国服服务器上游玩，并使用您蒸汽平台帐户内的钱包资金消费。",
            value="perfectworld",
            variable=self.server_type
        )
        self.option_pw.pack(fill=tk.X, pady=(0, 12))

        # 国际服选项
        self.option_ww = RadioOption(
            options_frame,
            title="Steam 国际服",
            subtitle="在中国境外的服务器上游玩，并使用您 Steam 帐户内的钱包资金消费。可能会造成丢包卡顿等众多网络问题。",
            value="worldwide",
            variable=self.server_type
        )
        self.option_ww.pack(fill=tk.X)

        # 底部区域
        bottom_frame = tk.Frame(main_container, bg=COLORS["bg_primary"])
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # 按钮容器
        btn_frame = tk.Frame(bottom_frame, bg=COLORS["bg_primary"])
        btn_frame.pack(pady=(16, 8))

        # 写入启动项按钮（次要按钮）- 尺寸翻倍
        self.write_btn = ModernButton(
            btn_frame,
            text="写入启动项",
            command=self.on_write_only,
            width=200,
            height=52,
            bg_color=COLORS["bg_card"],
            hover_color=COLORS["bg_secondary"],
            text_color=COLORS["text_primary"]
        )
        self.write_btn.pack(side=tk.LEFT, padx=(0, 16))

        # 开始游戏按钮（主要按钮）- 白色文字，尺寸翻倍
        self.start_btn = ModernButton(
            btn_frame,
            text="开始游戏",
            command=self.on_start_game,
            width=200,
            height=52,
            bg_color=COLORS["success"],
            hover_color=COLORS["success_hover"],
            text_color="#ffffff"
        )
        self.start_btn.pack(side=tk.LEFT)

        # 状态栏
        self.status_label = tk.Label(bottom_frame,
                                    text=self.get_status_text(),
                                    bg=COLORS["bg_primary"],
                                    fg=COLORS["text_muted"],
                                    font=("Microsoft YaHei", 10))
        self.status_label.pack(pady=(12, 0))

    def get_status_text(self):
        if self.steam_path:
            return f"Steam 已检测"
        return "未检测到 Steam，首次使用将提示选择路径"

    def find_steam_path(self):
        """查找 Steam 路径"""
        possible_paths = [
            r"C:\Program Files (x86)\Steam",
            r"C:\Program Files\Steam",
            r"D:\Steam",
            r"E:\Steam",
            os.path.expandvars(r"%LOCALAPPDATA%\Steam"),
            os.path.expandvars(r"%PROGRAMFILES%\Steam"),
            os.path.expandvars(r"%PROGRAMFILES(X86)%\Steam"),
        ]

        for path in possible_paths:
            if path and os.path.exists(os.path.join(path, "steam.exe")):
                self.steam_path = path
                return

        # 尝试注册表
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r"SOFTWARE\WOW6432Node\Valve\Steam")
            path, _ = winreg.QueryValueEx(key, "InstallPath")
            if path and os.path.exists(os.path.join(path, "steam.exe")):
                self.steam_path = path
            winreg.CloseKey(key)
        except:
            pass

    def _ensure_steam_path(self):
        """确保 Steam 路径已设置，如果没有则提示选择"""
        if not self.steam_path:
            from tkinter import filedialog
            path = filedialog.askdirectory(title="选择 Steam 目录（包含 steam.exe）")
            if not path or not os.path.exists(os.path.join(path, "steam.exe")):
                messagebox.showerror("错误", "未找到 steam.exe")
                return False
            self.steam_path = path
        return True

    def _configure_all_users(self):
        """给所有检测到的账号配置启动项，返回 (success_count, server_name)"""
        user_ids = self.find_steam_user_ids()
        if not user_ids:
            messagebox.showerror("错误", "未找到 Steam 用户配置")
            return 0, ""

        use_pw = self.server_type.get() == "perfectworld"
        server_name = "国服" if use_pw else "国际服"

        success_count = 0
        for user_id in user_ids:
            success, error = self.configure_launch_options(user_id, use_pw)
            if success:
                success_count += 1

        return success_count, server_name

    def on_write_only(self):
        """写入启动项，不启动游戏"""
        self.write_btn.text = "写入中..."
        self.write_btn.draw_button()
        self.root.update()

        try:
            if not self._ensure_steam_path():
                return

            success_count, server_name = self._configure_all_users()

            if success_count == 0:
                messagebox.showerror("配置失败", "无法配置启动项")
                return

            self.status_label.config(text=f"已配置{server_name}启动项", fg=COLORS["success"])
            messagebox.showinfo("完成", f"已成功配置{server_name}启动项\n共 {success_count} 个账号")

        except Exception as e:
            messagebox.showerror("错误", str(e))
        finally:
            self.write_btn.text = "写入启动项"
            self.write_btn.draw_button()
            self.status_label.config(fg=COLORS["text_muted"])

    def on_start_game(self):
        """写入启动项并启动游戏"""
        self.start_btn.text = "启动中..."
        self.start_btn.draw_button()
        self.root.update()

        try:
            if not self._ensure_steam_path():
                return

            success_count, server_name = self._configure_all_users()

            if success_count == 0:
                messagebox.showerror("配置失败", "无法配置启动项")
                return

            # 启动游戏
            self.status_label.config(text=f"正在启动 Dota 2...", fg=COLORS["success"])
            self.root.update()

            os.startfile("steam://rungameid/570")

            # 延迟关闭
            self.root.after(2000, self.root.destroy)

        except Exception as e:
            messagebox.showerror("错误", str(e))
            self.start_btn.text = "开始游戏"
            self.start_btn.draw_button()

    def find_steam_user_ids(self):
        """查找 Steam 用户 ID"""
        if not self.steam_path:
            return []
        userdata_path = os.path.join(self.steam_path, "userdata")
        if not os.path.exists(userdata_path):
            return []
        try:
            return [name for name in os.listdir(userdata_path)
                   if os.path.isdir(os.path.join(userdata_path, name))
                   and re.match(r'^\d+$', name)]
        except:
            return []

    def configure_launch_options(self, user_id, use_perfectworld):
        """配置启动选项"""
        try:
            config_path = os.path.join(self.steam_path, "userdata", user_id,
                                      "7", "remote", "sharedconfig.vdf")
            config_dir = os.path.dirname(config_path)

            if not os.path.exists(config_dir):
                os.makedirs(config_dir)

            # 读取现有配置
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 备份
                backup_path = f"{config_path}.backup.{datetime.now():%Y%m%d%H%M%S}"
                shutil.copy2(config_path, backup_path)

                # 修改启动项
                if use_perfectworld:
                    # 添加 -perfectworld（会先清理旧的）
                    content = self.add_launch_option(content, "-perfectworld")
                else:
                    # 国际服：移除 -perfectworld，不添加其他内容
                    content = self.remove_launch_option(content, "-perfectworld")

                with open(config_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            else:
                # 创建新配置（只有国服需要创建，国际服不需要任何配置）
                if use_perfectworld:
                    content = self.create_new_config(True)
                    with open(config_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                # 国际服且文件不存在：什么都不做

            return True, None

        except Exception as e:
            return False, str(e)

    def add_launch_option(self, content, option):
        """添加启动选项到 VDF"""
        # 先移除 -perfectworld（避免重复添加）
        content = self.remove_launch_option(content, "-perfectworld")

        # 查找 Dota 2 配置段
        dota_pattern = r'"570"\s*\{([^}]*)\}'
        match = re.search(dota_pattern, content, re.DOTALL)

        if match:
            # 已有 Dota 2 配置，修改 LaunchOptions
            section = match.group(1)
            if '"LaunchOptions"' in section:
                # 修改现有启动项
                new_section = re.sub(
                    r'("LaunchOptions"\s*")([^"]*)"',
                    lambda m: f'{m.group(1)}{option}"',
                    section
                )
            else:
                # 添加 LaunchOptions
                new_section = section.rstrip() + f'\n\t\t\t\t"LaunchOptions"\t\t"{option}"'

            content = content.replace(match.group(0), f'"570"\n\t\t\t\t{{{new_section}\n\t\t\t\t}}')
        else:
            # 添加新的 Dota 2 配置段
            new_app = f'''"570"
\t\t\t\t{{
\t\t\t\t\t"LaunchOptions"\t\t"{option}"
\t\t\t\t}}'''
            # 在 apps 段中添加
            content = re.sub(r'("apps"\s*\{)', r'\1\n\t\t\t\t' + new_app, content)

        return content

    def remove_launch_option(self, content, option):
        """从 VDF 移除启动选项（包括 LaunchOptions 字段）"""
        # 查找 Dota 2 配置段
        dota_pattern = r'"570"\s*\{([^}]*)\}'
        match = re.search(dota_pattern, content, re.DOTALL)

        if match and '"LaunchOptions"' in match.group(1):
            # 移除 LaunchOptions 整行
            section = match.group(1)
            new_section = re.sub(r'\s*"LaunchOptions"\s*"[^"]*"', '', section)
            content = content.replace(match.group(0), f'"570"\n\t\t\t\t{{{new_section}\n\t\t\t\t}}')

        # 清理多余空行
        content = re.sub(r'\n\n+', '\n', content)
        return content

    def create_new_config(self, use_perfectworld):
        """创建新的 VDF 配置"""
        launch_opt = "-perfectworld" if use_perfectworld else ""
        return f'''"UserRoamingConfigStore"
{{
\t"Software"
\t{{
\t\t"Valve"
\t{{
\t\t\t"Steam"
\t\t\t{{
\t\t\t\t"apps"
\t\t\t\t{{
\t\t\t\t\t"570"
\t\t\t\t\t{{
\t\t\t\t\t\t"LaunchOptions"\t\t"{launch_opt}"
\t\t\t\t\t}}
\t\t\t\t}}
\t\t\t}}
\t\t}}
\t}}
}}
'''


def main():
    root = tk.Tk()

    # 设置 DPI 感知
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass

    app = Dota2Launcher(root)
    root.mainloop()


if __name__ == "__main__":
    main()

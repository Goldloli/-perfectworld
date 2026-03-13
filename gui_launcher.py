#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dota 2 国服启动器 - CS 风格 GUI 版本
"""

import os
import sys
import re
import subprocess
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# Dota 2 AppID
DOTA2_APPID = "570"


class ModernButton(tk.Canvas):
    """现代风格的按钮"""
    def __init__(self, parent, text, command=None, width=200, height=50,
                 bg_color="#4a4a4a", hover_color="#5a5a5a", text_color="white", **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bg=parent["bg"], **kwargs)

        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.text = text
        self.command = command
        self.is_hovered = False

        self.draw_button()

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def draw_button(self):
        self.delete("all")
        color = self.hover_color if self.is_hovered else self.bg_color

        # 绘制圆角矩形背景
        self.create_rectangle(2, 2, self.winfo_reqwidth()-2, self.winfo_reqheight()-2,
                             fill=color, outline="#6a6a6a", width=2)

        # 绘制文字
        self.create_text(self.winfo_reqwidth()//2, self.winfo_reqheight()//2,
                        text=self.text, fill=self.text_color,
                        font=("Microsoft YaHei", 14, "bold"))

    def on_enter(self, event):
        self.is_hovered = True
        self.draw_button()
        self.config(cursor="hand2")

    def on_leave(self, event):
        self.is_hovered = False
        self.draw_button()
        self.config(cursor="")

    def on_click(self, event):
        if self.command:
            self.command()


class RadioOption(tk.Frame):
    """自定义单选选项"""
    def __init__(self, parent, title, subtitle, value, variable, **kwargs):
        super().__init__(parent, bg="#2a2a2a", **kwargs)

        self.value = value
        self.variable = variable

        # 左侧选择圆圈
        self.circle_canvas = tk.Canvas(self, width=24, height=24, bg="#2a2a2a",
                                      highlightthickness=0)
        self.circle_canvas.pack(side=tk.LEFT, padx=(0, 15))
        self.draw_circle()

        # 文字区域
        text_frame = tk.Frame(self, bg="#2a2a2a")
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 标题（参数名）
        self.title_label = tk.Label(text_frame, text=title, bg="#2a2a2a",
                                   fg="#cccccc", font=("Microsoft YaHei", 11),
                                   anchor="w")
        self.title_label.pack(fill=tk.X)

        # 副标题（说明）
        self.subtitle_label = tk.Label(text_frame, text=subtitle, bg="#2a2a2a",
                                      fg="#888888", font=("Microsoft YaHei", 10),
                                      anchor="w", wraplength=400, justify=tk.LEFT)
        self.subtitle_label.pack(fill=tk.X, pady=(3, 0))

        # 绑定点击事件
        for widget in [self, self.circle_canvas, text_frame, self.title_label, self.subtitle_label]:
            widget.bind("<Button-1>", self.select)
            widget.bind("<Enter>", self.on_enter)
            widget.bind("<Leave>", self.on_leave)

        # 跟踪变量变化
        self.variable.trace_add("write", self.update_state)

    def draw_circle(self):
        self.circle_canvas.delete("all")
        selected = self.variable.get() == self.value

        # 外圈
        self.circle_canvas.create_oval(2, 2, 22, 22, outline="#666666", width=2)

        # 内圆（选中时显示）
        if selected:
            self.circle_canvas.create_oval(7, 7, 17, 17, fill="white", outline="")

    def select(self, event=None):
        self.variable.set(self.value)

    def update_state(self, *args):
        self.draw_circle()
        selected = self.variable.get() == self.value
        self.title_label.config(fg="white" if selected else "#cccccc")

    def on_enter(self, event):
        self.config(cursor="hand2")

    def on_leave(self, event):
        self.config(cursor="")


class Dota2Launcher:
    def __init__(self, root):
        self.root = root
        self.root.title("Dota 2 国服启动器")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a1a")

        # 居中窗口
        self.center_window()

        self.steam_path = None
        self.find_steam_path()

        # 选中的服务器类型
        self.server_type = tk.StringVar(value="perfectworld")

        self.create_ui()

    def center_window(self):
        """窗口居中"""
        self.root.update_idletasks()
        width = 700
        height = 500
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_ui(self):
        """创建 CS 风格的界面"""
        # 顶部渐变背景区域（模拟 CS 的背景图效果）
        header_frame = tk.Frame(self.root, bg="#0a0a0a", height=180)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        # Dota 2 Logo/标题区域
        logo_frame = tk.Frame(header_frame, bg="#0a0a0a")
        logo_frame.pack(pady=30)

        # 游戏手柄图标（用 Unicode 字符模拟）
        icon_label = tk.Label(logo_frame, text="🎮", bg="#0a0a0a", fg="white",
                             font=("Arial", 48))
        icon_label.pack(side=tk.LEFT, padx=(0, 15))

        # 标题
        title_frame = tk.Frame(logo_frame, bg="#0a0a0a")
        title_frame.pack(side=tk.LEFT)

        title = tk.Label(title_frame, text="Dota 2", bg="#0a0a0a", fg="white",
                        font=("Microsoft YaHei", 28, "bold"))
        title.pack(anchor="w")

        subtitle = tk.Label(title_frame, text="启动配置", bg="#0a0a0a", fg="#888888",
                           font=("Microsoft YaHei", 14))
        subtitle.pack(anchor="w")

        # 提示文字
        hint = tk.Label(header_frame, text="请选择您欲进行游戏的方式：",
                       bg="#0a0a0a", fg="#aaaaaa", font=("Microsoft YaHei", 11))
        hint.pack(pady=(10, 0))

        # 主内容区域
        content_frame = tk.Frame(self.root, bg="#1a1a1a")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

        # 国服选项
        self.option_pw = RadioOption(
            content_frame,
            title="-perfectworld",
            subtitle="在低延迟的国服服务器上游玩，并使用您蒸汽平台帐户内的钱包资金消费。",
            value="perfectworld",
            variable=self.server_type
        )
        self.option_pw.pack(fill=tk.X, pady=8)

        # 国际服选项
        self.option_ww = RadioOption(
            content_frame,
            title="国际服",
            subtitle="在中国境外的服务器上游玩，并使用您Steam 帐户内的钱包资金消费。可能会造成丢包卡顿等众多网络问题。",
            value="worldwide",
            variable=self.server_type
        )
        self.option_ww.pack(fill=tk.X, pady=8)

        # 底部区域
        bottom_frame = tk.Frame(self.root, bg="#1a1a1a", height=100)
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)
        bottom_frame.pack_propagate(False)

        # 按钮容器
        btn_frame = tk.Frame(bottom_frame, bg="#1a1a1a")
        btn_frame.pack(expand=True)

        # 写入启动项按钮
        self.write_btn = ModernButton(
            btn_frame,
            text="[ 写入启动项 ]",
            command=self.on_write_only,
            width=150,
            height=45,
            bg_color="#3a3a3a",
            hover_color="#4a4a4a"
        )
        self.write_btn.pack(side=tk.LEFT, padx=10)

        # 开始游戏按钮
        self.start_btn = ModernButton(
            btn_frame,
            text="[ 开始游戏 ]",
            command=self.on_start_game,
            width=150,
            height=45,
            bg_color="#5a4a3a",
            hover_color="#6a5a4a"
        )
        self.start_btn.pack(side=tk.LEFT, padx=10)

        # 状态栏
        self.status_label = tk.Label(self.root,
                                    text=self.get_status_text(),
                                    bg="#1a1a1a", fg="#666666",
                                    font=("Microsoft YaHei", 9))
        self.status_label.pack(side=tk.BOTTOM, pady=5)

    def get_status_text(self):
        if self.steam_path:
            return f"已检测到 Steam: {self.steam_path}"
        return "未自动检测到 Steam 路径，启动时会提示选择"

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

    def on_start(self):
        """点击开始按钮"""
        self.start_btn.text = "[ 配置中... ]"
        self.start_btn.draw_button()
        self.root.update()

        try:
            # 选择 Steam 路径（如果需要）
            if not self.steam_path:
                from tkinter import filedialog
                path = filedialog.askdirectory(title="选择 Steam 目录（包含 steam.exe）")
                if not path or not os.path.exists(os.path.join(path, "steam.exe")):
                    messagebox.showerror("错误", "未找到 steam.exe")
                    return
                self.steam_path = path

            # 查找用户 ID
            user_ids = self.find_steam_user_ids()
            if not user_ids:
                messagebox.showerror("错误", "未找到 Steam 用户配置")
                return

            # 给所有检测到的账号设置启动项
            use_pw = self.server_type.get() == "perfectworld"
            server_name = "国服" if use_pw else "国际服"

            success_count = 0
            for user_id in user_ids:
                success, error = self.configure_launch_options(user_id, use_pw)
                if success:
                    success_count += 1

            if success_count == 0:
                messagebox.showerror("配置失败", "无法配置启动项")
                return

            # 启动游戏
            self.status_label.config(text=f"已配置{server_name}，正在启动 Dota 2...", fg="#00aa00")
            self.root.update()

            os.startfile("steam://rungameid/570")

            # 延迟关闭
            self.root.after(2000, self.root.destroy)

        except Exception as e:
            messagebox.showerror("错误", str(e))
            self.start_btn.text = "[ 开始 ]"
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
                    if '-perfectworld' not in content.lower():
                        # 添加 perfectworld
                        content = self.add_launch_option(content, "-perfectworld")
                else:
                    # 移除 perfectworld
                    content = self.remove_launch_option(content, "-perfectworld")

                with open(config_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            else:
                # 创建新配置
                content = self.create_new_config(use_perfectworld)
                with open(config_path, 'w', encoding='utf-8') as f:
                    f.write(content)

            return True, None

        except Exception as e:
            return False, str(e)

    def add_launch_option(self, content, option):
        """添加启动选项到 VDF"""
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
                    lambda m: f'{m.group(1)}{option} {m.group(2)}"'.strip(),
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
        """从 VDF 移除启动选项"""
        # 移除 perfectworld 但保留其他选项
        content = re.sub(r'\s*' + option + r'\s*', ' ', content, flags=re.IGNORECASE)
        content = re.sub(r'\s+', ' ', content)  # 清理多余空格
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

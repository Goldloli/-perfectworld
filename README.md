# 🎮 Dota 2 国服启动器

一款简洁优雅的 Dota 2 启动工具，帮助你一键配置国服启动项。

![截图](screenshot.png)

## ✨ 特点

- 🎨 **现代化界面** - 扁平化深色主题，卡片式布局设计
- ⚡ **一键配置** - 自动添加/移除 `-perfectworld` 启动项
- 🎮 **双模式启动** - 支持"仅写入配置"或"写入并启动游戏"
- 💾 **安全备份** - 每次修改前自动备份原配置
- 🔍 **智能检测** - 自动查找 Steam 安装路径，支持多账号
- 🏷️ **视觉标签** - 国服显示"推荐"标签，国际服显示"全球"标签

## 📦 下载

访问 [Releases](../../releases) 页面下载最新版本。

## 🚀 使用方法

1. 运行 `Dota2Launcher.exe`
2. 选择服务器：
   - **Perfect World 国服**: 低延迟，需要绑定完美世界账号
   - **Steam 国际服**: 全球服务器，可能有网络延迟
3. 点击按钮：
   - **仅写入启动项**: 只修改配置，不启动游戏
   - **开始游戏**: 修改配置并自动启动 Dota 2

## 🛠️ 从源码构建

```bash
# 安装依赖
pip install pyinstaller Pillow

# 生成图标（可选）
python generate_icon.py

# 构建可执行文件（带图标）
pyinstaller --onefile --windowed --name "Dota2Launcher" --icon=icon.ico gui_launcher.py

# 输出位置: dist/Dota2Launcher.exe
```

## 📋 项目结构

```
.
├── gui_launcher.py           # 主程序源码
├── generate_icon.py          # 图标生成脚本
├── .github/workflows/        # GitHub Actions 配置
└── README.md                 # 本文件
```

## ⚠️ 注意事项

- 建议在 Steam 关闭状态下运行本工具
- 工具会自动备份原配置，无需担心
- 国服需要绑定完美世界账号

## 📄 协议

MIT License

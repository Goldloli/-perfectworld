# 🎮 Dota 2 国服启动器

一款简洁优雅的 Dota 2 启动工具，帮助你一键配置国服启动项。

![截图](screenshot.png)

## ✨ 特点

- 🎨 **现代化界面** - 类似 CS 启动器的深色主题设计
- ⚡ **一键配置** - 自动添加/移除 `-perfectworld` 启动项
- 🎮 **自动启动** - 配置完成后自动启动 Dota 2
- 💾 **安全备份** - 每次修改前自动备份原配置
- 🔍 **智能检测** - 自动查找 Steam 安装路径

## 📦 下载

访问 [Releases](../../releases) 页面下载最新版本。

## 🚀 使用方法

1. 运行 `Dota2Launcher.exe`
2. 选择服务器：
   - **-perfectworld**: 国服（低延迟，推荐）
   - **-worldwide**: 国际服
3. 点击 **[ 开始 ]** 按钮
4. 程序会自动配置并启动 Dota 2

## 🛠️ 从源码构建

```bash
# 安装依赖
pip install pyinstaller

# 构建可执行文件
pyinstaller --onefile --windowed --name "Dota2Launcher" gui_launcher.py

# 输出位置: dist/Dota2Launcher.exe
```

## 📋 项目结构

```
.
├── gui_launcher.py           # 主程序源码
├── .github/workflows/        # GitHub Actions 配置
└── README.md                 # 本文件
```

## ⚠️ 注意事项

- 建议在 Steam 关闭状态下运行本工具
- 工具会自动备份原配置，无需担心
- 国服需要绑定完美世界账号

## 📄 协议

MIT License

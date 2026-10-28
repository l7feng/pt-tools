# Pro Tools 工具箱

版本：4.2.2。

扫描 Pro Tools 工程、导出音频和整理交付包。发行包内置 Python、PTSL 客户端及技能脚本。

## 下载与使用

在 [GitHub Releases](https://github.com/l7feng/pt-tools/releases) 下载对应 Windows x64 ZIP，完整解压后打开中文名称的 EXE。详细依赖和验证边界见 [使用说明](packaging/使用说明.md)。

## 源码构建

安装 Python 3.12、PyInstaller、pywebview、pyaaf2；PT 构建另需 py-ptsl 602.0.0。运行 `python tools/v4_pack/build_v4.py pt --out-root build/output`。具体构建版本见 `packaging/build-requirements.txt`。

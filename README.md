# Android Remote Control

## 简介 / Introduction
Android Remote Control 是一个基于 ADB 和 Scrcpy 的远程 Android 设备控制工具。通过简单的安装和配置，您可以轻松管理和远程控制多台 Android 设备。

Android Remote Control is a remote Android device control tool based on ADB and Scrcpy. With simple installation and configuration, you can easily manage and control multiple Android devices remotely.

## 特点 / Features
- 自动安装 ADB 和 Scrcpy 到项目的 `tools` 目录
- 配置环境变量，方便直接调用 `adb` 和 `scrcpy`
- 支持多设备管理和设备状态显示
- 一键启动，无需手动操作

## 环境要求 / Requirements
- 系统支持 / Supported OS: Windows / macOS / Linux
- Python 版本 / Python Version: >= 3.7

## 安装 / Installation

### 克隆项目 / Clone the Project
```bash
git clone https://github.com/yunze7373/Android-remote-control.git
cd Android-remote-control
```

### 一键安装 / One-click Installation
运行以下命令来安装所需的依赖和工具：
```bash
python install.py
```

安装完成后，ADB 和 Scrcpy 将自动安装到 tools 目录，并配置到系统环境变量中。

## 使用方法 / Usage

### 启动主程序 / Run the Main Program
```bash
python remote.py
```

根据提示选择设备并进行操作。

## 项目结构 / Project Structure
- `install.py`: 一键安装脚本，自动下载和配置 ADB 与 Scrcpy
- `remote.py`: 主程序，用于管理和控制设备
- `devices_example.txt`: 示例设备列表模板
- `tools/`: 包含 ADB 和 Scrcpy 的工具目录

## 开发者须知 / Developer Notes

### 设备列表文件 / Device List File
- `devices_example.txt` 是设备列表的模板文件
- 首次运行程序时，脚本会自动生成 `devices.txt`
- 如果您有自定义设备列表，请将其保存为 `devices.txt` 并确保其不被提交到版本控制

### 环境变量 / Environment Variables
- 程序会自动将 ADB 和 Scrcpy 的路径添加到系统环境变量中
- 若环境变量未生效，请手动重新启动终端

## 更新日志 / Changelog

### v1.0.0
- 实现设备管理功能
- 支持 ADB 和 Scrcpy 的自动安装
- 增加用户界面菜单

## 许可证 / License
本项目基于 MIT License 发布。  
This project is licensed under the MIT License.
import os
import platform
import subprocess
import shutil


def is_command_available(command):
    """检查命令是否可用"""
    return shutil.which(command) is not None


def install_adb_and_scrcpy():
    """
    检查并安装 ADB 和 Scrcpy 到同一目录
    """
    system = platform.system()
    print(f"检测到操作系统: {system}")

    tools_path = os.path.join(os.getcwd(), "tools")  # ADB 和 Scrcpy 的安装目录
    adb_path = os.path.join(tools_path, "platform-tools")  # ADB 解压后的目录
    scrcpy_path = os.path.join(tools_path, "scrcpy")  # Scrcpy 解压后的目录

    if not os.path.exists(tools_path):
        os.makedirs(tools_path)

    if is_command_available("adb") and is_command_available("scrcpy"):
        print("ADB 和 Scrcpy 已安装，跳过安装步骤。")
        return

    # 根据操作系统设置下载链接
    if system == "Windows":
        adb_url = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
        scrcpy_url = "https://github.com/Genymobile/scrcpy/releases/download/v2.0/scrcpy-win64-v2.0.zip"
    elif system == "Darwin":  # macOS
        adb_url = "https://dl.google.com/android/repository/platform-tools-latest-darwin.zip"
        scrcpy_url = "https://github.com/Genymobile/scrcpy/releases/download/v2.0/scrcpy-macos-v2.0.zip"
    elif system == "Linux":
        adb_url = "https://dl.google.com/android/repository/platform-tools-latest-linux.zip"
        scrcpy_url = "https://github.com/Genymobile/scrcpy/releases/download/v2.0/scrcpy-linux-v2.0.tar.gz"
    else:
        print("不支持的操作系统！")
        return False

    # 下载并安装 ADB
    print("检查并安装 ADB...")
    if not os.path.exists(adb_path):
        download_and_extract(adb_url, adb_path)
        print("ADB 安装完成。")
    else:
        print("ADB 已安装。")

    # 下载并安装 Scrcpy
    print("检查并安装 Scrcpy...")
    if not os.path.exists(scrcpy_path):
        download_and_extract(scrcpy_url, scrcpy_path)
        print("Scrcpy 安装完成。")
    else:
        print("Scrcpy 已安装。")

    # 配置环境变量
    set_environment_path(tools_path)
    print("环境变量配置完成。")


def download_and_extract(url, target_path):
    """
    下载并解压文件到指定路径
    """
    try:
        import requests
    except ImportError:
        print("请先安装 requests 模块: pip install requests")
        return

    import zipfile
    import tarfile

    local_file = target_path + (".zip" if "zip" in url else ".tar.gz")
    print(f"正在下载 {url} 到 {local_file}...")

    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(local_file, "wb") as file:
            shutil.copyfileobj(response.raw, file)

    print(f"{local_file} 下载完成，正在解压...")
    if local_file.endswith(".zip"):
        with zipfile.ZipFile(local_file, "r") as zip_ref:
            zip_ref.extractall(target_path)
    elif local_file.endswith(".tar.gz"):
        with tarfile.open(local_file, "r:gz") as tar_ref:
            tar_ref.extractall(target_path)

    os.remove(local_file)
    print(f"{target_path} 解压完成。")


def set_environment_path(tools_path):
    """
    添加工具目录到环境变量
    """
    system = platform.system()
    if system == "Windows":
        subprocess.run(f"setx PATH \"%PATH%;{tools_path}\"", shell=True)
    elif system in ["Darwin", "Linux"]:
        config_files = [os.path.expanduser("~/.bashrc"), os.path.expanduser("~/.zshrc"), os.path.expanduser("~/.bash_profile")]
        for config_file in config_files:
            if os.path.exists(config_file):
                with open(config_file, "a") as file:
                    file.write(f'\nexport PATH="{tools_path}:$PATH"\n')
        subprocess.run("source ~/.bashrc || source ~/.zshrc || source ~/.bash_profile", shell=True)


def verify_installation():
    """
    验证 ADB 和 Scrcpy 是否安装成功
    """
    print("正在验证 ADB 和 Scrcpy 是否安装成功...")
    try:
        subprocess.run(["adb", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["scrcpy", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("ADB 和 Scrcpy 安装成功！")
    except subprocess.CalledProcessError:
        print("验证失败，请检查安装过程或环境变量设置。")


def main():
    """
    一键部署入口
    """
    print("欢迎使用 Android Remote Control 一键部署工具！")
    install_adb_and_scrcpy()
    verify_installation()


if __name__ == "__main__":
    main()

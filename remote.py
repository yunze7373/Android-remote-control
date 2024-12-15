import os
import subprocess
import re
import time


def create_devices_file(file_path="devices.txt"):
    """
    如果设备列表文件不存在，则创建一个空的设备列表文件
    """
    if not os.path.exists(file_path):
        print(f"设备列表文件 {file_path} 不存在，正在创建...")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("# 格式: IP,设备名称\n")
            file.write("192.168.1.100:5555,Example\n")  # 示例设备
        print(f"文件已创建。请修改 {file_path} 文件以添加更多设备。\n")


def read_device_list(file_path="devices.txt"):
    """
    从文件中读取设备列表
    """
    devices = {}
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip() and not line.startswith("#"):  # 忽略空行和注释
                parts = line.strip().split(",")  # 假设文件格式为 "IP,设备名称"
                if len(parts) == 2:
                    ip, name = parts
                    devices[ip.strip()] = name.strip()
    return devices


def save_device_list(devices, file_path="devices.txt"):
    """
    保存设备列表到文件
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("# 格式: IP,设备名称\n")
        for ip, name in devices.items():
            file.write(f"{ip},{name}\n")


def is_valid_ip(ip):
    """
    检查 IP 地址或域名是否有效
    """
    # 匹配IP格式: xxx.xxx.xxx.xxx:端口
    ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}:\d{1,5}$"
    # 匹配域名格式: xxxxx.xxx:端口
    domain_pattern = r"^[a-zA-Z0-9.-]+:\d{1,5}$"
    return re.match(ip_pattern, ip) or re.match(domain_pattern, ip)


def get_connected_devices():
    """
    获取通过 ADB 已连接的设备
    """
    connected = {}
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, errors='ignore')
    lines = result.stdout.splitlines()[1:]  # 忽略第一行 "List of devices attached"
    
    for line in lines:
        if 'device' in line and 'offline' not in line:
            device = line.split('\t')[0]
            connected[device] = True  # 表示设备在线
    return connected


def connect_device(ip):
    """
    尝试通过 ADB 连接设备
    """
    print(f"尝试连接设备 {ip}...")
    result = subprocess.run(['adb', 'connect', ip], capture_output=True, text=True, errors='ignore')
    print(result.stdout)
    return "connected" in result.stdout.lower()


def start_scrcpy(device, name):
    """
    启动 Scrcpy 连接指定设备
    """
    print(f"正在启动 Scrcpy 控制设备 {name} ({device})...")
    os.system(f"scrcpy --tcpip={device} --no-audio")


def countdown(seconds=5):
    """
    倒计时提示
    """
    for i in range(seconds, 0, -1):
        print(f"\r即将开始操作，剩余时间: {i} 秒...", end="")
        time.sleep(1)
    print("\n")


def display_menu():
    """
    显示欢迎界面和菜单选项
    """
    print("=" * 50)
    print("              欢迎使用手机远程控制工具")
    print("=" * 50)
    print("[1] 查看并控制手机")
    print("[2] 修改设备信息（包括 IP 和名称）")
    print("[3] 添加新设备")
    print("[4] 删除设备")
    print("[5] 退出程序")
    choice = input("请输入你的选择: ")
    return choice


def display_device_status(all_devices, connected_devices):
    """
    显示设备的在线/离线状态
    """
    print("当前设备状态:")
    available_devices = []
    for i, (ip, name) in enumerate(all_devices.items(), 1):
        status = "在线" if ip in connected_devices else "离线"
        print(f"[{i}] {name} ({ip}) - {status}")
        available_devices.append((ip, name, status))
    return available_devices


def main():
    devices_file = "devices.txt"  # 保存设备列表的文件路径
    create_devices_file(devices_file)  # 确保文件存在

    while True:
        choice = display_menu()
        
        if choice == "1":
            # 查看并控制手机
            all_devices = read_device_list(devices_file)
            connected_devices = get_connected_devices()
            available_devices = display_device_status(all_devices, connected_devices)
            
            selected = input("请输入要控制的设备编号: ")
            if selected.isdigit() and 1 <= int(selected) <= len(available_devices):
                ip, name, status = available_devices[int(selected) - 1]
                if status == "离线":
                    print(f"{name} ({ip}) 当前离线。")
                    reconnect = input("是否尝试重新连接？(y/n): ").strip().lower()
                    if reconnect == "y":
                        countdown(5)  # 倒计时 5 秒
                        if connect_device(ip):
                            print(f"{name} ({ip}) 连接成功！")
                            start_scrcpy(ip, name)
                        else:
                            print(f"无法连接到 {name} ({ip})。")
                elif status == "在线":
                    start_scrcpy(ip, name)
                else:
                    print("未知状态，无法操作。")
            else:
                print("无效的选择，请重新输入！")
        elif choice == "2":
            # 修改设备信息
            all_devices = read_device_list(devices_file)
            print("当前设备列表:")
            for i, (ip, name) in enumerate(all_devices.items(), 1):
                print(f"[{i}] {name} ({ip})")
            selected = input("请输入要修改的设备编号: ")
            if selected.isdigit() and 1 <= int(selected) <= len(all_devices):
                ip = list(all_devices.keys())[int(selected) - 1]
                new_ip = input(f"请输入新 IP (当前: {ip}, 按回车保留当前值): ").strip()
                if not new_ip:
                    new_ip = ip  # 保留当前 IP
                elif not is_valid_ip(new_ip):
                    print("无效的 IP 格式，请重新输入！")
                    continue
                new_name = input(f"请输入新设备名称 (当前: {all_devices[ip]}, 按回车保留当前值): ").strip()
                if not new_name:
                    new_name = all_devices[ip]  # 保留当前名称
                all_devices.pop(ip)
                all_devices[new_ip] = new_name
                save_device_list(all_devices, devices_file)
                print(f"设备信息已更新为: {new_ip} ({new_name})")
            else:
                print("无效的选择，请重新输入！")
    
        elif choice == "3":
            all_devices = read_device_list(devices_file)
            new_ip = input("请输入新设备的 IP 地址或域名 (格式如: xxx.xxx.xxx.xxx:端口 或 example.com:端口): ").strip()
            if not is_valid_ip(new_ip):
                print("无效的 IP 或域名格式，请重新输入！")
                continue
            if new_ip in all_devices:
                print(f"设备 {new_ip} 已存在！")
                continue
            new_name = input(f"请输入设备 {new_ip} 的名称: ").strip()
            if new_name:
                if connect_device(new_ip):
                    print(f"设备 {new_name} ({new_ip}) 已成功连接并添加！")
                    all_devices[new_ip] = new_name
                    save_device_list(all_devices, devices_file)  # 保存新设备到文件
                else:
                    force_add = input(f"设备 {new_name} ({new_ip}) 不在线，是否强制添加？(y/n): ").strip().lower()
                    if force_add == "y":
                        all_devices[new_ip] = new_name
                        save_device_list(all_devices, devices_file)  # 保存新设备到文件
                        print(f"设备 {new_name} ({new_ip}) 已成功添加！")
            else:
                print("设备名称不能为空，请重新输入！")

        elif choice == "4":
            # 删除设备
            all_devices = read_device_list(devices_file)
            print("当前设备列表:")
            for i, (ip, name) in enumerate(all_devices.items(), 1):
                print(f"[{i}] {name} ({ip})")
            selected = input("请输入要删除的设备编号: ")
            if selected.isdigit() and 1 <= int(selected) <= len(all_devices):
                ip = list(all_devices.keys())[int(selected) - 1]
                confirm = input(f"确认删除设备 {all_devices[ip]} ({ip}) 吗？(y/n): ").strip().lower()
                if confirm == "y":
                    all_devices.pop(ip)
                    save_device_list(all_devices, devices_file)
                    print(f"设备 {ip} 已成功删除！")
                else:
                    print("已取消删除操作。")
            else:
                print("无效的选择，请重新输入！")
        elif choice == "5":
            print("感谢使用，再见！")
            break
        else:
            print("无效的输入，请重新输入！")


if __name__ == "__main__":
    main()

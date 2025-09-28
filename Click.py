import pygetwindow as gw
import pyautogui
import os
import time
import sys
from typing import List, Tuple, Optional

def get_all_monitors() -> List[Tuple[int, int, int, int]]:
    """获取所有显示器的边界信息，返回(left, top, width, height)的列表"""
    monitors = []
    screen_info = pyautogui.size()
    screen_width, screen_height = screen_info

    # 获取所有显示器的工作区
    # 对于多显示器，pygetwindow可能返回组合的边界，我们需要解析
    if hasattr(gw, 'getMonitors'):
        # 某些版本的pygetwindow提供getMonitors方法
        for monitor in gw.getMonitors():
            monitors.append((monitor.left, monitor.top, monitor.width, monitor.height))
    else:
        # 否则使用pyautogui的信息并假设单显示器
        monitors.append((0, 0, screen_width, screen_height))

    return monitors

def print_monitor_info(monitors: List[Tuple[int, int, int, int]]):
    """打印所有显示器的信息"""
    print(f"检测到 {len(monitors)} 台显示器:")
    for i, (left, top, width, height) in enumerate(monitors):
        print(f"显示器 {i}: 位置=({left}, {top}), 尺寸={width}x{height}")

def is_window_on_monitor(window, monitor_idx: int, monitors: List[Tuple[int, int, int, int]]) -> bool:
    """检查窗口是否在指定的显示器上"""
    if monitor_idx < 0 or monitor_idx >= len(monitors):
        return False

    m_left, m_top, m_width, m_height = monitors[monitor_idx]
    m_right = m_left + m_width
    m_bottom = m_top + m_height

    # 检查窗口中心是否在显示器范围内
    w_center_x = window.left + window.width // 2
    w_center_y = window.top + window.height // 2

    return (m_left <= w_center_x < m_right) and (m_top <= w_center_y < m_bottom)

def find_and_activate_window_on_monitor(window_title: str, monitor_idx: int,
                                      monitors: List[Tuple[int, int, int, int]]) -> Optional[gw.Window]:
    """在指定显示器上查找并激活窗口"""
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        return None

    # 优先选择指定显示器上的窗口
    for window in windows:
        if is_window_on_monitor(window, monitor_idx, monitors):
            try:
                window.activate()
                print(f"已激活显示器 {monitor_idx} 上的窗口: {window_title}")
                return window
            except Exception as e:
                print(f"激活窗口时出错: {e}")

    # 如果指定显示器上没有找到，尝试激活第一个找到的窗口
    window = windows[0]
    try:
        window.activate()
        print(f"已激活窗口: {window_title} (在显示器 {get_window_monitor(window, monitors)})")
        return window
    except Exception as e:
        print(f"激活窗口时出错: {e}")
        return None

def get_window_monitor(window, monitors: List[Tuple[int, int, int, int]]) -> int:
    """获取窗口所在的显示器索引"""
    w_center_x = window.left + window.width // 2
    w_center_y = window.top + window.height // 2

    for i, (m_left, m_top, m_width, m_height) in enumerate(monitors):
        m_right = m_left + m_width
        m_bottom = m_top + m_height
        if (m_left <= w_center_x < m_right) and (m_top <= w_center_y < m_bottom):
            return i
    return 0  # 默认返回第一个显示器

def start_application_from_desktop(app_name: str, monitor_idx: int,
                                  monitors: List[Tuple[int, int, int, int]]) -> bool:
    """从桌面启动指定应用程序"""
    # 获取桌面路径
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    # 尝试不同的文件扩展名
    extensions = [".exe", ".lnk", ".bat"]
    app_path = None

    for ext in extensions:
        potential_path = os.path.join(desktop_path, f"{app_name}{ext}")
        if os.path.exists(potential_path):
            app_path = potential_path
            break

    if app_path:
        try:
            print(f"从 {app_path} 启动应用程序...")
            os.startfile(app_path)

            # 等待应用启动
            time.sleep(5)  # 可以根据实际启动速度调整
            return True
        except Exception as e:
            print(f"启动应用程序时出错: {e}")
            return False
    else:
        print(f"在桌面上未找到 {app_name} 的可执行文件")
        return False

def click_relative_to_window(window, x_ratio: float, y_ratio: float) -> bool:
    """相对于窗口点击指定比例位置"""
    if not window:
        print("无法点击，窗口不存在")
        return False

    try:
        # 获取窗口的位置和大小
        left, top = window.left, window.top
        width, height = window.width, window.height

        # 计算点击坐标（相对于窗口的比例位置）
        click_x = left + int(width * x_ratio)
        click_y = top + int(height * y_ratio)

        # 移动鼠标并点击
        pyautogui.moveTo(click_x, click_y, duration=0.5)
        pyautogui.click()
        print(f"已点击窗口相对位置: ({x_ratio}, {y_ratio})，绝对坐标: ({click_x}, {click_y})")
        return True
    except Exception as e:
        print(f"点击时出错: {e}")
        return False

def main(target_monitor_idx: int = 0):
    app_name = "BrownDust II"

    # 获取所有显示器信息
    monitors = get_all_monitors()
    print_monitor_info(monitors)

    # 检查目标显示器是否存在
    if target_monitor_idx < 0 or target_monitor_idx >= len(monitors):
        print(f"指定的显示器编号 {target_monitor_idx} 无效，使用默认显示器 0")
        target_monitor_idx = 0

    # 尝试在指定显示器上查找并激活窗口
    window = find_and_activate_window_on_monitor(app_name, target_monitor_idx, monitors)

    # 如果未找到窗口，则从桌面启动
    if not window:
        print(f"在显示器 {target_monitor_idx} 上未找到 {app_name} 窗口，尝试启动应用程序...")
        if start_application_from_desktop(app_name, target_monitor_idx, monitors):
            # 再次尝试查找窗口
            window = find_and_activate_window_on_monitor(app_name, target_monitor_idx, monitors)
            if not window:
                print("启动后仍未找到窗口，程序退出")
                sys.exit(1)

    # 点击相对于窗口的指定坐标（这里使用比例，0.5,0.5表示中心）
    # 你可以根据需要修改这些值，例如(0.2, 0.3)表示左侧20%，顶部30%的位置
    click_relative_to_window(window, 0.5, 0.5)

if __name__ == "__main__":
    # 可以通过命令行参数指定显示器编号，默认为0
    target_monitor = 0
    if len(sys.argv) > 1:
        try:
            target_monitor = int(sys.argv[1])
        except ValueError:
            print("显示器编号必须是整数，使用默认值0")

    # 防止鼠标失控，提供10秒的准备时间
    print(f"程序将在10秒后开始执行，操作显示器 {target_monitor}...")
    time.sleep(10)
    main(target_monitor)

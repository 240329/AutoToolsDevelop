import pygetwindow as gw
import pyautogui
import os
import time
import tkinter as tk
from tkinter import messagebox
from screeninfo import get_monitors  # 用于获取多显示器信息
import Click

class BrownDustTool:
    def __init__(self):
        self.window_title = "飞书"
        self.window = None
        self.running = False
        self.coordinate_window = None
        self.monitors = get_monitors()  # 获取所有显示器信息

    def find_window(self):
        """查找并返回名为BrownDust II的窗口"""
        windows = gw.getWindowsWithTitle(self.window_title)
        if windows:
            return windows[0]
        return None

    def activate_window(self):
        """激活BrownDust II窗口，如果未找到则从桌面启动"""
        self.window = self.find_window()

        if self.window:
            try:
                self.window.activate()
                time.sleep(0.5)
                return True
            except Exception as e:
                print(f"激活窗口时出错: {e}")
                return False
        else:
            print(f"未找到{self.window_title}窗口，尝试从桌面启动...")
            return self.launch_from_desktop()

    def launch_from_desktop(self):
        app_path = ''
        if os.path.exists(app_path):
            try:
                os.startfile(app_path)
                print(f"已从{app_path}启动程序")

                # 等待程序启动
                print("等待程序启动...")
                for _ in range(30):
                    time.sleep(1)
                    self.window = self.find_window()
                    if self.window:
                        self.window.activate()
                        return True

                print("程序启动超时")
                return False
            except Exception as e:
                print(f"启动程序时出错: {e}")
                return False

        print(f"在桌面上未找到{self.window_title}程序")
        return False

    def get_relative_coordinates(self, x, y):
        """计算鼠标位置相对于窗口的坐标"""
        if not self.window:
            return None

        try:
            window_left, window_top = self.window.topleft
            rel_x = x - window_left
            rel_y = y - window_top
            return (rel_x, rel_y)
        except Exception as e:
            print(f"计算相对坐标时出错: {e}")
            return None

    def get_monitor_info(self, x, y):
        """获取鼠标所在的显示器编号和显示器信息"""
        for i, monitor in enumerate(self.monitors, 1):  # 显示器编号从1开始
            # 检查坐标是否在当前显示器范围内
            if (monitor.x <= x <= monitor.x + monitor.width and
                    monitor.y <= y <= monitor.y + monitor.height):
                return {
                    "monitor_id": i,
                    "width": monitor.width,
                    "height": monitor.height,
                    "x": monitor.x,
                    "y": monitor.y
                }
        return None  # 未找到对应显示器

    def get_window_percentage(self, rel_x, rel_y):
        """计算相对于目标窗口的百分比坐标"""
        if not self.window or rel_x is None or rel_y is None:
            return None

        try:
            # 获取窗口的宽高
            window_width, window_height = self.window.size

            # 防止除以零错误
            if window_width == 0 or window_height == 0:
                return None

            # 计算百分比（保留两位小数）
            percent_x = round((rel_x / window_width) * 100, 2)
            percent_y = round((rel_y / window_height) * 100, 2)

            return (percent_x, percent_y)
        except Exception as e:
            print(f"计算窗口百分比坐标时出错: {e}")
            return None

    def on_click(self, event):
        """鼠标点击事件处理函数（包含相对窗口百分比坐标）"""
        if not self.window:
            messagebox.showwarning("警告", "未找到目标窗口")
            return

        # 获取鼠标在屏幕上的绝对坐标
        abs_x, abs_y = pyautogui.position()

        # 获取显示器信息
        monitor_info = self.get_monitor_info(abs_x, abs_y)
        monitor_id = monitor_info["monitor_id"] if monitor_info else "未知"

        # 计算相对窗口坐标
        rel_window_coords = self.get_relative_coordinates(abs_x, abs_y)

        # 计算相对窗口百分比坐标
        window_percent = None
        if rel_window_coords:
            rel_x, rel_y = rel_window_coords
            window_percent = self.get_window_percentage(rel_x, rel_y)

        # 构建坐标信息文本
        coord_text = [
            f"绝对坐标: ({abs_x}, {abs_y})",
            f"所在显示器: {monitor_id}"
        ]

        if rel_window_coords:
            coord_text.append(f"相对窗口坐标: ({rel_x}, {rel_y})")

        if window_percent:
            percent_x, percent_y = window_percent
            coord_text.append(f"相对窗口百分比: ({percent_x}%, {percent_y}%)")

        # 显示和打印坐标信息
        result_text = "\n".join(coord_text)
        messagebox.showinfo("坐标信息", result_text)
        print(result_text)
        self.coordinate_window.bind("<Escape>", lambda e: self.stop_listener())
        pyautogui.click(abs_x, abs_y)

    def start_coordinate_listener(self):
        """启动鼠标点击监听器"""
        self.running = True

        self.coordinate_window = tk.Tk()
        self.coordinate_window.title(f"{self.window_title}坐标工具")
        self.coordinate_window.attributes("-alpha", 0.3)
        self.coordinate_window.attributes("-topmost", True)
        self.coordinate_window.geometry("400x400")

        # 更新说明文本，反映当前功能
        label = tk.Label(
            self.coordinate_window,
            text="点击屏幕任意位置获取坐标\n包含绝对坐标、显示器编号、相对窗口坐标和窗口百分比\n按ESC键退出"
        )
        label.pack(expand=True)

        self.coordinate_window.bind("<Button-1>", self.on_click)
        self.coordinate_window.bind("<Escape>", lambda e: self.stop_listener())

        self.coordinate_window.mainloop()

    def stop_listener(self):
        """停止监听器"""
        self.running = False
        if self.coordinate_window:
            self.coordinate_window.destroy()
        print("坐标监听已停止")

    def run(self):
        """运行工具主流程"""
        if not self.activate_window():
            print("无法激活或启动目标窗口，程序退出")
            return

        print(f"成功找到并激活{self.window_title}窗口")
        print(f"检测到{len(self.monitors)}个显示器")
        print("窗口位置:", self.window.topleft)
        print("窗口大小:", self.window.size)
        print("请点击屏幕上的位置来获取坐标，按ESC键退出")

        self.start_coordinate_listener()


if __name__ == "__main__":
    pyautogui.FAILSAFE = True

    # 检查并提示安装必要的库
    try:
        import screeninfo
    except ImportError:
        print("检测到缺少screeninfo库，正在尝试安装...")
        os.system("pip install screeninfo")
        import screeninfo

    tool = BrownDustTool()
    tool.run()
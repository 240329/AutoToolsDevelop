import pyautogui as pg
import time

class Check:
    def __init__(self):
        self.max_times = 10
        self.number_of_attempts = 0
    def unlimited_check(self,name):
        while True:
            # 在屏幕上寻找开始按钮
            try:
                button_location = pg.locateOnScreen(name, confidence=0.8)  # confidence是匹配度，0.8表示80%相似
                if button_location is not None:
                    print("Success!")
                    return True
            except:
                self.number_of_attempts += 1
                print(f"The {self.number_of_attempts} time attempt Fail")
                if self.number_of_attempts >= self.max_times:
                    return False
                time.sleep(0.5)  # 每秒钟检测一次

    def limited_check(self,name):
        while True:
            if self.number_of_attempts >= self.max_times:
                return False
            # 在屏幕上寻找开始按钮
            button_location = pg.locateOnScreen(name, confidence=0.8)  # confidence是匹配度，0.8表示80%相似
            if button_location is not None:
                print("Success!")
                return True
            # time.sleep(0.5)  # 每秒钟检测一次
            self.number_of_attempts += 1

if __name__ == "__main__":
    checker = Check()
    checker.unlimited_check(name="./asset/unread.png")
import tkinter as tk
from tkinter import ttk, messagebox


class BD2BotUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BD2Bot")
        self.root.geometry("600x800")
        self.root.resizable(False, False)

        # 创建主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 创建滚动条
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.initUI()

    def initUI(self):
        # 日常部分
        self.create_daily_section()

        # 周常部分
        self.create_weekly_section()

        # 跑图部分
        self.create_run_map_section()

        # 特殊任务部分
        self.create_special_section()

        # 设置互斥逻辑
        self.setup_mutual_exclusion()

    def create_daily_section(self):
        daily_frame = ttk.LabelFrame(self.scrollable_frame, text="日常", padding="10")
        daily_frame.pack(fill=tk.X, pady=5)

        self.daily_vars = {}

        # 日常选项
        daily_options = [
            "扫荡", "狩猎场选择", "木材", "金矿", "圣石洞穴属性图选择",
            "水", "火", "风", "光", "暗", "活动图", "抽卡", "角色", "武器",
            "邮件", "普通", "商品", "装备制作强化分解", "领取日常任务奖励",
            "公会签到", "餐馆结算", "常客圣石领取", "领取通行证奖励",
            "肉鸽塔每日快速战斗（默认关闭）"
        ]

        for option in daily_options:
            var = tk.BooleanVar(value=True)
            cb = ttk.Checkbutton(daily_frame, text=option, variable=var)
            cb.pack(anchor="w")
            self.daily_vars[option] = var

        # PVP特殊处理
        pvp_frame = ttk.Frame(daily_frame)
        pvp_frame.pack(fill=tk.X, pady=2)

        self.pvp_var = tk.BooleanVar(value=True)
        pvp_cb = ttk.Checkbutton(pvp_frame, text="PVP", variable=self.pvp_var)
        pvp_cb.pack(side=tk.LEFT)

        self.pvp_text = ttk.Entry(pvp_frame, width=10)
        self.pvp_text.insert(0, "0")
        self.pvp_text.pack(side=tk.LEFT, padx=5)

        ttk.Label(pvp_frame, text="次").pack(side=tk.LEFT)

    def create_weekly_section(self):
        weekly_frame = ttk.LabelFrame(self.scrollable_frame, text="周常", padding="10")
        weekly_frame.pack(fill=tk.X, pady=5)

        self.weekly_vars = {}
        weekly_options = ["三次点赞", "街机", "一次末日"]

        for option in weekly_options:
            var = tk.BooleanVar(value=True)
            cb = ttk.Checkbutton(weekly_frame, text=option, variable=var)
            cb.pack(anchor="w")
            self.weekly_vars[option] = var

    def create_run_map_section(self):
        run_frame = ttk.LabelFrame(self.scrollable_frame, text="跑图", padding="10")
        run_frame.pack(fill=tk.X, pady=5)

        self.run_vars = {}
        run_options = ["是否跑商", "是否完成城镇任务"]

        for option in run_options:
            var = tk.BooleanVar(value=True)
            cb = ttk.Checkbutton(run_frame, text=option, variable=var)
            cb.pack(anchor="w")
            self.run_vars[option] = var

    def create_special_section(self):
        special_frame = ttk.LabelFrame(self.scrollable_frame, text="特殊任务", padding="10")
        special_frame.pack(fill=tk.X, pady=5)

        # 末日选项
        doom_frame = ttk.Frame(special_frame)
        doom_frame.pack(fill=tk.X, pady=2)

        self.special_var = tk.StringVar()
        self.doom_radio = ttk.Radiobutton(doom_frame, text="末日", variable=self.special_var, value="doom")
        self.doom_radio.pack(side=tk.LEFT)

        self.doom_text = ttk.Entry(doom_frame, width=10)
        self.doom_text.insert(0, "0")
        self.doom_text.pack(side=tk.LEFT, padx=5)

        ttk.Label(doom_frame, text="次").pack(side=tk.LEFT)

        # 分隔线
        separator = ttk.Separator(special_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=5)

        # 刷粉选项
        self.powder_radio = ttk.Radiobutton(special_frame, text="刷粉", variable=self.special_var, value="powder")
        self.powder_radio.pack(anchor="w")

        # 刷粉详细选项
        powder_frame = ttk.Frame(special_frame)
        powder_frame.pack(fill=tk.X, padx=20, pady=5)

        self.use_wood_var = tk.BooleanVar(value=True)
        use_wood_cb = ttk.Checkbutton(powder_frame, text="是否使用木头", variable=self.use_wood_var)
        use_wood_cb.pack(anchor="w")

        self.use_rice_var = tk.BooleanVar(value=True)
        use_rice_cb = ttk.Checkbutton(powder_frame, text="是否使用米饭", variable=self.use_rice_var)
        use_rice_cb.pack(anchor="w")

        # 强化等级
        enhance_level_frame = ttk.Frame(powder_frame)
        enhance_level_frame.pack(fill=tk.X, pady=2)

        ttk.Label(enhance_level_frame, text="强化等级:").pack(side=tk.LEFT)
        self.enhance_level_text = ttk.Entry(enhance_level_frame, width=10)
        self.enhance_level_text.insert(0, "0")
        self.enhance_level_text.pack(side=tk.LEFT, padx=5)

        # 强化次数
        enhance_count_frame = ttk.Frame(powder_frame)
        enhance_count_frame.pack(fill=tk.X, pady=2)

        ttk.Label(enhance_count_frame, text="强化次数:").pack(side=tk.LEFT)
        self.enhance_count_text = ttk.Entry(enhance_count_frame, width=10)
        self.enhance_count_text.insert(0, "0")
        self.enhance_count_text.pack(side=tk.LEFT, padx=5)

    def setup_mutual_exclusion(self):
        # 绑定事件
        self.doom_radio.configure(command=self.on_special_toggled)
        self.powder_radio.configure(command=self.on_special_toggled)

        # 为所有日常、周常、跑图复选框绑定事件
        for var in list(self.daily_vars.values()) + list(self.weekly_vars.values()) + list(self.run_vars.values()):
            # 由于tkinter的BooleanVar没有直接绑定命令的方式，我们需要在每次改变时检查
            pass

    def on_special_toggled(self):
        special_selected = self.special_var.get() in ["doom", "powder"]

        # 启用或禁用日常、周常、跑图部分
        state = "normal" if not special_selected else "false"

        # 更新所有复选框状态
        for widget in self.scrollable_frame.winfo_children():
            if isinstance(widget, ttk.LabelFrame) and widget.cget("text") in ["日常", "周常", "跑图"]:
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Checkbutton):
                        child.configure(state=state)


def main():
    root = tk.Tk()
    app = BD2BotUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
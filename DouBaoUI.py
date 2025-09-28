import tkinter as tk
from tkinter import ttk


class BD2BotInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("BD2Bot")
        self.root.resizable(False, False)  # 固定窗口大小，不允许缩放

        # 创建变量存储各个选项的状态
        # 日常相关变量
        self.daily_var = tk.BooleanVar(value=True)
        self.sweep_var = tk.BooleanVar(value=True)
        self.hunting_ground_var = tk.BooleanVar(value=True)
        self.wood_var = tk.BooleanVar(value=True)
        self.gold_var = tk.BooleanVar(value=False)
        self.stone_var = tk.BooleanVar(value=True)
        self.water_var = tk.BooleanVar(value=True)
        self.fire_var = tk.BooleanVar(value=False)
        self.wind_var = tk.BooleanVar(value=False)
        self.light_var = tk.BooleanVar(value=False)
        self.dark_var = tk.BooleanVar(value=False)
        self.activity_map_var = tk.BooleanVar(value=True)
        self.gacha_var = tk.BooleanVar(value=True)
        self.character_var = tk.BooleanVar(value=True)
        self.weapon_var = tk.BooleanVar(value=True)
        self.arena_var = tk.BooleanVar(value=True)
        self.arena_count_var = tk.StringVar(value="0")
        self.mail_var = tk.BooleanVar(value=True)
        self.normal_mail_var = tk.BooleanVar(value=True)
        self.goods_mail_var = tk.BooleanVar(value=True)  # 商品
        self.equipment_var = tk.BooleanVar(value=True)
        self.daily_quest_reward_var = tk.BooleanVar(value=True)
        self.guild_checkin_var = tk.BooleanVar(value=True)
        self.restaurant_settlement_var = tk.BooleanVar(value=True)
        self.daily_sacred_stone_var = tk.BooleanVar(value=True)
        self.pass_reward_var = tk.BooleanVar(value=True)
        self.pigeon_tower_var = tk.BooleanVar(value=True)

        # 周常相关变量
        self.weekly_var = tk.BooleanVar(value=True)

        # 跑图相关变量
        self.map_running_var = tk.BooleanVar(value=True)
        self.trade_var = tk.BooleanVar(value=True)
        self.town_quest_var = tk.BooleanVar(value=True)

        # 末日和刷粉相关变量
        self.doomsday_var = tk.BooleanVar(value=False)
        self.doomsday_count_var = tk.StringVar(value="0")
        self.shuafen_var = tk.BooleanVar(value=True)  # 刷粉
        self.use_wood_var = tk.BooleanVar(value=True)
        self.use_rice_var = tk.BooleanVar(value=True)
        self.qianghuadengji_var = tk.StringVar(value="0")  # 强化等级
        self.qianghuacishu_var = tk.StringVar(value="0")  # 强化次数

        # 创建界面组件
        self.create_widgets()

        # 绑定事件处理
        self.bind_events()

        # 初始状态更新
        self.update_daily_dependent_states()

    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 日常区域
        daily_frame = ttk.LabelFrame(main_frame, text="", padding="5")
        daily_frame.grid(row=0, column=0, sticky=tk.W, pady=5)

        # 第一行：日常、扫荡、狩猎场选择、木材、金矿
        ttk.Checkbutton(daily_frame, text="日常", variable=self.daily_var).grid(row=0, column=0, sticky=tk.W, padx=2)
        ttk.Checkbutton(daily_frame, text="扫荡", variable=self.sweep_var).grid(row=0, column=1, sticky=tk.W, padx=2)
        ttk.Checkbutton(daily_frame, text="狩猎场选择", variable=self.hunting_ground_var).grid(row=0, column=2,
                                                                                               sticky=tk.W, padx=2)
        ttk.Radiobutton(daily_frame, text="木材", variable=self.wood_var, value=True).grid(row=0, column=3, sticky=tk.W,
                                                                                           padx=2)
        ttk.Radiobutton(daily_frame, text="金矿", variable=self.wood_var, value=False).grid(row=0, column=4,
                                                                                            sticky=tk.W, padx=2)

        # 第二行：石头选择、水、火、风、光、暗
        ttk.Checkbutton(daily_frame, text="石头选择", variable=self.stone_var).grid(row=1, column=0, sticky=tk.W,
                                                                                    padx=2)
        ttk.Radiobutton(daily_frame, text="水", variable=self.water_var, value=True).grid(row=1, column=1, sticky=tk.W,
                                                                                          padx=2)
        ttk.Radiobutton(daily_frame, text="火", variable=self.water_var, value=False).grid(row=1, column=2, sticky=tk.W,
                                                                                           padx=2)
        ttk.Radiobutton(daily_frame, text="风", variable=self.wind_var, value=True).grid(row=1, column=3, sticky=tk.W,
                                                                                         padx=2)
        ttk.Radiobutton(daily_frame, text="光", variable=self.light_var, value=True).grid(row=1, column=4, sticky=tk.W,
                                                                                          padx=2)
        ttk.Radiobutton(daily_frame, text="暗", variable=self.dark_var, value=True).grid(row=1, column=5, sticky=tk.W,
                                                                                         padx=2)

        # 第三行：活动图
        ttk.Checkbutton(daily_frame, text="活动图", variable=self.activity_map_var).grid(row=2, column=0, sticky=tk.W,
                                                                                         padx=2)

        # 第四行：抽卡、角色、武器
        ttk.Checkbutton(daily_frame, text="抽卡", variable=self.gacha_var).grid(row=3, column=0, sticky=tk.W, padx=2)
        ttk.Checkbutton(daily_frame, text="角色", variable=self.character_var).grid(row=3, column=1, sticky=tk.W,
                                                                                    padx=2)
        ttk.Checkbutton(daily_frame, text="武器", variable=self.weapon_var).grid(row=3, column=2, sticky=tk.W, padx=2)

        # 第五行：竞技场
        arena_frame = ttk.Frame(daily_frame)
        arena_frame.grid(row=4, column=0, sticky=tk.W, padx=2)
        ttk.Checkbutton(arena_frame, text="竞技场", variable=self.arena_var).pack(side=tk.LEFT)
        ttk.Entry(arena_frame, textvariable=self.arena_count_var, width=5).pack(side=tk.LEFT, padx=5)
        ttk.Label(arena_frame, text="次").pack(side=tk.LEFT)

        # 第六行：邮件、普通、商品
        mail_frame = ttk.Frame(daily_frame)
        mail_frame.grid(row=5, column=0, sticky=tk.W, padx=2)
        ttk.Checkbutton(mail_frame, text="邮件", variable=self.mail_var).pack(side=tk.LEFT)
        ttk.Checkbutton(mail_frame, text="普通", variable=self.normal_mail_var).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(mail_frame, text="商品", variable=self.goods_mail_var).pack(side=tk.LEFT, padx=5)

        # 第七行：装备制作强化分解
        ttk.Checkbutton(daily_frame, text="装备制作强化分解", variable=self.equipment_var).grid(row=6, column=0,
                                                                                                sticky=tk.W, padx=2)

        # 第八行：领取日常任务奖励、公会签到、餐馆结算、日常圣石领取
        rewards_frame1 = ttk.Frame(daily_frame)
        rewards_frame1.grid(row=7, column=0, sticky=tk.W, padx=2)
        ttk.Checkbutton(rewards_frame1, text="领取日常任务奖励", variable=self.daily_quest_reward_var).pack(
            side=tk.LEFT)
        ttk.Checkbutton(rewards_frame1, text="公会签到", variable=self.guild_checkin_var).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(rewards_frame1, text="餐馆结算", variable=self.restaurant_settlement_var).pack(side=tk.LEFT,
                                                                                                       padx=5)
        ttk.Checkbutton(rewards_frame1, text="日常圣石领取", variable=self.daily_sacred_stone_var).pack(side=tk.LEFT,
                                                                                                        padx=5)

        # 第九行：领取通行证奖励
        ttk.Checkbutton(daily_frame, text="领取通行证奖励", variable=self.pass_reward_var).grid(row=8, column=0,
                                                                                                sticky=tk.W, padx=2)

        # 第十行：肉鸽塔每日快速战斗
        ttk.Checkbutton(daily_frame, text="肉鸽塔每日快速战斗（默认关闭）", variable=self.pigeon_tower_var).grid(row=9,
                                                                                                               column=0,
                                                                                                               sticky=tk.W,
                                                                                                               padx=2)

        # 周常区域
        weekly_frame = ttk.LabelFrame(main_frame, text="", padding="5")
        weekly_frame.grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Checkbutton(weekly_frame, text="周常", variable=self.weekly_var).pack(side=tk.LEFT)

        # 跑图区域
        map_frame = ttk.LabelFrame(main_frame, text="", padding="5")
        map_frame.grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Checkbutton(map_frame, text="跑图", variable=self.map_running_var).pack(side=tk.LEFT)
        ttk.Checkbutton(map_frame, text="是否跑商", variable=self.trade_var).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(map_frame, text="是否完成城镇任务", variable=self.town_quest_var).pack(side=tk.LEFT, padx=5)

        # 末日区域
        doomsday_frame = ttk.LabelFrame(main_frame, text="", padding="5")
        doomsday_frame.grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Radiobutton(doomsday_frame, text="末日", variable=self.doomsday_var, value=True).pack(side=tk.LEFT)
        ttk.Entry(doomsday_frame, textvariable=self.doomsday_count_var, width=5).pack(side=tk.LEFT, padx=5)
        ttk.Label(doomsday_frame, text="次").pack(side=tk.LEFT)

        # 刷粉区域
        powder_frame = ttk.LabelFrame(main_frame, text="", padding="5")
        powder_frame.grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Radiobutton(powder_frame, text="刷粉", variable=self.doomsday_var, value=False).pack(side=tk.LEFT)
        ttk.Checkbutton(powder_frame, text="是否使用木头", variable=self.use_wood_var).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(powder_frame, text="是否使用米饭", variable=self.use_rice_var).pack(side=tk.LEFT, padx=5)
        ttk.Label(powder_frame, text="强化等级").pack(side=tk.LEFT, padx=5)
        ttk.Entry(powder_frame, textvariable=self.qianghuadengji_var, width=5).pack(side=tk.LEFT)
        ttk.Label(powder_frame, text="强化次数").pack(side=tk.LEFT, padx=5)
        ttk.Entry(powder_frame, textvariable=self.qianghuacishu_var, width=5).pack(side=tk.LEFT)

        # 按钮区域
        button_frame = ttk.Frame(main_frame, padding="5")
        button_frame.grid(row=0, column=1, rowspan=5, padx=10, pady=5)
        ttk.Button(button_frame, text="执行", width=10).pack(fill=tk.X, pady=5)
        ttk.Button(button_frame, text="停止", width=10).pack(fill=tk.X, pady=5)

    def bind_events(self):
        # 绑定日常复选框事件
        self.daily_var.trace_add("write", lambda *args: self.update_daily_dependent_states())

        # 绑定末日/刷粉单选框事件
        self.doomsday_var.trace_add("write", lambda *args: self.update_mutual_exclusion())

        # 绑定日常、周常、跑图复选框事件
        self.daily_var.trace_add("write", lambda *args: self.update_mutual_exclusion())
        self.weekly_var.trace_add("write", lambda *args: self.update_mutual_exclusion())
        self.map_running_var.trace_add("write", lambda *args: self.update_mutual_exclusion())

    def update_daily_dependent_states(self):
        # 根据日常是否选中，更新依赖选项的状态
        state = tk.NORMAL if self.daily_var.get() else tk.DISABLED

        # 更新依赖日常的选项状态
        self.sweep_var.set(self.daily_var.get() and self.sweep_var.get())
        self.hunting_ground_var.set(self.daily_var.get() and self.hunting_ground_var.get())
        self.stone_var.set(self.daily_var.get() and self.stone_var.get())
        self.activity_map_var.set(self.daily_var.get() and self.activity_map_var.get())
        self.gacha_var.set(self.daily_var.get() and self.gacha_var.get())
        self.character_var.set(self.daily_var.get() and self.character_var.get())
        self.weapon_var.set(self.daily_var.get() and self.weapon_var.get())
        self.arena_var.set(self.daily_var.get() and self.arena_var.get())
        self.mail_var.set(self.daily_var.get() and self.mail_var.get())
        self.equipment_var.set(self.daily_var.get() and self.equipment_var.get())
        self.daily_quest_reward_var.set(self.daily_var.get() and self.daily_quest_reward_var.get())
        self.guild_checkin_var.set(self.daily_var.get() and self.guild_checkin_var.get())
        self.restaurant_settlement_var.set(self.daily_var.get() and self.restaurant_settlement_var.get())
        self.daily_sacred_stone_var.set(self.daily_var.get() and self.daily_sacred_stone_var.get())
        self.pass_reward_var.set(self.daily_var.get() and self.pass_reward_var.get())
        self.pigeon_tower_var.set(self.daily_var.get() and self.pigeon_tower_var.get())

        # 禁用/启用控件
        for child in self.root.winfo_children():
            for sub_child in child.winfo_children():
                if hasattr(sub_child, 'winfo_children'):
                    for widget in sub_child.winfo_children():
                        if widget.winfo_class() in ['TCheckbutton', 'TRadiobutton', 'TEntry']:
                            if widget not in [self.daily_var, self.weekly_var, self.map_running_var,
                                              self.doomsday_var, self.shuafen_var]:
                                widget.config(state=state)

    def update_mutual_exclusion(self):
        # 末日/刷粉 与 日常/周常/跑图 互斥
        if self.doomsday_var.get() or not self.shuafen_var.get():  # 如果选择了末日或刷粉
            # 禁用日常、周常、跑图
            self.daily_var.set(False)
            self.weekly_var.set(False)
            self.map_running_var.set(False)


        # 如果选择了日常、周常或跑图中的任何一个
        if self.daily_var.get() or self.weekly_var.get() or self.map_running_var.get():
            # 禁用末日和刷粉
            self.doomsday_var.set(False)
            self.shuafen_var.set(False)

if __name__ == "__main__":
    root = tk.Tk()
    app = BD2BotInterface(root)
    root.mainloop()

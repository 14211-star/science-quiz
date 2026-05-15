import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

class SpinnerTab:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#f8fafc")
        
        # 狀態變量
        self.min_val = tk.IntVar(value=1)
        self.max_val = tk.IntVar(value=34)
        self.count_val = tk.IntVar(value=1)
        self.no_repeat = tk.BooleanVar(value=True)
        self.animating = False
        
        self._build_ui()

    def _build_ui(self):
        # 顯示區域
        display_card = tk.Frame(self.frame, bg="#ffffff", padx=40, pady=40, 
                                highlightbackground="#e2e8f0", highlightthickness=1)
        display_card.pack(pady=20, padx=20, fill="both", expand=True)

        self.result_label = tk.Label(display_card, text="?", 
                                    font=("Microsoft JhengHei", 120, "bold"), 
                                    bg="#ffffff", fg="#2563eb")
        self.result_label.pack(expand=True)

        # 設定區域
        settings_frame = tk.Frame(self.frame, bg="#f8fafc", pady=10)
        settings_frame.pack()

        # 第一行：範圍
        range_frame = tk.Frame(settings_frame, bg="#f8fafc")
        range_frame.pack()
        
        tk.Label(range_frame, text="學號範圍：", font=("Microsoft JhengHei", 12), bg="#f8fafc").pack(side="left")
        ttk.Spinbox(range_frame, from_=1, to=1000, textvariable=self.min_val, width=5, font=("Arial", 12)).pack(side="left", padx=5)
        tk.Label(range_frame, text="至", font=("Microsoft JhengHei", 12), bg="#f8fafc").pack(side="left")
        ttk.Spinbox(range_frame, from_=1, to=1000, textvariable=self.max_val, width=5, font=("Arial", 12)).pack(side="left", padx=5)

        # 第二行：數量與重複
        opt_frame = tk.Frame(settings_frame, bg="#f8fafc", pady=10)
        opt_frame.pack()

        tk.Label(opt_frame, text="每次抽取：", font=("Microsoft JhengHei", 12), bg="#f8fafc").pack(side="left")
        ttk.Spinbox(opt_frame, from_=1, to=100, textvariable=self.count_val, width=5, font=("Arial", 12)).pack(side="left", padx=5)
        tk.Label(opt_frame, text="個", font=("Microsoft JhengHei", 12), bg="#f8fafc").pack(side="left")

        tk.Checkbutton(opt_frame, text="不重複", variable=self.no_repeat, 
                       bg="#f8fafc", font=("Microsoft JhengHei", 12)).pack(side="left", padx=20)

        # 按鈕
        self.draw_btn = tk.Button(self.frame, text="🎰 隨機抽取", command=self.start_draw,
                                 font=("Microsoft JhengHei", 18, "bold"), 
                                 bg="#2563eb", fg="white", relief="flat", 
                                 width=15, pady=10)
        self.draw_btn.pack(pady=20)

    def start_draw(self):
        if self.animating:
            return
        
        try:
            low = self.min_val.get()
            high = self.max_val.get()
            count = self.count_val.get()
            
            if low >= high:
                messagebox.showerror("錯誤", "範圍設定錯誤：起始值需小於結束值")
                return
            
            if self.no_repeat.get() and count > (high - low + 1):
                messagebox.showerror("錯誤", "抽取數量超過範圍總數（不重複模式）")
                return

            self.animating = True
            self._animate_draw(0, 15) # 動畫次數
            
        except ValueError:
            messagebox.showerror("錯誤", "請輸入有效的數字")

    def _animate_draw(self, current, total):
        if current < total:
            # 顯示隨機跳動過程
            rand_temp = random.randint(self.min_val.get(), self.max_val.get())
            self.result_label.config(text=str(rand_temp), fg="#94a3b8")
            # 逐漸減慢
            delay = 50 + (current * 20)
            self.frame.after(delay, lambda: self._animate_draw(current + 1, total))
        else:
            # 最終結果
            self._show_final_result()

    def _show_final_result(self):
        low = self.min_val.get()
        high = self.max_val.get()
        count = self.count_val.get()
        
        if self.no_repeat.get():
            results = random.sample(range(low, high + 1), count)
        else:
            results = [random.randint(low, high) for _ in range(count)]
        
        if len(results) == 1:
            self.result_label.config(text=str(results[0]), fg="#2563eb")
        else:
            # 抽取多個時，縮小字體顯示
            res_str = ", ".join(map(str, sorted(results)))
            self.result_label.config(text=res_str, font=("Microsoft JhengHei", 40, "bold"), fg="#2563eb")
            # 2秒後自動恢復大字體大小的設置，方便下次抽取
            self.frame.after(5000, lambda: self.result_label.config(font=("Microsoft JhengHei", 120, "bold")))

        self.animating = False

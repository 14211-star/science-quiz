import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading

# 嘗試加載 pygame 用於高品質音效
try:
    import pygame
    pygame.mixer.init()
    HAS_PYGAME = True
except ImportError:
    HAS_PYGAME = False

class TimerTab:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#f8fafc")
        
        # 狀態變量
        self.remaining = 180 # 默認 180 秒 (3分鐘)
        self.running = False
        self.paused = False
        self.beep_enabled = tk.BooleanVar(value=True)
        self.start_beep_enabled = tk.BooleanVar(value=True)
        
        self._build_ui()
        self._update_display()

    def _build_ui(self):
        # 顯示區域
        display_card = tk.Frame(self.frame, bg="#ffffff", padx=40, pady=40, 
                                highlightbackground="#e2e8f0", highlightthickness=1)
        display_card.pack(pady=30, padx=20, fill="both", expand=True)

        self.time_label = tk.Label(display_card, text="03:00", 
                                  font=("Courier New", 80, "bold"), 
                                  bg="#ffffff", fg="#1e293b")
        self.time_label.pack(expand=True, fill="both")
        
        # 綁定視窗縮放事件
        self.time_label.bind("<Configure>", self._on_resize)

        # 設定區域
        settings_frame = tk.Frame(self.frame, bg="#f8fafc")
        settings_frame.pack(pady=10)

        tk.Label(settings_frame, text="設定時間：", font=("Microsoft JhengHei", 12), bg="#f8fafc").grid(row=0, column=0)
        
        self.min_spin = ttk.Spinbox(settings_frame, from_=0, to=99, width=5, font=("Arial", 14))
        self.min_spin.set(3)
        self.min_spin.grid(row=0, column=1, padx=5)
        tk.Label(settings_frame, text="分", font=("Microsoft JhengHei", 12), bg="#f8fafc").grid(row=0, column=2)

        self.sec_spin = ttk.Spinbox(settings_frame, from_=0, to=59, width=5, font=("Arial", 14))
        self.sec_spin.set(0)
        self.sec_spin.grid(row=0, column=3, padx=5)
        tk.Label(settings_frame, text="秒", font=("Microsoft JhengHei", 12), bg="#f8fafc").grid(row=0, column=4)

        apply_btn = tk.Button(settings_frame, text="套用", command=self.apply_settings,
                             bg="#94a3b8", fg="white", relief="flat", padx=15)
        apply_btn.grid(row=0, column=5, padx=10)

        # 提示音控制
        audio_frame = tk.Frame(self.frame, bg="#f8fafc")
        audio_frame.pack(pady=10)

        tk.Checkbutton(audio_frame, text="開始提示音", variable=self.start_beep_enabled, 
                       bg="#f8fafc", font=("Microsoft JhengHei", 10)).pack(side="left", padx=10)
        tk.Checkbutton(audio_frame, text="結束提示音", variable=self.beep_enabled, 
                       bg="#f8fafc", font=("Microsoft JhengHei", 10)).pack(side="left", padx=10)

        # 按鈕區域
        btn_frame = tk.Frame(self.frame, bg="#f8fafc")
        btn_frame.pack(pady=30)

        self.start_btn = tk.Button(btn_frame, text="▶ 開始", command=self.toggle_timer,
                                  font=("Microsoft JhengHei", 16, "bold"), 
                                  bg="#22c55e", fg="white", relief="flat", 
                                  width=10, pady=10)
        self.start_btn.pack(side="left", padx=10)

        self.reset_btn = tk.Button(btn_frame, text="⟳ 重置", command=self.reset_timer,
                                  font=("Microsoft JhengHei", 16, "bold"), 
                                  bg="#ef4444", fg="white", relief="flat", 
                                  width=10, pady=10)
        self.reset_btn.pack(side="left", padx=10)

    def _on_resize(self, event):
        # 根據標籤高度動態調整字體大小 (高度的 0.6 倍左右)
        new_size = int(event.height * 0.6)
        # 限制字體大小範圍
        new_size = max(20, min(new_size, 300))
        self.time_label.config(font=("Courier New", new_size, "bold"))

    def _update_display(self):
        mins, secs = divmod(self.remaining, 60)
        self.time_label.config(text=f"{mins:02d}:{secs:02d}")
        
        # 倒計時警告色 (剩餘10秒變紅)
        if self.remaining <= 10 and self.running:
            self.time_label.config(fg="#ef4444")
        else:
            self.time_label.config(fg="#1e293b")

    def apply_settings(self):
        try:
            m = int(self.min_spin.get())
            s = int(self.sec_spin.get())
            self.remaining = m * 60 + s
            self._update_display()
            self.running = False
            self.start_btn.config(text="▶ 開始", bg="#22c55e")
        except ValueError:
            messagebox.showerror("錯誤", "請輸入有效的數字")

    def toggle_timer(self):
        if not self.running:
            self.running = True
            self.start_btn.config(text="⏸ 暫停", bg="#f59e0b")
            if self.start_beep_enabled.get():
                self._play_sound("start")
            self._run_timer()
        else:
            self.running = False
            self.start_btn.config(text="▶ 繼續", bg="#22c55e")

    def _run_timer(self):
        if self.running and self.remaining > 0:
            self.remaining -= 1
            self._update_display()
            self.frame.after(1000, self._run_timer)
        elif self.remaining <= 0:
            self.running = False
            self.start_btn.config(text="▶ 開始", bg="#22c55e")
            if self.beep_enabled.get():
                self._play_sound("end")
            messagebox.showinfo("時間到", "倒計時結束！")

    def reset_timer(self):
        self.running = False
        self.apply_settings()
        self.start_btn.config(text="▶ 開始", bg="#22c55e")

    def _play_sound(self, type):
        # 這裡未來可以用 pygame 播放真正的音效檔
        # 目前先用 winsound 作為替代，或靜音
        try:
            import winsound
            if type == "start":
                winsound.Beep(1000, 200)
            else:
                winsound.Beep(1500, 500)
                winsound.Beep(1500, 500)
        except:
            pass

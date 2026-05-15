import tkinter as tk
from tkinter import ttk
from timer_tab import TimerTab
from spinner_tab import SpinnerTab
import sys
import os

# 解決 PyInstaller 打包後的路徑問題
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("教學小助手 - 倒計時 & 隨機抽號")
        self.root.geometry("600x700")
        self.root.configure(bg="#f8fafc") # Slate 50
        
        # 設置圖標 (如果有的話)
        # self.root.iconbitmap(resource_path("assets/icon.ico"))

        self._setup_style()
        self._build_ui()
        
        self.fullscreen = False
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)

    def _setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # 全域色彩定義 (護眼淺色調)
        bg_color = "#f8fafc"
        accent_color = "#2563eb" # Blue 600
        text_color = "#1e293b" # Slate 800
        
        style.configure("TNotebook", background=bg_color, borderwidth=0)
        style.configure("TNotebook.Tab", 
                        background="#e2e8f0", 
                        foreground=text_color, 
                        padding=[20, 10], 
                        font=("Microsoft JhengHei", 12, "bold"))
        
        style.map("TNotebook.Tab",
                  background=[("selected", accent_color)],
                  foreground=[("selected", "#ffffff")])
        
        style.configure("TFrame", background=bg_color)
        style.configure("Card.TFrame", background="#ffffff", relief="flat")

    def _build_ui(self):
        # 標題欄
        header = tk.Frame(self.root, bg="#2563eb", height=60)
        header.pack(fill="x", side="top")
        
        tk.Label(header, text="🏫 教學小助手", 
                 font=("Microsoft JhengHei", 18, "bold"), 
                 bg="#2563eb", fg="#ffffff", pady=10).pack()

        # 分頁控制
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)

        self.timer_tab = TimerTab(self.notebook)
        self.spinner_tab = SpinnerTab(self.notebook)

        self.notebook.add(self.timer_tab.frame, text=" ⏱ 倒計時器 ")
        self.notebook.add(self.spinner_tab.frame, text=" 🎰 隨機抽號 ")

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def exit_fullscreen(self, event=None):
        self.fullscreen = False
        self.root.attributes("-fullscreen", False)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()

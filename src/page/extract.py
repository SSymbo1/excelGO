import ttkbootstrap as ttk
import json


# 提取为sql界面
class Extract(ttk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent)

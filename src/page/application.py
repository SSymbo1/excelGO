import ttkbootstrap as ttk
from page.home import Home
from page.setting import Setting
from page.extract import Extract


# 主应用类
class Application:
    def __init__(self, root: ttk.Window, config):
        self.root = root
        # 主容器
        self.container = ttk.Frame(self.root)
        self.container.pack(fill="both", expand=True)
        # 标签页容器
        self.notebook = ttk.Notebook(
            self.container, bootstyle=config["project"]["notebook_theme"]
        )
        self.notebook.pack(fill="both", expand=True)
        # 初始化标签页
        self.init_notebook(config)
        # 加载主界面
        self.root.place_window_center()
        root.mainloop()

    def init_notebook(self, config):
        # 首页标签页
        self.home = Home(self.notebook, config)
        self.notebook.add(self.home, text="首页")
        # sql生成标签页
        self.extract = Extract(self.notebook, config)
        self.notebook.add(self.extract, text="提取为sql")
        # 设置标签页
        self.setting = Setting(self.notebook, config)
        self.notebook.add(self.setting, text="设置")
        # 默认选择首页标签页
        self.notebook.select(self.home)

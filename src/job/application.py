import ttkbootstrap as ttk
import util.path as path
import json
from page.home import Home
from page.setting import Setting
from page.extract import Extract
from page.aggregation import Aggregation


# 主应用类
class Application:
    def __init__(self):
        # 读取配置文件
        with open(
            path.get_resource_path("resources\config.json"), "r", encoding="utf-8"
        ) as cf:
            self.__config = json.load(cf)
        # 初始化主界面
        self.__root = ttk.Window(
            title=self.__config["project"]["name"],
            size=(
                self.__config["project"]["width"],
                self.__config["project"]["height"],
            ),
            themename=self.__config["project"]["theme"],
            resizable=(
                self.__config["project"]["resizable"],
                self.__config["project"]["resizable"],
            ),
            iconphoto=self.__config["project"]["icon"],
        )
        # 主容器
        self.__container = ttk.Frame(self.__root)
        self.__container.pack(fill="both", expand=True)
        # 标签页容器
        self.__notebook = ttk.Notebook(
            self.__container, bootstyle=self.__config["project"]["notebook_theme"]
        )
        self.__notebook.pack(fill="both", expand=True)
        # 初始化标签页
        self.__init_notebook(self.__config)
        # 加载主界面
        self.__root.place_window_center()
        self.__root.mainloop()

    def __init_notebook(self, config):
        # 首页标签页
        self.__home = Home(self.__notebook, config)
        self.__notebook.add(self.__home, text="首页")
        # sql生成标签页
        self.__extract = Extract(self.__notebook, config)
        self.__notebook.add(self.__extract, text="提取为sql")
        # 表格聚合标签页
        self.__aggregation = Aggregation(self.__notebook, config)
        self.__notebook.add(self.__aggregation, text="表格聚合")
        # 设置标签页
        self.__setting = Setting(self.__notebook, config)
        self.__notebook.add(self.__setting, text="设置")
        # 默认选择首页标签页
        self.__notebook.select(self.__home)

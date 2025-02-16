import ttkbootstrap as ttk
import json
from page.application import Application
import util.path as path

if __name__ == "__main__":
    # 读取配置文件
    with open(
        path.get_resource_path("resources\config.json"), "r", encoding="utf-8"
    ) as cf:
        config = json.load(cf)
    # 启动程序
    app = Application(
        ttk.Window(
            title=config["project"]["name"],
            size=(config["project"]["width"], config["project"]["height"]),
            themename=config["project"]["theme"],
            resizable=(config["project"]["resizable"], config["project"]["resizable"]),
            iconphoto=config["project"]["icon"],
        ),
        config,
    )

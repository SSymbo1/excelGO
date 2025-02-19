from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import util.path as path
import time
import os

# 加载文件（获取文件路径）
def load_file(title_name, types):
    return filedialog.askopenfilename(title=title_name, filetypes=types)


# 初始化导出文件夹
def init_dump_folder():
    export_forder_path = os.path.join(os.getcwd(), "export")
    if not os.path.exists(path.get_resource_path(export_forder_path)):
        os.mkdir(path.get_resource_path(export_forder_path))


# 加载图片文件
def load_image_file(image_path: str, is_round: bool, width: int, height: int):
    image = Image.open(path.get_resource_path(image_path))
    image = image.resize((width, height))
    if is_round:
        mask = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, width, height), fill=255)
        image.putalpha(mask)
    return ImageTk.PhotoImage(image)


# 导出文件
def dump_file(config: dict, content: str):
    dump_file_name = config["default_name"].format(timestamp=int(time.time() * 1000))
    with open(
        f"{config['export_path']}\\{dump_file_name}",
        "w",
        encoding="utf-8",
    ) as file:
        file.write(content)
    return f"{config['export_path']}\\{dump_file_name}"

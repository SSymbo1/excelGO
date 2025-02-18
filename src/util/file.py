from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import util.path as path


def load_file(title_name, types):
    return filedialog.askopenfilename(title=title_name, filetypes=types)


def load_image_file(image_path: str, is_round: bool, width: int, height: int):
    image = Image.open(path.get_resource_path(image_path))
    image = image.resize((width, height))
    if is_round:
        mask = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, width, height), fill=255)
        image.putalpha(mask)
    return ImageTk.PhotoImage(image)

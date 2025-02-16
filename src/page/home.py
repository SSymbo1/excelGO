import ttkbootstrap as ttk
from PIL import Image, ImageTk, ImageDraw
import util.path as path


# 主页
class Home(ttk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.home_image_init(config)
        ttk.Label(self, text="excelGO", bootstyle="primary", font=("", 25)).pack(
            pady=20
        )
        ttk.Label(
            self, text=config["project"]["desc"], bootstyle="secondry", font=("", 12)
        ).pack()
        ttk.Button(
            self,
            text="检查更新",
            bootstyle="primary-outline",
            command=self.check_update,
        ).pack(pady=20)

    def home_image_init(self, config):
        image = Image.open(path.get_resource_path(config["project"]["home_logo"]))
        image = image.resize((150, 150))
        mask = Image.new("L", (150, 150), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 150, 150), fill=255)
        image.putalpha(mask)
        self.logo_image = ImageTk.PhotoImage(image)
        ttk.Label(self, image=self.logo_image).pack(pady=(120, 0))

    def check_update(self):
        print("检查更新")

import ttkbootstrap as ttk
import util.file as file
import webbrowser


# 主页
class Home(ttk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent)
        self.site = config["project"]["site"]
        self.pack(fill="both", expand=True)
        self.__home_image_init(config)
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
            command=self.__check_update,
        ).pack(pady=20)

    def __home_image_init(self, config):
        self.logo_image = file.load_image_file(
            config["project"]["home_logo"], True, 150, 150
        )
        ttk.Label(self, image=self.logo_image).pack(pady=(120, 0))

    def __check_update(self):
        webbrowser.open(self.site)

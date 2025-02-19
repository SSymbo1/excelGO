from ttkbootstrap.dialogs import dialogs
import ttkbootstrap as ttk

# 通知类
class Notice:
    def __init__(
        self, title: str, message: str, type: str = "info", container: ttk.Frame = None
    ):
        self.title = title
        self.message = message
        self.type = type
        self.container = container

    # 根据实例化时提供的参数，调用不同的提示框
    def show_message_box(self):
        message_box_functions = {
            "info": dialogs.Messagebox.show_info,
            "error": dialogs.Messagebox.show_error,
        }
        message_box_functions.get(self.type)(
            title=self.title, message=self.message, parent=self.container
        )

    # 根据实例化时提供的参数，调用不同的判断框
    def show_judge_box(self, buttons: list):
        return dialogs.Messagebox.show_question(
            title=self.title,
            message=self.message,
            buttons=buttons,
            parent=self.container,
        )

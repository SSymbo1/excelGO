import ttkbootstrap as ttk
import util.file as file
import random
from job.dump import Dump
from util.notice import Notice


# 提取为sql界面
class Extract(ttk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent)
        self.__excel_path = ""
        self.__extract_config = []
        self.__delete_index: str = ""
        self.__config_window = None
        self.__dump = None
        self.__excel_headers = []
        self.__config = config
        # 上下布局容器
        self.pack(fill="both", expand=True)
        # 操作侧grid布局容器
        self.__file_grid = ttk.Frame(self)
        self.__file_grid.grid(row=1, column=0, sticky="we")
        # 操作选项label
        ttk.Label(
            self.__file_grid, text="操作类型:", bootstyle="secondry", font=("", 12)
        ).grid(row=0, column=0, padx=(5, 0), pady=(10, 0))
        # 操作选项菜单
        self.__operation = ttk.Menubutton(
            self.__file_grid,
            text=config["project"]["default_extract"],
            bootstyle="primary-outline",
            width=17,
        )
        self.__operation.grid(row=0, column=1, padx=(10, 0), pady=(10, 0))
        self.__menu = ttk.Menu(self.__operation, tearoff=0)
        self.__selected_option = ttk.StringVar(
            value=config["project"]["default_extract"]
        )
        for option in config["project"]["exract_options"]:
            self.__menu.add_radiobutton(
                label=option,
                value=option,
                variable=self.__selected_option,
                command=lambda: self.__operation.config(
                    text=self.__selected_option.get()
                ),
            )
        self.__operation["menu"] = self.__menu
        # 选择文件按钮
        ttk.Button(
            self.__file_grid,
            text="选择文件",
            command=self.__user_select_file,
            bootstyle="primary-outline",
        ).grid(row=0, column=2, padx=(10, 0), pady=(10, 0))
        # 提取为sql功能设置按钮
        ttk.Button(
            self.__file_grid,
            text="提取设置",
            bootstyle="primary-outline",
        ).grid(row=0, column=3, padx=(10, 0), pady=(10, 0))
        # 表名输入框
        ttk.Label(
            self.__file_grid, text="操作表名:", bootstyle="secondry", font=("", 12)
        ).grid(row=1, column=0, padx=(5, 0), pady=(10, 0))
        ttk.Entry(
            self.__file_grid, bootstyle="primary", width=20, name="table_name"
        ).grid(row=1, column=1, padx=(10, 0), pady=(10, 0))
        # 新增配置按钮
        ttk.Button(
            self.__file_grid,
            text="新增配置",
            bootstyle="success-outline",
            command=self.__add_config,
        ).grid(row=1, column=2, padx=(10, 0), pady=(10, 0))
        # 删除配置按钮
        ttk.Button(
            self.__file_grid,
            text="删除配置",
            bootstyle="danger-outline",
            command=self.__delete_config,
        ).grid(row=1, column=3, padx=(10, 0), pady=(10, 0))
        # 表格展示
        self.__table = ttk.Treeview(self, bootstyle="primary", show="headings")
        self.__table.configure(
            columns=tuple(self.__config["project"]["extract_config_table"])
        )
        self.__table.bind("<<TreeviewSelect>>", self.__select_config_column)
        for column in self.__table["columns"]:
            self.__table.heading(column, text=column)
        self.__table.grid(row=2, column=0, padx=(20, 0), pady=(10, 0), sticky="we")
        # 导出按钮
        ttk.Button(
            self,
            image=file.load_image_file(config["project"]["exract_icon"], False, 50, 50),
            text="导出",
            bootstyle="primary-outline",
            command=self.__dump_data,
        ).grid(row=3, column=0, pady=(10, 0))

    # 选择文件按钮
    def __user_select_file(self):
        self.__excel_path = file.load_file(
            "选择表格文件,注意:打开这个界面会清空之前的配置信息!",
            [("Excel", "*.xlsx"), ("Excel", "*.xls")],
        )
        if self.__excel_path != "" and self.__excel_path is not None:
            self.__dump = Dump(self.__excel_path, self.__config["extract"])
        if self.__dump and self.__excel_path != "":
            self.__excel_headers = self.__dump.get_data_header()
            Notice("提示", "表格加载成功!", container=self).show_message_box()
        self.__extract_config = []
        self.__dynamic_rander_table()

    # 提取设置按钮
    def __set_extract_config(self):
        pass

    # 新增配置按钮
    def __add_config(self):
        if self.__excel_path == "" or self.__excel_path is None:
            Notice(
                "错误", "请先选择表格文件!", "error", container=self
            ).show_message_box()
        else:
            operation = self.__selected_option.get()
            self.__config_window = ttk.Toplevel(self)
            self.__config_window.title("新增配置")
            self.__config_window.geometry("500x600")
            self.__config_window.resizable(False, False)
            self.__config_window.place_window_center()
            # 表单布局初始化
            self.__form_frame = ttk.Frame(self.__config_window)
            self.__form_frame.pack(padx=20, pady=20, fill="x", anchor="center")
            # 导出列名
            column_name = ttk.Label(self.__form_frame, text="导出列名:", font=("", 12))
            column_name.grid(row=0, column=0, padx=(30, 0), pady=(10, 0))
            column_name_entry = ttk.Entry(
                self.__form_frame, bootstyle="primary", name="column_name"
            )
            column_name_entry.grid(row=0, column=1, padx=(10, 0), pady=(10, 0))
            # 取值方式
            dump_type = ttk.Label(self.__form_frame, text="取值方式:", font=("", 12))
            dump_type.grid(row=1, column=0, padx=(30, 0), pady=(10, 0))
            self.__dump_type_combobox = ttk.Combobox(
                self.__form_frame,
                bootstyle="primary",
                width=18,
                name="dump_type",
                state="readonly",
            )
            self.__dump_type_combobox["values"] = self.__config["project"][
                "extract_config"
            ]
            self.__dump_type_combobox.bind(
                "<<ComboboxSelected>>",
                self.__dyniamic_config_component,
            )
            self.__dump_type_combobox.set(
                self.__config["project"]["default_extract_config"]
            )
            self.__dump_type_combobox.grid(row=1, column=1, padx=(10, 0), pady=(10, 0))
            # 取值
            dump_value = ttk.Label(self.__form_frame, text="导出取值:", font=("", 12))
            dump_value.grid(row=2, column=0, padx=(30, 0), pady=(10, 0))
            self.__dump_value_entry = ttk.Entry(
                self.__form_frame,
                bootstyle="primary",
                state="readonly",
                name="dynamic_component",
            )
            self.__dump_value_entry.grid(row=2, column=1, padx=(10, 0), pady=(10, 0))
            if operation == "UPDATE":
                pass
            # 保存按钮
            ttk.Button(
                self.__form_frame,
                text="保存",
                bootstyle="primary-outline",
                command=self.__close_config_window,
            ).grid(row=3, column=2, padx=(5, 0), pady=(20, 0))

    # 删除配置按钮
    def __delete_config(self):
        result = ""
        if self.__delete_index == "":
            result = Notice(
                "提示",
                "当前未选中配置行,请先选中配置行",
                container=self,
            ).show_judge_box(["删除所有配置:danger", "否:secondary"])
        else:
            result = Notice(
                "提示",
                "是否删除已选择数据?或删除全部配置?",
                container=self,
            ).show_judge_box(["是:primary", "否:secondary", "删除所有配置:danger"])
        if result == "是":
            filter_config = [
                config
                for config in self.__extract_config
                if config["index"] != str(self.__delete_index)
            ]
            self.__extract_config = filter_config
        elif result == "删除所有配置":
            self.__extract_config = []
        self.__dynamic_rander_table()

    # 导出按钮
    def __dump_data(self):
        table_name = ""
        for child in self.__file_grid.winfo_children():
            if child.winfo_name() == "table_name":
                table_name = child.get()
                break
        if self.__excel_path == "" or self.__excel_path is None:
            Notice("错误", "请先选择表格文件", "error", self).show_message_box()
        elif self.__extract_config.__len__() == 0:
            Notice("错误", "请先添加配置", "error", self).show_message_box()
        elif table_name == "":
            Notice("错误", "请先输入操作表名", "error", self).show_message_box()
        elif not any(
            config.get("dump_type") == self.__config["project"]["extract_config"][2]
            for config in self.__extract_config
        ):
            Notice(
                "错误",
                "必须添加一项取值方式为:'表格取值'的配置项作为索引配置",
                "error",
                self,
            ).show_message_box()
        else:
            result = Notice(
                "提示",
                "确定导出数据?",
                container=self,
            ).show_judge_box(["是:primary", "否:secondary"])
            if result == "是":
                dump = Dump(self.__excel_path, self.__config["extract"])
                dump_result = dump.dump_sql(
                    self.__extract_config, table_name, self.__selected_option.get()
                )
                if dump_result:
                    Notice(
                        "提示", f"导出成功,位置为:{dump_result}", container=self
                    ).show_message_box()

    # 动态配置组件
    def __dyniamic_config_component(self, event):
        for child in self.__form_frame.winfo_children():
            if child.winfo_name() == "dynamic_component":
                child.destroy()
                break
        dump_type_selected = self.__dump_type_combobox.get()
        if (
            dump_type_selected == self.__config["project"]["extract_config"][0]
            or dump_type_selected == self.__config["project"]["extract_config"][1]
        ):
            entry = ttk.Entry(
                self.__form_frame,
                bootstyle="primary",
                state="readonly",
                name="dynamic_component",
            )
            entry.grid(row=2, column=1, padx=(10, 0), pady=(10, 0))
        elif dump_type_selected == self.__config["project"]["extract_config"][2]:
            # todo 从数据列表格取数据列
            combobox = ttk.Combobox(
                self.__form_frame,
                bootstyle="primary",
                width=18,
                name="dynamic_component",
            )
            combobox["values"] = self.__excel_headers
            combobox.set(self.__excel_headers[0])
            combobox.grid(row=2, column=1, padx=(10, 0), pady=(10, 0))
        elif dump_type_selected == self.__config["project"]["extract_config"][3]:
            entry = ttk.Entry(
                self.__form_frame,
                bootstyle="primary",
                name="dynamic_component",
            )
            entry.grid(row=2, column=1, padx=(10, 0), pady=(10, 0))

    # 保存并关闭新增配置窗口
    def __close_config_window(self):
        custom_config = {}
        # 获取配置项
        for child in self.__form_frame.winfo_children():
            if child.winfo_name() == "column_name":
                custom_config["column_name"] = child.get()
                continue
            elif child.winfo_name() == "dump_type":
                custom_config["dump_type"] = child.get()
                continue
            elif child.winfo_name() == "dynamic_component":
                custom_config["dump_value"] = child.get()
                continue
        # 配置项空值检查
        if (
            custom_config["column_name"] == ""
            or (
                custom_config["dump_type"]
                == self.__config["project"]["extract_config"][3]
                and custom_config["dump_value"] == ""
            )
            or (
                custom_config["dump_type"]
                == self.__config["project"]["extract_config"][2]
                and custom_config["dump_value"] == ""
            )
        ):
            Notice(
                "错误", "配置项存在空值项,不能保存!", "error", self.__config_window
            ).show_message_box()
        elif any(
            config.get("column_name") == custom_config["column_name"]
            for config in self.__extract_config
        ):
            Notice(
                "错误",
                "已保存的配置项中存在重复的列名,请重新配置!",
                "error",
                self.__config_window,
            ).show_message_box()
        else:
            # 保存配置并关闭配置窗口,更新配置表格
            custom_config["index"] = "".join(
                map(str, random.sample(range(10), 5))
            )  # 生成配置索引
            self.__extract_config.append(custom_config)
            self.__dynamic_rander_table()

    # 监听选中配置表格其中一行
    def __select_config_column(self, event):
        if self.__table.selection():
            values = self.__table.item(self.__table.selection())["values"]
            self.__delete_index = values[3]

    # 动态渲染配置表格
    def __dynamic_rander_table(self):
        if self.__config_window:
            self.__config_window.destroy()
        self.__table.delete(*self.__table.get_children())
        for config in self.__extract_config:
            column_value = (
                config["column_name"],
                config["dump_type"],
                config["dump_value"],
                config["index"],
            )
            self.__table.insert("", "end", values=column_value)

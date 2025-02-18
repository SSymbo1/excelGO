import xlwings as xw
import util.path as path
import json


class Dump:
    def __init__(self, file_path, config):
        self.__file_path = file_path
        self.__config = config

    # 获取数据表头
    def get_data_header(self):
        app = xw.App(visible=False)
        wb = app.books.open(path.get_resource_path(self.__file_path))
        sheet = wb.sheets[0]
        headers = (
            sheet.range(f"A{self.__config['header_column']}").expand("right").value
        )
        wb.close()
        app.quit()
        return headers

    # 导出数据sql
    def dump_sql(self, dump_config, table_name, operation):
        if operation == "INSERT":
            self.__insert_dump(
                self.__dump_config_builder(dump_config, table_name, operation)
            )
        elif operation == "UPDATE":
            pass

    # INSERT语句生成导出
    def __insert_dump(self, sql_config):
        sql = ""
        app = xw.App(visible=False)
        wb = app.books.open(path.get_resource_path(self.__file_path))
        sheet = wb.sheets[0]
        if sql_config["config"]["sql_case"] == "lower":
            with open(path.get_resource_path("resources\\template.json")) as t:
                sql = json.load(t)["insert_lower"]
        elif sql_config["config"]["sql_case"] == "upper":
            with open(path.get_resource_path("resources\\template.json")) as t:
                sql = json.load(t)["insert_upper"]
        columns = ",".join(sql_config["columns"])
        sql = sql.format(table_name=sql_config["table_name"], columns=columns)
        header = sheet.range(f"A{self.__config['header_column']}").expand("right").value
        for column in sql_config["dump_data"]:
            data_col = header.index(column["dump"]) + 1
            data_index = self.__column_index_to_character(data_col)
            column["data"] = (
                sheet.range(f"{data_index}{self.__config['data_column']}")
                .expand("down")
                .value
            )
            print(column["data"])
        wb.close()
        app.quit()

    # UPDATE语句生成导出
    def __update_dump(self, sql_config):
        pass

    # 构建导出配置
    def __dump_config_builder(self, dump_config, table_name, operation):
        to_sql = {}
        columns = [column["column_name"] for column in dump_config]
        auto_number = [
            column["column_name"]
            for column in dump_config
            if column["dump_type"] == "数字自增"
        ]
        auto_character = [
            column["column_name"]
            for column in dump_config
            if column["dump_type"] == "字母自增"
        ]
        customize = [
            column["column_name"]
            for column in dump_config
            if column["dump_type"] == "自定义"
        ]
        dump_data = [
            {"column": column["column_name"], "dump": column["dump_value"]}
            for column in dump_config
            if column["dump_type"] == "表格取值"
        ]
        to_sql["table_name"] = table_name
        to_sql["columns"] = columns
        to_sql["auto_number"] = auto_number
        to_sql["auto_character"] = auto_character
        to_sql["customize"] = customize
        to_sql["dump_data"] = dump_data
        to_sql["config"] = self.__config
        if operation == "update":
            pass
        return to_sql

    def __column_index_to_character(self, col_num):
        letter = ""
        while col_num > 0:
            col_num, remainder = divmod(col_num - 1, 26)
            letter = chr(65 + remainder) + letter
        return letter

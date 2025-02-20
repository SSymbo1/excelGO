import xlwings as xw
import util.path as path
import util.file as file
import json


# 数据sql提取
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

    # 从导出时表格获取数据
    def __dump_get_data(self, config):
        app = xw.App(visible=False)
        wb = app.books.open(path.get_resource_path(self.__file_path))
        sheet = wb.sheets[0]
        header = sheet.range(f"A{self.__config['header_column']}").expand("right").value
        for column in config["dump_data"]:
            data_col = header.index(column["dump"]) + 1
            data_index = self.__column_index_to_character(data_col)
            column["data"] = (
                sheet.range(f"{data_index}{self.__config['data_column']}")
                .expand("down")
                .value
            )
        wb.close()
        app.quit()
        return config

    # 导出数据sql
    def dump_sql(self, dump_config, table_name, operation):
        if operation == "INSERT":
            return self.__insert_dump(
                self.__dump_config_builder(dump_config, table_name, operation)
            )
        elif operation == "UPDATE":
            pass

    # INSERT语句生成导出
    def __insert_dump(self, sql_config):
        sql_template = ""
        # 获取sql模板
        with open(
            path.get_resource_path("resources\\template.json"), encoding="utf-8"
        ) as t:
            template = json.load(t)
            if sql_config["config"]["sql_case"] == "lower":
                sql_template = template["insert_lower"]
            elif sql_config["config"]["sql_case"] == "upper":
                sql_template = template["insert_upper"]
        # 处理补全sql模板，动态设置插入值索引
        insert_placeholder = []
        for index in range(len(sql_config["columns"])):
            insert_placeholder.append(f"'{{{index}}}'")
        columns = ",".join(sql_config["columns"])
        insert_index = ",".join(insert_placeholder)
        sql_template = sql_template.format(
            table_name=sql_config["table_name"], columns=columns, values=insert_index
        )
        # sql模板补全，生成导出sql
        auto_number, auto_character = (
            sql_config["config"]["auto_number"],
            ord(sql_config["config"]["auto_character"]),
        )
        dump_sql = ""
        for index in range(len(sql_config["dump_data"][0]["data"])):
            sql = sql_template
            target_value = []
            for column in range(len(sql_config["columns"])):
                # 当前插入项是否为数值自动填充
                if sql_config["columns"][column] in sql_config["auto_number"]:
                    target_value.append(str(auto_number))
                    continue
                # 当前插入项是否为字母自动填充
                elif sql_config["columns"][column] in sql_config["auto_character"]:
                    target_value.append(chr(auto_character))
                    continue
                # 当前插入项是否为自定义值
                elif any(
                    config.get("column") == sql_config["columns"][column]
                    for config in sql_config["customize"]
                ):
                    target_value.append(
                        [
                            item.get("dump")
                            for item in sql_config["customize"]
                            if item.get("column") == sql_config["columns"][column]
                        ][0]
                    )
                    continue
                # 当前插入项是否为表格取值
                elif any(
                    config.get("column") == sql_config["columns"][column]
                    for config in sql_config["dump_data"]
                ):
                    target_value.append(
                        [
                            item.get("data")[index]
                            for item in sql_config["dump_data"]
                            if item.get("column") == sql_config["columns"][column]
                        ][0]
                    )
                    continue
            auto_number += 1
            auto_character += 1
            dump_sql += sql.format(*target_value)
        return file.dump_file(sql_config["config"], dump_sql)

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
            {"column": column["column_name"], "dump": column["dump_value"]}
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
        to_sql = self.__dump_get_data(to_sql)
        return to_sql

    # excel数字列索引转字母列索引
    def __column_index_to_character(self, col_num):
        letter = ""
        while col_num > 0:
            col_num, remainder = divmod(col_num - 1, 26)
            letter = chr(65 + remainder) + letter
        return letter

import datetime
import sys
import time
import os
from tqdm import tqdm
from pathlib import Path
from core.jsonInfo import JsonInfo


# from db_tools.tools.Img_class import LabelInfo


class Create(object):
    def __init__(self, database, db_cursor):
        self.db_cursor = db_cursor
        self.database = database

        # 读取标签信息表，形成了一个标签和大类的一一对应的字典，方便后续使用和查询。
        sql_statement = "SELECT 标签 FROM `标签信息表`;"
        self.db_cursor.execute(sql_statement)
        label_info = list(self.db_cursor.fetchall())
        self.label_dic = {}
        for item in label_info:
            self.label_dic[item[0]] = item[1:]

        self.json_parsing = JsonInfo  # 读取json信息的类，使用时传入json文件的路径。
        self.date = self.Operation_date()  # 获取操作时的日期信息

    def add_md5_uc_info(self, md5, uc):
        # 将md5信息，添加到md5_uc这个表中
        sql_statement = "INSERT INTO md5_uc (MD5,UC) VALUES('{}','{}');".format(md5, uc)
        self.db_cursor.execute(sql_statement)  # 执行语句
        pass

    def add_json_to_db(self, json_list: list, confidence: bool, label_list: list) -> bool:
        # 传入一个json的路径列表
        label_dic = {}
        for item in label_list:
            label_dic[item] = True

        for json_path in json_list:
            json_class = self.json_parsing(json_path)  # 读取实例化的json文件
            self.__add_new_json(json_class, add_confidence=int(confidence), label_dic=label_dic)
            print("解析完成：{}".format(json_path))
        print("正在写入数据库......")
        self.database.commit()  # 提交修改
        return True

    def __add_new_json(self, json_class, label_dic: dict, add_confidence=0) -> None:
        # 私有函数，禁止外部访问，仅通过add_json函数调用。

        object_list = json_class.objects
        label_in_json = {}  # 保存json中含有的标签

        # 遍历目标列表
        for item in object_list:
            label = item.label
            if label not in self.label_dic.keys():
                # 检查json中是否含有不明标签
                # continue
                pass
            if label in label_in_json:
                # 如果标签已经更新过了，这个物体就跳过
                continue
            if label in label_dic:
                sql_statement = "INSERT INTO `目标标注表` VALUES ('{}', '{}', 1) ON DUPLICATE KEY UPDATE 置信度=置信度+{};" \
                    .format(json_class.unique_code, label, add_confidence)
                self.db_cursor.execute(sql_statement)  # 执行语句
            else:
                # sql_statement = "INSERT INTO `目标标注表` VALUES ('{}', '{}', 1) ON DUPLICATE KEY UPDATE 置信度=置信度;" \
                #     .format(json_class.unique_code, label)
                sql_statement = "INSERT IGNORE INTO `目标标注表` VALUES ('{}', '{}', 1);" \
                    .format(json_class.unique_code, label)
                self.db_cursor.execute(sql_statement)  # 执行语句
            label_in_json[label] = True  # 为记录标签的更新日期，将json中含有的标签记录下来。

        # 更新标签信息表
        for label in label_in_json:
            sql_statement = "UPDATE 标签信息表 SET 更新日期={} where `标签`='{}'".format(self.date, label)
            self.db_cursor.execute(sql_statement)  # 执行语句

    @staticmethod
    def Operation_date() -> str:
        # 生成一个日期的三位编码，以记录标签更新的日期。
        date = datetime.datetime.now()
        year = date.year
        month = date.month
        day = date.day
        if month < 10:
            month = '0' + str(month)
        else:
            month = str(month)
        if day < 10:
            day = '0' + str(day)
        else:
            day = str(day)
        year = str(year)[2:]

        return year + month + day

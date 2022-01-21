import pymysql
import sys
import os
from pathlib import Path
from db_tools.tools.Img_class import LabelInfo


class Delete(object):
    # 用于删除数据的类
    # 按照唯一编码，删除所有表中的相关信息
    def __init__(self, database, db_cursor, user):
        self.db_cursor = db_cursor
        self.database = database
        # 读取标签信息表，形成了一个标签和大类的一一对应的字典，方便后续使用和查询。
        sql_statement = "SELECT * FROM `标签信息表`;"
        self.db_cursor.execute(sql_statement)
        label_info = list(self.db_cursor.fetchall())
        self.label_dic = {}
        for item in label_info:
            self.label_dic[item[0]] = item[1:]
        self.user = user

    def drop_all_tables(self):
        # 删除数据库中所有表的内容。连个毛都不剩下
        if self.user == 'root':
            sql_statement = "TRUNCATE TABLE 图片大类表;"
            self.db_cursor.execute(sql_statement)  # 执行语句

            sql_statement = "TRUNCATE TABLE 目标标注表;"
            self.db_cursor.execute(sql_statement)  # 执行语句

            sql_statement = "TRUNCATE TABLE MD5对照表;"
            self.db_cursor.execute(sql_statement)  # 执行语句

            print("删库跑路了！")
            return True
        else:
            print("无清空权限！")
            return False
        pass

    def __drop(self, uc: str):
        # 删除一个编码对应的所有信息。
        # 私有函数，禁止外部调用。
        sql_statement = "DELETE FROM 图片大类表 where 唯一编码 = '{}';".format(uc)
        self.db_cursor.execute(sql_statement)

        sql_statement = "DELETE FROM 其他信息表 where 唯一编码 = '{}';".format(uc)
        self.db_cursor.execute(sql_statement)

        sql_statement = "DELETE FROM 特殊标注表 where 唯一编码 = '{}';".format(uc)
        self.db_cursor.execute(sql_statement)

        sql_statement = "DELETE FROM 绝缘子 where 唯一编码 = '{}';".format(uc)
        self.db_cursor.execute(sql_statement)

        self.database.commit()

    pass

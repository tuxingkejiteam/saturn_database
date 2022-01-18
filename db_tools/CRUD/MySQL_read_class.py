import sys
import os
import datetime
from pathlib import Path
from db_tools.tools.Img_class import LabelInfo


class Read(object):
    # 用于查询数据库的类
    def __init__(self, database, db_cursor):
        self.db_cursor = db_cursor
        self.database = database
        # 读取标签信息表，形成了一个标签和大类的一一对应的字典，方便后续使用和查询。
        sql_statement = "SELECT * FROM `标签信息表`;"
        self.db_cursor.execute(sql_statement)
        label_info = list(self.db_cursor.fetchall())
        self.label_dic = {}
        for item in label_info:
            self.label_dic[item[0]] = item[1:]

        self.json = LabelInfo  # 读取json信息的类，使用时传入json文件的路径。
        self.date = self.Operation_date()  # 获取操作时的日期信息

    def all_label(self) -> None:
        # 输出所有已经录入数据库的标签
        for key in self.label_dic:
            print(key)

    def __query_UC(self, label_list, scope='and'):
        # 标签信息解析
        query_dic = self.__label_analyze(label_list)
        UC_set = set()  # 唯一编码不允许重复，用集合来存储
        # 分表查询
        for main_class, subclass in query_dic.items():
            conditions = ''
            for describe in subclass:
                if describe != '日期':
                    conditions += "{}=TRUE {} ".format(describe, scope)
            # 形成的condition字符串，最后五位为：' AND '，需要去掉

            sql_statement = "SELECT 唯一编码 FROM `{}` WHERE {};".format(main_class, conditions[:-5])
            self.db_cursor.execute(sql_statement)
            label_info = self.db_cursor.fetchall()
            for item in label_info:
                UC_set.add(item[0])  # 将查询到的唯一编码添加到集合当中去。

        return UC_set

    def export_data(self, label_list, scope='and', save_path=''):
        UC_set = self.__query_UC(label_list, scope=scope)
        label_set = set(label_list)
        for UC in UC_set:
            UC_json = self.__get_json(UC)
            for item in UC_json.objects:
                if UC_json.objects[item]['label'] in label_set:
                    print(11111)
                    pass
                    # TODO：这里要写一个写xml文件的函数
                else:
                    pass
            # TODO：保存xml和图片到指定路径。

        pass

    def md5_in_db(self, md5):
        # 通过md5，返回一个UC。新md5则会生成一个新值，旧md5则会使用旧值。
        sql_statement = "SELECT UC FROM `md5_uc` WHERE MD5='{}';".format(md5)
        self.db_cursor.execute(sql_statement)
        uc_info = self.db_cursor.fetchall()
        if len(uc_info) == 1:
            return True, uc_info[0][0]  # md5已经存在与数据库，则返回已有的UC
        else:
            return False, ''  # md5不存在于数据库

    def get_coding_num(self, uc_date) -> int:
        sql_statement = "SELECT 已使用数量 FROM `record` WHERE 日期编码='{}';".format(uc_date)
        self.db_cursor.execute(sql_statement)
        coding_num = self.db_cursor.fetchall()
        if len(coding_num) == 0:
            print("warning!有日子没有弄record了。")
            return 0
        else:
            return coding_num[0][0]

    def __get_json(self, UC):
        # 通过唯一编码，返回该编码对应的json标注信息，私有函数，禁止外部调用

        # TODO:这里需要嵌入一个通过UC来寻找json路径的函数。
        json_path = 'output_json/Clc0007.json'
        json_class = self.json(json_path)  # 读取实例化的json文件
        return json_class

    def __label_analyze(self, label_list):
        # 分析查询的标签当中有哪些字段，私有函数，禁止外部调用。
        query_dic = {}
        label_sub_class = {}
        for label in label_list:
            if label not in self.label_dic.keys():
                print('标签：{}未导入数据库，请核实！'.format(label))
                continue
            elif self.label_dic[label][3] == 1:
                # TODO:还未支持特殊标签查询
                pass
            else:
                label_info = self.label_dic[label]
                label_main_class = label_info[0]
                # 更新小类字典
                label_sub_class[label_info[1]] = True  # 部件名
                label_sub_class[label_info[2]] = True  # 描述名
                label_sub_class['日期'] = label_info[4]  # 上次更新的日期

                query_dic[label_main_class] = label_sub_class
        return query_dic

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

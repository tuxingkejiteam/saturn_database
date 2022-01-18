import datetime
import sys
import os
from tqdm import tqdm
from pathlib import Path
from db_tools.tools.Img_class import LabelInfo


class Create(object):
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

    def add_md5_uc_info(self, md5, uc):
        # 将md5信息，添加到md5_uc这个表中
        sql_statement = "INSERT INTO md5_uc (MD5,UC) VALUES('{}','{}');".format(md5, uc)
        self.db_cursor.execute(sql_statement)  # 执行语句
        pass

    def add_json(self, json_file: str):
        # 此函数用于在数据库中添加一组记录。既支持传入单个json文件路径，也支持导入当前路径下的全部json文件。
        # 形成json的文件列表
        json_file_list = []
        if json_file.endswith('.json'):
            json_file_list.append(json_file)
        elif Path(json_file).is_dir():
            json_file_list = os.listdir(json_file)
        else:
            print('数据导入错误！')
            sys.exit(-1)

        for json_path in tqdm(json_file_list):  # 这里是进度条
            if json_path.endswith('.json'):
                json_class = self.json(json_path)  # 读取实例化的json文件
                # new_record = self.__check_uc(json_class.unique_code)  # 检查是否为新入库的数据。
                new_record = True
                if new_record:  # 新增数据记录
                    self.__add_new_json(json_class)
            self.database.commit()  # 提交修改

    def __data_init(self, json_class):
        # 此函数的作用，是将每一个json文件都必然含有的信息写入数据库。
        # 在调用add_json函数时，自动调用此函数，禁止外部调用。

        # 在图片大类表中，初始化一条记录: UC，长宽，MD5
        if json_class.objects_num == 0:  # 若图片中没有object的标注信息，则视为裸图
            without_info = 'TRUE'
        else:
            without_info = 'FALSE'
        sql_statement = "INSERT INTO 图片大类表 (唯一编码,历史遗留,可见光,裸图) VALUES('{}',{},{},{});" \
            .format(json_class.unique_code, json_class.trace, json_class.visible, without_info)
        self.db_cursor.execute(sql_statement)  # 执行语句

        # 在其他信息表中，添加UC，原名，宽高，md5几条信息。
        sql_statement = "INSERT INTO 其他信息表 (唯一编码,原名,宽,高,md5) VALUES('{}','{}',{},{},'{}');" \
            .format(json_class.unique_code, json_class.org_name, json_class.W, json_class.H, json_class.MD5)
        self.db_cursor.execute(sql_statement)  # 执行语句

    def __add_new_json(self, json_class) -> None:
        # TODO:将已标注目标全部置为0，若文件中确实含有此标签，则将0修改为1

        # 私有函数，禁止外部访问，仅通过add_json函数调用。
        # self.__data_init(json_class)  # 初始化json中必然含有的信息。
        object_dic = json_class.objects

        # 大类字典
        main_class_dic = {}
        # 部件名和描述字典
        part_describe_dic = {}
        # 含有的标签字典
        label_in_json = {}
        # 标注类型字典
        label_type = {}

        # 遍历json中的所有标签，找到其中含有的全部：大类，部件和描述
        for key in object_dic:
            label = object_dic[key]['label']
            if label not in self.label_dic.keys():
                # 检查json中是否含有不明标签，若含有不明标签，则跳过此条数据，并打印信息。
                print('{}文件出现不明标签：{}，已跳过该标签！'.format(json_class.unique_code, label))
                continue

            label_in_json[label] = True  # 为记录标签的更新日期，将json中含有的标签记录下来。
            main_class = self.label_dic[label][0]  # 获取大类表的名称
            part_name = self.label_dic[label][1]  # 获取部件名称
            part_describe = self.label_dic[label][2]  # 获取部件的描述
            # special_label = self.label_dic[label][3]  # 是否为特殊标注
            label_type[object_dic[key]['shape_type']] = True

            # 对三个字典进行更新
            main_class_dic[main_class] = True
            part_describe_dic[part_name] = main_class
            part_describe_dic[part_describe] = main_class

        # 更新标签信息表
        for label in label_in_json:
            sql_statement = "UPDATE 标签信息表 SET 更新日期={} where `标签`='{}'".format(self.date, label)
            self.db_cursor.execute(sql_statement)  # 执行语句

        # TODO:更新其他信息表中的标注方式

        # 拼接图片大类表的SQL语句
        for key in main_class_dic:
            # 更新图片大类表
            sql_statement = "UPDATE 图片大类表 SET {}=True where `唯一编码`='{}'".format(key, json_class.unique_code)
            self.db_cursor.execute(sql_statement)  # 执行语句

            # TODO:这里需要反复遍历标签字典，逻辑有点迷，后续将优化
            # 拼接小类表的SQL语句
            name_part = ''
            bool_part = ''
            for item in part_describe_dic:
                name_part += ',{}'.format(item)
                bool_part += ',True'
                pass
            # 更新标签对应的小类表
            sql_statement = "INSERT INTO {} (唯一编码{}) VALUES('{}'{});" \
                .format(key, name_part, json_class.unique_code, bool_part)
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

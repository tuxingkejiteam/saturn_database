import datetime
from core.jsonInfo import JsonInfo


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
        # 将md5信息，添加到MD5对照表中
        sql_statement = "INSERT IGNORE INTO `MD5对照表` (MD5,UC) VALUES('{}','{}');".format(md5, uc)
        self.db_cursor.execute(sql_statement)  # 执行语句
        self.database.commit()  # 提交add_md5_uc_info的修改。很不爽。

    def add_json_label_to_db(self, json_list: list, confidence: bool, label_list=None) -> bool:
        # 传入一个json的路径列表。可以传入label_list，只会按照label_list中的标签进行更新，若confidence为True则必须传入。
        label_dic = {}
        if len(label_list) == 0:
            print("标签列表不可为空。")
            return False
        else:
            for item in label_list:
                label_dic[item] = True

        for json_path in json_list:
            json_class = self.json_parsing(json_path)  # 读取实例化的json文件
            self.__add_new_json(json_class, confidence=confidence, label_dic=label_dic)
            print("解析完成：{}".format(json_path))
        print("正在写入数据库......")
        self.database.commit()  # 提交修改
        return True

    def __add_new_json(self, json_class, label_dic=None, confidence=False) -> None:
        # 私有函数，禁止外部访问，仅通过add_json函数调用。
        object_list = json_class.objects
        label_in_json_has_add = {}  # 保存json中含有的标签

        add_confidence = int(confidence)
        if label_dic is None:  # 如果未传入参数，则将json中的标签写入label_dic
            label_dic = {}
            # for item in object_list:
            #     label_dic[item.label] = True

        # 遍历目标列表
        for item in object_list:
            label = item.label
            # if label not in self.label_dic.keys():
            #     # 检查json中是否含有不明标签。暂时不启用这个功能
            #     # continue
            #     pass

            if label in label_in_json_has_add:
                # 如果标签已经更新过了，这个物体就跳过
                continue
            if label in label_dic:  # 如果标签在标签字典里面，则根据是否增加置信度进行写入
                sql_statement = "INSERT INTO `目标标注表` VALUES ('{}', '{}', 1) ON DUPLICATE KEY UPDATE 置信度=置信度+{};" \
                    .format(json_class.unique_code, label, add_confidence)
                self.db_cursor.execute(sql_statement)  # 执行语句
            elif len(label_dic) == 0:  # 如果标签不在字典里面，且标签字典为空，则什么都插入
                # sql_statement = "INSERT INTO `目标标注表` VALUES ('{}', '{}', 1) ON DUPLICATE KEY UPDATE 置信度=置信度;" \
                #     .format(json_class.unique_code, label)
                sql_statement = "INSERT IGNORE INTO `目标标注表` VALUES ('{}', '{}', 1);" \
                    .format(json_class.unique_code, label)
                self.db_cursor.execute(sql_statement)  # 执行语句
            else:  # 物体的标签不在指定的标签字典里面，则什么都不做
                pass

            label_in_json_has_add[label] = True  # 为记录标签的更新日期，将json中含有的标签记录下来。

        # 还要更新一下json中没有，但是存在于标签列表中的标签。
        if confidence:
            for label_mark in label_dic:
                if label_mark not in label_in_json_has_add:
                    sql_statement = "INSERT INTO `目标标注表` VALUES ('{}', '{}', -1) ON DUPLICATE KEY UPDATE 置信度=置信度+{};" \
                        .format(json_class.unique_code, label_mark, '-1')
                    self.db_cursor.execute(sql_statement)  # 执行语句

        # 更新标签信息表。
        for label in label_in_json_has_add:
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

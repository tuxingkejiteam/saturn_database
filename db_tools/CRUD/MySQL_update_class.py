import datetime
from Img_class import LabelInfo


class Update(object):
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

    def UC_labeled(self, label_list, UC_list):
        # 导入标签后，需要明确哪些图片已经标注过，但没有标注目标，该段程序会将NULL的信息修改为0，表示没有信息
        # 标签信息解析
        query_dic = self.__label_analyze(label_list)

        pass

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
    pass

import datetime
from core.jsonInfo import JsonInfo


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

        self.json = JsonInfo  # 读取json信息的类，使用时传入json文件的路径。
        self.date = self.Operation_date()  # 获取操作时的日期信息

    def query_json_label_info_from_uc_label(self, uc_list: list, label_list: list):
        label_info_list = [{} for i in range(len(uc_list))]
        count = 0
        for uc in uc_list:
            sql_statement = "SELECT `标签`, `置信度` FROM `目标标注表` WHERE `唯一编码`='{}'".format(uc)
            self.db_cursor.execute(sql_statement)
            label_info = self.db_cursor.fetchall()
            one_uc_label = {}
            for one_label in label_info:
                one_uc_label[one_label[0]] = one_label[1]
            label_info_list[count][uc] = one_uc_label
            count += 1
        return label_info_list

    def all_label(self) -> None:
        # 输出所有已经录入数据库的标签
        for key in self.label_dic:
            print(key)

    def md5_in_db(self, md5):
        # 通过md5，返回一个UC。新md5则会生成一个新值，旧md5则会使用旧值。
        sql_statement = "SELECT UC FROM `MD5对照表` WHERE MD5='{}';".format(md5)
        self.db_cursor.execute(sql_statement)
        uc_info = self.db_cursor.fetchall()
        if len(uc_info) == 1:
            return True, uc_info[0][0]  # md5已经存在与数据库，则返回已有的UC
        else:
            return False, ''  # md5不存在于数据库

    def query_uc_list_from_label(self, label_list: list, conf: int = 1, MODE='AND') -> list:
        # 选取所有置信度的绝对值达到conf以上的数据。
        # 默认1次过图即做输出。不做强制输入要求。

        label_condition = ''
        # conf_condition = '置信度>={} OR 置信度<=-{}'.format(conf, conf)
        for label in label_list:
            label_condition += "标签='{}' OR ".format(label)
        label_condition = label_condition[:-4]  # 去掉最后面的" OR "
        num_label = len(label_list)

        # 拼接条件语句，屎山if-else
        if MODE == 'AND':
            conf_condition = '置信度>={} OR 置信度<=-{}'.format(conf, conf)
            sql_statement = "SELECT 唯一编码 FROM `目标标注表` WHERE ({}) AND ({}) GROUP BY `唯一编码` HAVING COUNT(`唯一编码`)={};" \
                .format(label_condition, conf_condition, num_label)
        elif MODE == 'OR':
            conf_condition = '置信度>={} OR 置信度<=-{}'.format(conf, conf)
            sql_statement = "SELECT 唯一编码 FROM `目标标注表` WHERE ({}) AND ({}) GROUP BY `唯一编码`;" \
                .format(label_condition, conf_condition)
        elif MODE == 'EXIST':
            conf_condition = '置信度>={}'.format(conf)
            sql_statement = "SELECT 唯一编码 FROM `目标标注表` WHERE ({}) AND ({}) GROUP BY `唯一编码`;" \
                .format(label_condition, conf_condition)
        elif MODE == 'NOT_EXIST':
            conf_condition = '置信度<=-{}'.format(conf)
            sql_statement = "SELECT 唯一编码 FROM `目标标注表` WHERE ({}) AND ({}) GROUP BY `唯一编码`;" \
                .format(label_condition, conf_condition)
        else:
            print("未识别的模式参数。")
            return []

        self.db_cursor.execute(sql_statement)
        uc_tuple_list = self.db_cursor.fetchall()
        uc_list = []
        for uc_tuple in uc_tuple_list:
            uc_list.append(uc_tuple[0])
        return uc_list

    def get_coding_num(self, uc_date) -> int:
        sql_statement = "SELECT 已使用数量 FROM `编码使用记录表` WHERE 日期编码='{}';".format(uc_date)
        self.db_cursor.execute(sql_statement)
        coding_num = self.db_cursor.fetchall()
        if len(coding_num) == 0:
            # print("warning!有日子没有弄record了。")
            sql_statement = "INSERT INTO `编码使用记录表` (`日期编码`,`已使用数量`) VALUES ('{}',0);".format(uc_date)
            self.db_cursor.execute(sql_statement)
            self.database.commit()
            return 0
        else:
            return coding_num[0][0]

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

import pymysql
import json
from time import time
import datetime
from db_tools.CRUD.MySQL_create_class import Create
from db_tools.CRUD.MySQL_delete_class import Delete
from db_tools.CRUD.MySQL_read_class import Read
from db_tools.CRUD.MySQL_update_class import Update


class SaturnSQL(object):
    # @staticmethod
    # def help(seek: str):
    #     # PyMySQL接口的帮助文档。打印相关的操作信息。
    #     if seek == 'MySQL':
    #         print(seek, '类的作用为：')
    #         print('此类中定义了数据库相关的函数。在进行数据库的相关操作时，会将json文件中的所选信息同步至数据库。')
    #         print('运行此程序的时候，SQLyog要处于开启的状态，否则会报错。')
    #         return None
    #
    #     if seek == 'read_json':
    #         print(seek, '函数的作用为：')
    #         print('传入json文件的路径，返回一个含有标注信息的类，该类的定义可通过help(LabelInfo)来查询')
    #         return None
    #
    #     if seek == 'data_init':
    #         print(seek, '函数的作用为：')
    #         print('此函数的作用，是将每一个json文件都必然含有的信息写入数据库。包括：唯一编码，图片原名，长宽，是否为裸图，MD5值')

    def __init__(self, host='192.168.3.101', user='root', password='', db_name='Saturn_Database_V1'):
        """

        :rtype: object
        """
        # TODO:调用之前，检查json文件是否是已经存在的文件。
        # 启动数据库函数。若启动失败，则报出错误并优雅地终止程序。
        # 入参：数据库服务器地址，用户名，密码，数据库名
        # 出参：用户名，地址，数据库名，密码，数据库，游标形式的数据库，大类小类对照表，json标注信息类。
        self.user = user
        self.host = host
        self.db_name = db_name

        if password == '':
            # TODO:输入密码时，需使用暗文显示。当前为明文。
            self.password = input('请输入{}用户密码：'.format(self.user))
        else:
            self.password = password
        self.database = pymysql.connect(host=self.host,
                                        user=self.user,
                                        password=self.password,
                                        database=self.db_name
                                        )
        print('数据库连接成功！版本号：1.0')
        self.db_cursor = self.database.cursor()

        # 初始化增删查改的四个代码库:CRUD
        self.C = Create  # 增
        self.D = Delete  # 删
        self.R = Read  # 查
        self.U = Update  # 改

        # with open('db_tools/docs/record.json') as data:
        #     self.record = json.load(data)

        self.comparison_tabel = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9',
                                 10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f', 16: 'g', 17: 'h', 18: 'i',
                                 19: 'j', 20: 'k', 21: 'm', 22: 'n', 23: 'p', 24: 'q', 25: 'r', 26: 's', 27: 't',
                                 28: 'u', 29: 'v', 30: 'w', 31: 'x', 32: 'y', 33: 'z'}
        self.year_dict = {2019: 'A', 2020: 'B', 2021: 'C', 2022: 'D', 2023: 'E', 2024: 'F', 2025: 'G'}

    def add_json_to_db(self, json_path_list: list, label_list=None, confidence=False, ) -> bool:
        # 将json中有的信息写入数据库
        # 是否更新置信度区间。
        succeed = False
        if label_list is None:
            print("未传入标签列表！")
            return succeed

        C = self.C(self.database, self.db_cursor)
        succeed = C.add_json_to_db(json_path_list, confidence=confidence, label_list=label_list)
        return succeed

    def clear_all_table(self) -> bool:
        # 删除数据库中所有表的内容。连个毛都不剩下
        if self.user == 'root':
            sql_statement = "TRUNCATE TABLE 图片大类表;"
            self.db_cursor.execute(sql_statement)  # 执行语句

            sql_statement = "TRUNCATE TABLE 目标标注表;"
            self.db_cursor.execute(sql_statement)  # 执行语句
            print("删库跑路了！")
            return True
        else:
            print("无清空权限！")
            return False

    def delete(self, UC):
        # 对数据库进行删除数据操作
        D = self.D(self.database, self.db_cursor)
        # TODO:删除功能需要添加

    def read(self, label_list, need='UC'):
        # 对数据库进行读取操作
        R = self.R(self.database, self.db_cursor)
        if need == 'UC':
            result_list = R.export_data(label_list, scope='and')  # 按标签进行查询。
            # 传入标签的列表，以及全包含还是不全包含。
        else:
            result_list = 0

        return result_list

    # 给一个md5，返回一个uc
    def get_uc_list(self, md5_list: list) -> list:
        # 实例化需要用到的操作：读和写
        R = self.R(self.database, self.db_cursor)
        C = self.C(self.database, self.db_cursor)

        # 获取当前日期的已编码数量
        uc_date = self.__first_3_letters()

        uc_list = ['' for i in range(len(md5_list))]  # 初始化uc列表，长度与md5列表相同
        new_data_num = 0  # 记录新录入的md5数量

        count = 0
        for md5 in md5_list:
            result = R.md5_in_db(md5)  # 查询md5是否出现在了数据库当中
            if result[0]:
                uc_list[count] = result[1]
            else:
                new_data_num += 1
            count += 1

        # 查询后立刻更新record表，尽快占坑
        coding_num = R.get_coding_num(uc_date)  # 查询一个当日已编码数量
        # TODO:更新操作，暂时不用update类
        sql_statement = "UPDATE record SET 已使用数量={} WHERE 日期编码='{}';".format(coding_num + new_data_num, uc_date)
        self.db_cursor.execute(sql_statement)  # 执行语句
        self.database.commit()  # 立即提交修改

        # 根据新数据的数量，统一申请一个UC编码的list
        new_uc_list = self.__apply_for_uc(new_data_num, coding_num, uc_date)

        count = 0
        for idx, item in enumerate(uc_list):
            if item == '':
                C.add_md5_uc_info(md5_list[idx], new_uc_list[count])  # 将MD5和UC插入数据库
                uc_list[idx] = new_uc_list[count]
                count += 1
            else:
                pass
        self.database.commit()  # 提交add_md5_uc_info的修改。很不爽。

        return uc_list

    def __apply_for_uc(self, new_num, coding_num, uc_date) -> list:
        # 使用一个编码的上下界，申请一个新uc的列表
        uc_rank_list = []
        for i in range(coding_num + 1, coding_num + new_num + 1):
            uc_rank_list.append(uc_date + self.__coding_rank(i))
        return uc_rank_list

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

    def __first_3_letters(self) -> str:
        # 获取日期编码
        date = datetime.datetime.now()
        year = date.year
        month = date.month
        day = date.day
        letter_1 = self.year_dict[year]

        if day <= 15:
            letter_2 = self.comparison_tabel[month + 9]  # 上半月，月份从a开始
            letter_3 = self.comparison_tabel[day + 9]
        else:
            letter_2 = self.comparison_tabel[month + 9 + 12]  # 下半月，月份从m开始
            letter_3 = self.comparison_tabel[day - 15 + 9]

        return letter_1 + letter_2 + letter_3

    def __coding_rank(self, serial_number) -> str:
        # 获取序列，编码至四位。每位有34种选择。
        # 方法：整除取余法
        assert serial_number <= 1336336, "编码溢出，操作终止！"
        remainder_1 = serial_number % 34  # 取余数
        quotient_1 = serial_number // 34

        remainder_2 = quotient_1 % 34  # 取余数
        quotient_2 = quotient_1 // 34

        remainder_3 = quotient_2 % 34  # 取余数
        quotient_3 = quotient_2 // 34

        remainder_4 = quotient_3 % 34  # 取余数
        assert quotient_3 // 34 == 0, '编码溢出，操作终止！'
        letter_4 = self.comparison_tabel[remainder_4]
        letter_5 = self.comparison_tabel[remainder_3]
        letter_6 = self.comparison_tabel[remainder_2]
        letter_7 = self.comparison_tabel[remainder_1]

        return letter_4 + letter_5 + letter_6 + letter_7

    def __str__(self):
        # 打印数据库中的所有表格名
        self.db_cursor.execute('SHOW TABLES')
        table_tuple = self.db_cursor.fetchall()
        out_str = ''
        # 递归到
        for item in table_tuple:
            out_str += item[0] + ','
        return out_str[0:-1]

    def __del__(self):
        # 断开数据库连接。
        try:
            # TODO: 数据库断开连接时存在问题
            self.database.close()
        except TypeError:
            # print("已知bug（1）")
            pass
        print('数据库连接已断开！')

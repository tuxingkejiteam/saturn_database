import pymysql
import json
from time import time
from CRUD.MySQL_create_class import Create
from CRUD.MySQL_delete_class import Delete
from CRUD.MySQL_read_class import Read
from CRUD.MySQL_update_class import Update


class MySQL(object):
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

    def __init__(self, host='localhost', user='root', password='', db_name='Saturn_Database'):
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

        with open('docs/record.json') as data:
            self.record = json.load(data)

        comparison_table = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10,
                            'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15, 'g': 16, 'h': 17, 'i': 18, 'j': 19, 'k': 20,
                            'm': 21, 'n': 22, 'p': 23, 'q': 24, 'r': 25, 's': 26, 't': 27, 'u': 28, 'v': 29, 'w': 30,
                            'x': 31, 'y': 32, 'z': 33}
        self.comparison_table = comparison_table

        # 计时模块
        self.start_time = time()

    def create(self, json_file) -> bool:
        # 对数据库进行添加数据操作
        C = self.C(self.database, self.db_cursor)
        succeed = C.add_json(json_file)
        return succeed

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

    def __check_uc(self, UC: str) -> bool:
        # 检查该数据是否已经在数据库当中
        key_as_date = UC[0:3]
        num_of_data = UC[-4:]
        letter_1 = int(self.comparison_table[num_of_data[0]])
        letter_2 = int(self.comparison_table[num_of_data[1]])
        letter_3 = int(self.comparison_table[num_of_data[2]])
        letter_4 = int(self.comparison_table[num_of_data[3]])
        count = letter_1 * 34 * 34 * 34 + letter_2 * 34 * 34 + letter_3 * 34 + letter_4
        if int(self.record[key_as_date]) >= int(count):
            return True
        else:
            return False

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
        self.database.close()
        print('操作耗时：{:.4f}s'.format(time() - self.start_time))
        print('数据库连接已断开！')

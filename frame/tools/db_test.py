# -*- coding: utf-8  -*-
# -*- author: jokker -*-


from JoTools.utils.MySqlUtil import MySqlUtil
from JoTools.utils.HashlibUtil import HashLibUtil
from JoTools.utils.JsonUtil import JsonUtil

# todo 数据库相关操作


a = MySqlUtil()

a.conoect_mysql('192.168.3.101', 3306, 'root', 'root123', 'modelcore2', charset='utf8')

# b = a.cursor.execute("show tables;")
#
# c = a.cursor.fetchall()
#
# print(c)
#
#
# exit()


# # # todo 新建一张表
# sql = """CREATE TABLE md5_uc2 (
#          MD5  CHAR(32),
#          UC  CHAR(7) )"""
#
# a.cursor.execute(sql)

# sql = "show create table md5_uc2"
# a.cursor.execute(sql)
# print(a.cursor.fetchall())

# sql = "INSERT INTO md5_uc2(MD5,UC) VALUES ('00fa186e8d4d6660b49ddef8a35a77de','1234567')"
#
# a.cursor.execute(sql)
# a.db.commit()

#
# a.cursor.execute("show tables;")
# print(a.cursor.fetchall())

# record = JsonUtil.load_data_from_json_file(r"D:\Algo\saturn_database\db_tools\jiahao_secret\all_MD5.json")
#
# for each_md5 in record:
#
#     # 表中插入数据
#     sql = """INSERT INTO md5_uc(MD5,UC)
#              VALUES ('{0}','{1}')""".format(each_md5, record[each_md5])
#
#
#     print(sql)
#
#     a.cursor.execute(sql)
#
# a.db.commit()
# print(a.cursor.fetchall())
#

# 查看表中的所有数据

sql = """SELECT * from md5_uc"""
a.cursor.execute(sql)
res = a.cursor.fetchall()

print(len(res))

print("OK")

for each in res:
    print(each)

















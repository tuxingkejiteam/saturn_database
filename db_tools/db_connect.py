from CRUD.MySQL_class import SaturnSQL

mysql = SaturnSQL(user='root', password='root123', host='192.168.3.101')  # 启动数据库，并实例化数据库接口的方法类。
# mysql.R.all_label()


# if __name__ == "__main__":
#     mysql = MySQL(password='fly1031')  # 启动数据库，并实例化数据库接口的方法类。
#     mysql.R.all_label()
#     # json_path = 'output_json/Clc0007.json'
#     # mysql.create(json_path)
#     # uc = 'Clc0007'
#     # mysql.delete(uc)
#
#     # label_list = ['cpb_ps']
#     # mysql.read(label_list)
#     pass

import numpy as np
import cv2
img_path = "D:\工作之禁忌之地\数据库建立\saturn_database\微信截图_20220119202753.png"
# a = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)  # 格式为BGR
#
# #a = np.ones((3, 4)).astype(np.uint8)
# # a = np.random.randn(3, 4, 4).astype(np.uint8)
# b = a.tobytes()
# aaa = map(int, b)
# d = list(map(int, b))
# c = np.array(d, dtype=a.dtype).reshape(a.shape)

sql = "INSERT INTO `img_bit` VALUES ('test03', LOAD_FILE('{}'));".format(img_path)
mysql.db_cursor.execute(sql)  # 执行语句
mysql.database.commit()

sql = "SELECT `bit` FROM `img_bit` WHERE `name`='test03'"
mysql.db_cursor.execute(sql)  # 执行语句
mysql.database.commit()

label_info = list(mysql.db_cursor.fetchall())[0][0]
e = list(map(int, label_info))
f = np.array(d, dtype=a.dtype).reshape(a.shape)
pass

# class TestClass:
#     a: int
#     b: str
#     c: int
#     d: int
#
#
# attr_dict = {
#     "a": -1,
#     "b": 's',
#     "c": 1,
#     "e": 1
# }
#
# obj = TestClass()
# obj.a = 10
# obj.b = "hello"
# obj.c = 100
# obj.d = 200
# attr_list = dir(obj)
#
# for key in attr_dict:
#     if key in attr_list:
#         if key == 'a':
#             obj.a = ...
#         aa = getattr(obj, key)
#         attr_dict[key] = getattr(obj, key)
# print(hasattr(obj, 'a'))
# # print(attr_dict)

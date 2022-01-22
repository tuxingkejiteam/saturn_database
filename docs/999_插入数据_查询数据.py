# -*- coding: utf-8  -*-
# -*- author: jokker -*-


import os
import shutil
from core.jsonInfo import JsonInfo
from core.jsonOpt import Opt
from JoTools.utils.FileOperationUtil import FileOperationUtil

from db_tools.CRUD.MySQL_class import SaturnSQL
import os


mysql = SaturnSQL(user='root', password='root123', host='192.168.3.101', db_name='Saturn_Database_V1')


# # 根据json的路径列表写入数据库示例---------------------
# data_dir = '功能测试用数据'
# json_list = []  # 这里先计算一个json的路径列表。
# for data in os.listdir(data_dir):
#     if data.endswith('.json'):
#         json_path = os.path.join(data_dir, data)
#         json_list.append(json_path)


opt = Opt()
opt.load_buffer()

# 插入数据
# uc_list = opt.get_uc_list_by_label_from_root_buffer(need_label_list='Fnormal')
#
# json_path_list = []
#
# for each_uc in uc_list[:10]:
#     json_path = opt.get_json_img_path_from_uc(each_uc)[0]
#     json_path_list.append(json_path)
#     each_json_info = JsonInfo(json_path)
#     a = each_json_info.count_tags()
#     print(a)
#
#
# label_list = ['Fnormal', 'fzc_broken']
# result = mysql.add_json_to_db(json_path_list, label_list=label_list, confidence=True)
# print(result)


# 查询数据

label_list = ['Fnormal']
uc_list = mysql.query_uc_list_from_label(label_list, conf=0, AND=True)
print(len(uc_list))
print(uc_list)


opt.get_xml_dataset_by_uc_list(uc_list[:50], r"C:\Users\14271\Desktop\del\root_dir\test_find")



# -*- coding: utf-8  -*-
# -*- author: jokker -*-


import os
from core.jsonInfo import JsonInfo
from core.jsonOpt import JsonOpt
from JoTools.utils.FileOperationUtil import FileOperationUtil
from JoTools.utils.HashlibUtil import HashLibUtil
from db_tools.CRUD.MySQL_class import SaturnSQL


# 读取 xml 中的内容，存放到数据库中

# todo 如果 json 存在，更新 json 中的 obj 数据，部分 attr 数据不进行更新
# todo 如果 img 存在，不复制 img
# todo 如果文件名本身就是符合 uc 规范的，可以不计算 md5 找到对应的 uc，可以直接使用

xml_dir = r"D:\data\001_fzc_优化相关资料\dataset_fzc\000_0_标准测试集\Annotations"
img_dir = r"D:\data\001_fzc_优化相关资料\dataset_fzc\000_0_标准测试集\JPEGImages"

opt = JsonOpt()
host="192.168.3.101"
user="root"
password="root123"
db_name="Saturn_Database_V1"
sql_zy = SaturnSQL(host=host, user=user, password=password, db_name=db_name)

label_list = []

index, json_path_list = 0,  []
for each_img_path in FileOperationUtil.re_all_file(img_dir, endswitch=['.jpg', '.JPG', '.png', '.PNG']):
    index += 1
    print(index, each_img_path)
    xml_name = FileOperationUtil.bang_path(each_img_path)[1] + '.xml'
    each_xml_path = os.path.join(xml_dir, xml_name)

    each_hash = HashLibUtil.get_file_md5(each_img_path)
    uc = sql_zy.get_uc_list([each_hash])[0]

    # print(each_img_path)
    # print(each_xml_path)
    print(uc)
    print('-'*20)

#     # 获取标准 json
#     json_path, img_path = opt.get_json_from_xml(each_xml_path, each_img_path)
#     # 标准 json 入库
#     opt.add_uc_to_root(json_path, img_path, is_clip=True)
#     json_path_list.append(json_path)
#
# # 更新入数据库
# opt.add_json_label_to_db(json_path_list, label_list, confidence=True)



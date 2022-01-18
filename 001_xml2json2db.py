# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import os
from core.jsonInfo import JsonInfo
from core.opt import Opt
from JoTools.utils.FileOperationUtil import FileOperationUtil


# 读取 xml 中的内容，存放到数据库中


xml_dir = r"C:\Users\14271\Desktop\del\del"
img_dir = r"C:\Users\14271\Desktop\del\del"
conf_path = r"D:\Algo\saturn_database\config.ini"

opt = Opt(conf_path)

for each_img_path in FileOperationUtil.re_all_file(xml_dir, endswitch=['.jpg', '.JPG', '.png', '.PNG']):
    xml_name = FileOperationUtil.bang_path(each_img_path)[1] + '.xml'
    each_xml_path = os.path.join(xml_dir, xml_name)
    # 获取标准 json
    json_path, img_path = opt.get_json_from_xml(each_xml_path, each_img_path)
    # 标准 json 入库
    opt.add_uc_to_root(json_path, img_path, is_clip=True)







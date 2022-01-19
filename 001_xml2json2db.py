# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import os
from core.jsonInfo import JsonInfo
from core.opt import Opt
from JoTools.utils.FileOperationUtil import FileOperationUtil


# 读取 xml 中的内容，存放到数据库中


xml_dir = r"D:\data\001_fzc_优化相关资料\dataset_fzc\000_0_标准测试集\Annotations"
img_dir = r"D:\data\001_fzc_优化相关资料\dataset_fzc\000_0_标准测试集\JPEGImages"
conf_path = r"D:\Algo\saturn_database\config.ini"

opt = Opt(conf_path)

index = 0
for each_img_path in FileOperationUtil.re_all_file(img_dir, endswitch=['.jpg', '.JPG', '.png', '.PNG']):
    index += 1
    print(index, each_img_path)
    xml_name = FileOperationUtil.bang_path(each_img_path)[1] + '.xml'
    each_xml_path = os.path.join(xml_dir, xml_name)
    # 获取标准 json
    json_path, img_path = opt.get_json_from_xml(each_xml_path, each_img_path)
    # 标准 json 入库
    opt.add_uc_to_root(json_path, img_path, is_clip=True)
    # 更新入数据库
    # opt.add_json_to_db()






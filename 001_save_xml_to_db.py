# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import os
from core.jsonInfo import JsonInfo
from core.jsonOpt import JsonOpt
from JoTools.utils.FileOperationUtil import FileOperationUtil
from core.ucDatasetOpt import UcDataset, UcDatasetOpt

# ----------------------------------------------------------------------------------------------------------------------
xml_dir = r"D:\data\001_fzc_优化相关资料\dataset_fzc\000_0_标准测试集\Annotations"
img_dir = r"D:\data\001_fzc_优化相关资料\dataset_fzc\000_0_标准测试集\JPEGImages"
label_list = ['Fnormal', 'fzc_broken']
# ----------------------------------------------------------------------------------------------------------------------

opt = JsonOpt()
index, json_path_list = 0,  []

for each_img_path in FileOperationUtil.re_all_file(img_dir, endswitch=['.jpg', '.JPG', '.png', '.PNG']):
    index += 1
    print(index, each_img_path)
    xml_name = FileOperationUtil.bang_path(each_img_path)[1] + '.xml'
    each_xml_path = os.path.join(xml_dir, xml_name)
    json_path, img_path = opt.add_xml_to_root(each_xml_path, each_img_path)
    json_path_list.append(json_path)

# 更新入数据库
opt.add_json_label_to_db(json_path_list, label_list, confidence=True)






# -*- coding: utf-8  -*-
# -*- author: jokker -*-


# 想找到一些数据的时候，（1）先查数据库，拿到 uc_list (2) 根据 uc list 拿到对应的数据


import os
import shutil
from core.jsonInfo import JsonInfo
from core.opt import Opt
from JoTools.utils.FileOperationUtil import FileOperationUtil

opt = Opt()

save_dir = r"C:\Users\14271\Desktop\del\root_dir\train_data"

# todo uc list 由查询得到，这边增加按条件查询代码
uc_list = ['Dnd0001', 'Dnd0002', 'Dnd0003', 'Dnd0004', 'Dnd0005', 'Dnd0006', 'Dnd0007']


for each_uc in uc_list:
    json_path, img_path = opt.get_json_img_path_from_uc(each_uc)
    # 读取 json_path, 转为 xml
    save_xml_path = os.path.join(save_dir, FileOperationUtil.bang_path(json_path)[1] + '.xml')
    save_img_path = os.path.join(save_dir, FileOperationUtil.bang_path(json_path)[1] + '.jpg')
    json_info = JsonInfo(json_path)
    json_info.save_to_xml(save_xml_path)
    shutil.copy(img_path, save_img_path)








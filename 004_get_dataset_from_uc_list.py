# -*- coding: utf-8  -*-
# -*- author: jokker -*-


# 想找到一些数据的时候，（1）先查数据库，拿到 uc_list (2) 根据 uc list 拿到对应的数据


import os
import shutil
from core.jsonInfo import JsonInfo
from core.opt import Opt
from JoTools.utils.FileOperationUtil import FileOperationUtil


save_dir = r"C:\Users\14271\Desktop\del\root_dir\train_data"

# ----------------------------------------------------------------------------------------------------------------------


# todo uc list 由查询得到，这边增加按条件查询代码
uc_list = ['Dnd0001', 'Dnd0002', 'Dnd0003', 'Dnd0004', 'Dnd0005', 'Dnd0006', 'Dnd0007']


# ----------------------------------------------------------------------------------------------------------------------

opt = Opt()

# 导出
opt.get_xml_dataset_by_uc_list(uc_list, save_dir)









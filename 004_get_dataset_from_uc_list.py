# -*- coding: utf-8  -*-
# -*- author: jokker -*-


# 想找到一些数据的时候，（1）先查数据库，拿到 uc_list (2) 根据 uc list 拿到对应的数据


import os
import shutil
from core.jsonInfo import JsonInfo
from core.jsonOpt import JsonOpt
from JoTools.utils.FileOperationUtil import FileOperationUtil


# ----------------------------------------------------------------------------------------------------------------------
save_dir = r"C:\Users\14271\Desktop\del\root_dir\fzc_error"
need_label = ['Fnormal', 'fzc_broken']
conf = 1
mode = 'OR'
# model = 'AND'
# ----------------------------------------------------------------------------------------------------------------------

opt = JsonOpt()

uc_list = opt.query_uc_list_from_label(need_label, conf, mode=mode)
opt.get_xml_dataset_by_uc_list(uc_list, save_dir)









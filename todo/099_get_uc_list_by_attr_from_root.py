# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import os
import shutil
from core.jsonInfo import JsonInfo
from core.opt import Opt
from JoTools.utils.FileOperationUtil import FileOperationUtil


save_dir = r"C:\Users\14271\Desktop\del\root_dir\train_data"


opt = Opt()
opt.load_buffer()

# 根据 label 获取 uc_list
# uc_list = opt.get_uc_list_by_label_from_root(need_label_list=['fzc_broken'])
# uc_list = opt.get_uc_list_by_label_from_root_buffer(need_label_list=['fzc_broken'])
uc_list = opt.get_uc_list_by_label_from_root_buffer(need_label_list=['fzc_gt'])
print(len(uc_list))

# 导出
# opt.get_xml_dataset_by_uc_list(uc_list, save_dir)





# -*- coding: utf-8  -*-
# -*- author: jokker -*-


import os
import shutil
from saturndatabase.core.jsonInfo import JsonInfo
from saturndatabase.core.jsonOpt import JsonOpt
from saturndatabase.core.ucDatasetOpt import UcDataset, UcDatasetOpt
from JoTools.utils.JsonUtil import JsonUtil
from JoTools.utils.FileOperationUtil import FileOperationUtil


# ----------------------------------------------------------------------------------------------------------------------
label_list = ['Fnormal', 'fzc_broken']
conf = 1
mode = 'AND'
config_path = r"D:\Algo\saturn_database\config.ini"
# ----------------------------------------------------------------------------------------------------------------------

uc_opt = UcDatasetOpt(config_path)
json_opt = JsonOpt(config_path)

uc_dataset = uc_opt.get_uc_dataset(dataset_name='fzc_test_dataset')

for each_uc in uc_dataset:
    each_json_path, each_img_path = json_opt.get_json_img_path_from_uc(each_uc)
    if os.path.exists(each_json_path):
        json_info = JsonInfo(each_json_path)
        print(json_info.extra_info)



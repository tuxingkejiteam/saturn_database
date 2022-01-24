# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import os
from core.jsonInfo import JsonInfo
from core.jsonOpt import JsonOpt
from core.ucDatasetOpt import UcDatasetOpt
from JoTools.utils.FileOperationUtil import FileOperationUtil


json_opt = JsonOpt()
uc_dataset = UcDatasetOpt()

# ----------------------------------------------------------------------------------------------------------------------
label_list = ['fzc_broken']
conf = 1
# mode = 'OR'
mode = 'AND'
attr_list = [('extra_info','fzc fzc broken')]
# ----------------------------------------------------------------------------------------------------------------------

uc_list = json_opt.query_uc_list_from_label(label_list, conf=conf, mode=mode)

json_opt.update_json_attr(uc_list=uc_list, attr_list=attr_list)

# uc_dataset.add_uc_dataset(uc_list, dataset_name='just_fzc_broken')
#
# fzc_broken_dataset = uc_dataset.get_uc_dataset(dataset_name='just_fzc_broken')
#
# for each_uc in fzc_broken_dataset:
#
#     json_path = json_opt.get_json_img_path_from_uc(each_uc)[0]
#
#     a = JsonInfo(json_path)
#
#     print(a.extra_info)
#









# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import os
from saturndatabase.core.jsonInfo import JsonInfo
from saturndatabase.core.jsonOpt import JsonOpt
from saturndatabase.core.ucDatasetOpt import UcDatasetOpt
from JoTools.utils.FileOperationUtil import FileOperationUtil


# ----------------------------------------------------------------------------------------------------------------------
label_list = ['fzc_broken']
conf = 1
# mode = 'OR'
mode = 'AND'
attr_list = [('extra_info','fzc fzc broken')]
config_path = r"D:\Algo\saturn_database\config.ini"
# ----------------------------------------------------------------------------------------------------------------------

json_opt = JsonOpt(config_path)
uc_dataset = UcDatasetOpt(config_path)

uc_list = json_opt.query_uc_list_from_label(label_list, conf=conf, mode=mode)

json_opt.update_json_attr(uc_list=uc_list, attr_list=attr_list)










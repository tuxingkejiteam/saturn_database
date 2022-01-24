# -*- coding: utf-8  -*-
# -*- author: jokker -*-


import os
import shutil
from core.jsonInfo import JsonInfo
from core.jsonOpt import JsonOpt
from JoTools.utils.FileOperationUtil import FileOperationUtil


opt = JsonOpt()

assign_uc = "Dni000c"

label_info = opt.query_label_info_from_uc_list([assign_uc])

print(label_info)

print(assign_uc, label_info[0][assign_uc].keys())

opt.del_uc_label_from_db(assign_uc, label_info[0][assign_uc].keys())

label_info = opt.query_label_info_from_uc_list([assign_uc])

print(label_info)







# -*- coding: utf-8  -*-
# -*- author: jokker -*-


import os
import shutil
from core.jsonInfo import JsonInfo
from core.jsonOpt import JsonOpt
from JoTools.utils.FileOperationUtil import FileOperationUtil

# todo fixme json 和 数据库都需要删除

# ----------------------------------------------------------------------------------------------------------------------
assign_uc = "Dni02hs"
# ----------------------------------------------------------------------------------------------------------------------


opt = JsonOpt()

label_info = opt.query_label_info_from_uc_list([assign_uc])
del_label_list = label_info[0][assign_uc].keys()

# json 库操作
json_path = opt.get_json_img_path_from_uc(assign_uc)[0]
json_info = JsonInfo(json_path)
json_info.del_obj_by_label(del_label_list)
# 数据库操作
opt.del_uc_label_from_db(assign_uc, del_label_list)



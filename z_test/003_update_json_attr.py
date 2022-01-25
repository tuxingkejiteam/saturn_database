# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import os
from SaturnDatabase.core.jsonInfo import JsonInfo
from SaturnDatabase.core.jsonOpt import JsonOpt
from SaturnDatabase.core.ucDatasetOpt import UcDatasetOpt
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










# -*- coding: utf-8  -*-
# -*- author: jokker -*-


import os
import shutil
from SaturnDatabase.core.jsonInfo import JsonInfo
from SaturnDatabase.core.jsonOpt import JsonOpt
from SaturnDatabase.core.ucDatasetOpt import UcDataset, UcDatasetOpt
from JoTools.utils.JsonUtil import JsonUtil
from JoTools.utils.FileOperationUtil import FileOperationUtil


# ----------------------------------------------------------------------------------------------------------------------
label_list = ['Fnormal', 'fzc_broken']
conf = 1
mode = 'AND'
# ----------------------------------------------------------------------------------------------------------------------


uc_opt = UcDatasetOpt()
json_opt = JsonOpt()


uc_list = json_opt.query_uc_list_from_label(label_list, conf=1, mode='AND')

uc_opt.add_uc_dataset(uc_list=uc_list, dataset_name='fzc_test_dataset', model_name='fzc', model_version='v0.0.1')


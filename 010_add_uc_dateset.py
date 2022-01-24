# -*- coding: utf-8  -*-
# -*- author: jokker -*-


import os
import shutil
from core.jsonInfo import JsonInfo
from core.jsonOpt import JsonOpt
from JoTools.utils.FileOperationUtil import FileOperationUtil
from core.ucDatasetOpt import UcDataset, UcDatasetOpt
from JoTools.utils.JsonUtil import JsonUtil


# ----------------------------------------------------------------------------------------------------------------------
label_list = ['Fnormal', 'fzc_broken']
conf = 1
mode = 'AND'
# ----------------------------------------------------------------------------------------------------------------------


uc_opt = UcDatasetOpt()
json_opt = JsonOpt()


uc_list = json_opt.query_uc_list_from_label(label_list, conf=1, mode='AND')

uc_opt.add_uc_dataset(uc_list=uc_list, dataset_name='fzc_test_dataset', model_name='fzc', model_version='v0.0.1')


# uc_dataset = uc_opt.get_uc_dataset(dataset_name='test_update_attr')
#
#
# for each_uc in uc_dataset:
#     each_json_path, each_img_path = opt.get_json_img_path_from_uc(each_uc)
#     json_info = JsonInfo(each_json_path)
#     print(json_info.extra_info)


# uc_list = opt.get_uc_list_by_label_from_root_buffer(need_label_list='fzc_gt')
#
# uc_opt.add_uc_dataset(uc_list=uc_list, dataset_name='fzc_gt_dataset', model_name='fzc', model_version='v4.7.9')
#
# fzc_gt_dataset = uc_opt.get_uc_dataset('fzc_gt_dataset')
#
# print(fzc_gt_dataset.get_info())
#
# fzc_gt_dataset.model_version = 'v0.2.3'
#
# uc_opt.update_uc_dataset(fzc_gt_dataset)
#
# fzc_gt_dataset = uc_opt.get_uc_dataset('fzc_gt_dataset')
#
# print(fzc_gt_dataset.get_info())
#

# uc_list = opt.get_uc_list_by_label_from_root_buffer(need_label_list=['fzc_broken'])
#
# uc_opt.add_uc_dataset(uc_list=uc_list, dataset_name="fzc_broken_train_data", model_name="fzc", model_version="v0.2.1")
#
# fzc_broken_dataset = uc_opt.get_uc_dataset(dataset_name="fzc_broken_train_data")
#
# print(fzc_broken_dataset.get_info())
#
#
#

# -*- coding: utf-8  -*-
# -*- author: jokker -*-


import os
import shutil
from core.jsonInfo import JsonInfo
from core.jsonOpt import Opt
from JoTools.utils.FileOperationUtil import FileOperationUtil
from core.ucDatasetOpt import UcDataset, UcDatasetOpt
from JoTools.utils.JsonUtil import JsonUtil

# fixme 给一个官方的方法，更新数据集和其对应的 uc_list ， 存在本地的一个地方

# fixme 保证 json 的唯一性，还需要计算 json 的 MD5 值专门放在一个地方用于记录, 如果 md5 一致，就不用更新


uc_opt = UcDatasetOpt()
opt = Opt()
opt.load_buffer()

uc_list = opt.get_uc_list_by_label_from_root_buffer(need_label_list='fzc_gt')

uc_opt.add_uc_dataset(uc_list=uc_list, dataset_name='fzc_gt_dataset', model_name='fzc', model_version='v4.7.9')

fzc_gt_dataset = uc_opt.get_uc_dataset('fzc_gt_dataset')

print(fzc_gt_dataset.get_info())

fzc_gt_dataset.model_version = 'v0.2.3'

uc_opt.update_uc_dataset(fzc_gt_dataset)

fzc_gt_dataset = uc_opt.get_uc_dataset('fzc_gt_dataset')

print(fzc_gt_dataset.get_info())


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

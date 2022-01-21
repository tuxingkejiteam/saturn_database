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

# uc_opt.get_uc_dataset_des_by_name()


# a = JsonUtil.load_data_from_json_file(r"C:\Users\14271\Desktop\fzc_test_data.json")
# print(a)
#
# exit()


uc_list = opt.get_uc_list_by_label_from_root_buffer(need_label_list=['Fnormal'])


# uc_opt.add_uc_dataset(uc_list=uc_list, dataset_name="fzc_test_data", model_name="fzc", model_version="v0.0.1")

# uc_opt.add_uc_dataset(uc_list=uc_list, dataset_name="fzc_test_data", model_name="fzc", model_version="v0.0.1")

fzc_dataset = uc_opt.get_uc_dataset("fzc_test_data")

print(fzc_dataset.get_info())

print('-'*20)

fzc_dataset.model_version = "v2.0.1"

uc_opt.update_uc_dataset(fzc_dataset)

fzc_dataset = uc_opt.get_uc_dataset("fzc_test_data")

print(fzc_dataset.get_info())








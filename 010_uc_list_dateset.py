# -*- coding: utf-8  -*-
# -*- author: jokker -*-


import os
import shutil
from core.jsonInfo import JsonInfo
from core.opt import Opt
from JoTools.utils.FileOperationUtil import FileOperationUtil

from .core.ucDatasetOpt import UcDataset, UcDatasetOpt


# fixme 给一个官方的方法，更新数据集和其对应的 uc_list ， 存在本地的一个地方

# fixme 保证 json 的唯一性，还需要计算 json 的 MD5 值专门放在一个地方用于记录, 如果 md5 一致，就不用更新


uc_opt = UcDatasetOpt()

uc_opt.get_uc_dataset_des_by_name()









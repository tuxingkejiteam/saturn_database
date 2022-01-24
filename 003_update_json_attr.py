# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import os
from core.jsonInfo import JsonInfo
from core.opt import Opt
from JoTools.utils.FileOperationUtil import FileOperationUtil


opt = Opt()

uc_list = opt.get_uc_list_by_label_from_root_buffer(need_label_list=['Fnormal'])


attr_list = [('extra_info','fzc test data')]
opt.update_json_attr(uc_list=uc_list, attr_list=attr_list)













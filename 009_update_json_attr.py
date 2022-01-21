# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import os
from core.jsonInfo import JsonInfo
from core.opt import Opt
from JoTools.utils.FileOperationUtil import FileOperationUtil


# todo 插入 json 数据的时候，如果 md5 对应的 uc 已存在，那么对 json 信息的更新符合下面的规则 (1) 更新 obj 信息，（2）属性信息只增不减 （3）想删除属性信息和增加某一些属性信息，只能通过 指定的函数来操作

# todo 输入 uc_list, [(输入需要改变的属性，输入属性修改后的值), (), ()]


opt = Opt()
opt.load_buffer()
# opt.update_buffer_objects('all')


# uc_list = opt.get_uc_list_by_label_from_root_buffer(need_label_list=['Fnormal', 'fzc_broken', 'fzc_yt', 'fzc_gt', 'zd_yt', 'qx_yt', 'zd_gt', 'zd_sm', 'fzc_sm', 'fs', 'qx_gt','qx_sm'])
uc_list = opt.get_uc_list_by_label_from_root_buffer(need_label_list=['Fnormal'])
print(uc_list, len(uc_list))


attr_list = [('extra_info','fzc test data')]
opt.update_json_attr(uc_list=uc_list, attr_list=attr_list)













# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import os
import shutil
from core.jsonInfo import JsonInfo
from core.jsonOpt import JsonOpt
from JoTools.utils.FileOperationUtil import FileOperationUtil


# fixme 验证结果

json_opt = JsonOpt()

# ----------------------------------------------------------------------------------------------------------------------
label_list = ['Fnormal', 'fzc_broken']
conf = 1
# mode = 'OR'
mode = 'AND'
# ----------------------------------------------------------------------------------------------------------------------


# AND 两个标签同时都含有
# OR 只需要有一个标签
uc_list = json_opt.query_uc_list_from_label(label_list, conf=conf, mode=mode)

print(uc_list)
print(len(uc_list))













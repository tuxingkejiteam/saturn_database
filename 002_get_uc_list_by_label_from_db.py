# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import os
import shutil
from core.jsonInfo import JsonInfo
from core.jsonOpt import JsonOpt
from JoTools.utils.FileOperationUtil import FileOperationUtil


json_opt = JsonOpt()
label_list = ['Fnormal']

uc_list = json_opt.query_uc_list_from_label(label_list, conf=1, mode='AND')

print(uc_list)














# -*- coding: utf-8  -*-
# -*- author: jokker -*-


import os
from core.jsonInfo import JsonInfo
from core.opt import Opt
from JoTools.utils.FileOperationUtil import FileOperationUtil


opt = Opt()
opt.load_buffer()


for each in opt.count_buffer_tags().items():
    print(each)





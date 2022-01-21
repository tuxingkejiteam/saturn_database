# -*- coding: utf-8  -*-
# -*- author: jokker -*-


import os
import time
import shutil
import configparser
from JoTools.utils.LogUtil import LogUtil
from JoTools.utils.JsonUtil import JsonUtil
this_dir = os.path.dirname(__file__)


# todo 写个日志装饰器，用于自动生成日志，或者写个日志函数，用于追踪每一步的操作，记录每一个操作的参数，日志有指定文件大小的功能最好能使用日志来做




class UcDataset(object):

    def __init__(self, uc_list, dataset_name, model_name=None, model_version=None, label_used=None, describe=""):
        self.uc_list = uc_list
        self.dataset_name = dataset_name
        #
        self.model_name = model_name
        self.model_version = model_version
        self.label_used = []  if label_used is None else label_used
        #
        self.set_time = time.time()
        self.update_time = time.time()
        # 描述信息
        self.describe = describe

    def __setattr__(self, key, value):
        """记录最后更新的时间"""
        object.__setattr__(self, key, value)
        if key == "uc_list":
            self.update_time = time.time()

    def get_info(self):
        """获取描述信息"""
        info = {
            "uc_list_length":"{0}".format(len(self.uc_list)),
            "model_name":"{0}".format(self.model_name),
            "model_version":"{0}".format(self.model_version),
            "label_used":"{0}".format(",".join(self.label_used)),
            "dataset_name":"{0}".format(self.dataset_name),
        }
        return info


class UcDatasetOpt(object):

    # todo 要有单独的日志，用于记录每一个 dataset 的设立，导入导出，时间 uc_list 变化等

    def __init__(self, config_path=None):
        self.root_dir = None            # 存储的文件夹
        #
        self.dataset_dir = None         # 用于存储数据集的地方
        self.log_dir = None             # 日志文件
        self.config_path = config_path
        #
        self.parse_config()

    def parse_config(self):
        """解析配置文件"""

        if self.config_path is None:
            config_path = os.path.join(this_dir, '..', 'config.ini')
            print(os.path.abspath(config_path))
            if os.path.exists(config_path):
                self.config_path = config_path
            else:
                raise ValueError("* config path not exist")

        cf = configparser.ConfigParser()
        cf.read(self.config_path, encoding='utf-8')
        self.root_dir = cf.get('common', 'root_dir')
        self.log_dir = os.path.join(self.root_dir, "log_dir")
        self.dataset_dir = os.path.join(self.root_dir, "uc_dataset")
        #
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(self.dataset_dir, exist_ok=True)

    def set_uc_dataset(self, uc_list, dataset_name) -> bool:
        """设置一个 uc_dataset 存储到本地"""
        pass

    def get_uc_dataset(self, dataset_name) -> list:
        pass

    def get_uc_dataset_by_name(self, dataset_name):
        pass

    def get_uc_dataset_by_label(self, label_last):
        pass

    def get_uc_dataset_des_by_name(self, dataset_name):
        pass

    def update_uc_dataset(self, uc_dataset):
        """根据 dataset_name 找到对应的"""
        # todo 增加日志记录
        pass




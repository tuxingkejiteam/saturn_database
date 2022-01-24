# -*- coding: utf-8  -*-
# -*- author: jokker -*-


import os
import time
import json
import shutil
import configparser
from JoTools.utils.LogUtil import LogUtil
from JoTools.utils.JsonUtil import JsonUtil
this_dir = os.path.dirname(__file__)



class UcDataset(object):

    def __init__(self, json_path=None, uc_list=None, dataset_name=None, model_name=None, model_version=None, label_used=None, describe=""):
        self.uc_list = uc_list
        self.dataset_name = dataset_name
        #
        self.model_name = model_name
        self.model_version = model_version
        self.label_used = []  if label_used is None else label_used
        #
        self.add_time = time.time()
        self.update_time = time.time()
        # 描述信息
        self.describe = describe
        self.json_path = json_path
        #
        self.parse_json_path()

    def __setattr__(self, key, value):
        """记录最后更新的时间"""
        object.__setattr__(self, key, value)
        if key == "uc_list":
            self.update_time = time.time()

    def __getitem__(self, index):
        """按照 index 取对应的对象"""
        return self.uc_list[index]

    def parse_json_path(self):
        """解析 json 信息"""
        if self.json_path is None:
            return

        if not os.path.exists(self.json_path):
            raise ValueError("json path is not exists")

        json_info = JsonUtil.load_data_from_json_file(self.json_path)
        self.uc_list = json_info['uc_list']
        self.dataset_name = json_info['dataset_name']
        self.model_name = json_info['model_name']
        self.model_version = json_info['model_version']
        self.label_used = json_info['label_used']
        self.add_time = json_info['add_time']
        self.update_time = json_info['update_time']
        self.describe = json_info['describe']

    def get_info(self):
        """获取描述信息"""
        info = {
            "uc_list_length":"{0}".format(len(self.uc_list)),
            "model_name":"{0}".format(self.model_name),
            "model_version":"{0}".format(self.model_version),
            "label_used":"{0}".format(",".join(self.label_used)),
            "dataset_name":"{0}".format(self.dataset_name),
            "add_time":"{0}".format(self.add_time),
            "update_time":"{0}".format(self.update_time),
        }
        return info

    def save_to_file(self, save_path):
        """保存为本地文件"""
        uc_dataset_info = {
            "uc_list": self.uc_list,
            "dataset_name": self.dataset_name,
            "model_name": self.model_name,
            "model_version": self.model_version,
            "label_used": self.label_used,
            "add_time": self.add_time,
            "update_time": self.update_time,
            "describe": self.describe,
        }
        JsonUtil.save_data_to_json_file(uc_dataset_info, save_path)


class UcDatasetOpt(object):

    # todo 要有单独的日志，用于记录每一个 dataset 的设立，导入导出，时间 uc_list 变化等

    def __init__(self, config_path=None):
        self.root_dir = None                    # 存储的文件夹
        #
        self.dataset_dir = None                 # 用于存储数据集的地方
        self.log_dir = None                     # 日志文件
        self.log = None
        self.config_path = config_path
        #
        self.parse_config()

    def parse_config(self):
        """解析配置文件"""

        if self.config_path is None:
            config_path = os.path.join(this_dir, '..\..', 'config.ini')
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
        self.log = LogUtil.get_log(os.path.join(self.log_dir, "uc_dataset_opt.log"), 4, "uc dataset opt", print_to_console=False)
        #
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(self.dataset_dir, exist_ok=True)

    def add_uc_dataset(self, uc_list, dataset_name, model_name=None, model_version=None, label_used=None, describe="") -> bool:
        """设置一个 uc_dataset 存储到本地"""
        self.log.info("add uc dataset : {0}".format(dataset_name))
        # 如果同样的名字已存在，那么就不能插入只能进行更新
        json_save_path = self._get_uc_dataset_path_by_dataset_name(dataset_name)
        if os.path.exists(json_save_path):
            raise ValueError("{0} is exists".format(dataset_name))
        #
        a = UcDataset(uc_list=uc_list, dataset_name=dataset_name, model_name=model_name, model_version=model_version, label_used=label_used, describe=describe)
        # 保存为本地文件
        if not self.check_dataset_name(dataset_name):
            raise ValueError(" dataset name error : {0}".format(dataset_name))
        # todo 对dataset_name 进行格式检查
        a.save_to_file(json_save_path)

    def get_uc_dataset(self, dataset_name):
        self.log.info("get uc dataset : {0}".format(dataset_name))
        json_path = self._get_uc_dataset_path_by_dataset_name(dataset_name)
        if os.path.exists(json_path):
            a = UcDataset(json_path=json_path)
            return a
        else:
            self.log.info("dataset not exists")
            raise ValueError('dataset not exists')

    def _get_uc_dataset_path_by_dataset_name(self, dataset_name):
        return os.path.join(self.dataset_dir, "{0}.json".format(dataset_name))

    def update_uc_dataset(self, uc_dataset):
        """根据 dataset_name 找到对应的"""
        if not isinstance(uc_dataset, UcDataset):
            raise TypeError("need UcDataset")
        uc_dataset_name = uc_dataset.dataset_name
        self.log.info("update uc dataset : {0}".format(uc_dataset_name))
        uc_dataset.update_time = time.time()
        json_path = self._get_uc_dataset_path_by_dataset_name(uc_dataset_name)
        if not os.path.exists(json_path):
            raise ValueError("no dataset with name {0} can not update, try insert".format(uc_dataset_name))
        uc_dataset.save_to_file(json_path)

    @staticmethod
    def check_dataset_name(dataset_name):
        """检查dataset的名字，确保能作为文件存储"""
        return True



# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import os
import cv2
import shutil
import random
import configparser
import numpy as np
from .jsonInfo import JsonInfo
from JoTools.utils.FileOperationUtil import FileOperationUtil

# todo 导入数据库操作函数
class DataBaseOpt():

    @staticmethod
    def add_json(json_path):
        pass

    @staticmethod
    def del_json(json_path):
        pass

    @staticmethod
    def update_json(json_path):
        pass

    @staticmethod
    def get_uc(md5):
        pass


class Opt(object):

    def __init__(self, config_path=None):
        self.config_path = config_path
        self.root_dir = None
        self.sql_path = None
        self.json_dir = None
        self.img_dir = None
        self.tmp_dir = None
        #
        self.parse_config()

    def parse_config(self):
        """解析配置参数"""

        if self.config_path is None:
            config_path = r"../config.ini"
            if os.path.exists(config_path):
                self.config_path = config_path
            else:
                raise ValueError("* config path not exist")

        cf = configparser.ConfigParser()
        cf.read(self.config_path)
        self.sql_path = cf.get('common', 'sql_path')
        self.root_dir = cf.get('common', 'root_dir')
        self.tmp_dir = cf.get('common', 'tmp_dir')
        #
        self.json_dir = self.img_dir = os.path.join(self.root_dir, "json_img")

        print('-' * 30)
        print("* sql path : {0}".format(self.sql_path))
        print("* root dir : {0}".format(self.root_dir))
        print("* json dir : {0}".format(self.json_dir))
        print("* img dir : {0}".format(self.img_dir))
        print("* tmp dir : {0}".format(self.tmp_dir))
        print('-'*30)

    @staticmethod
    def add_json_to_db(json_path):
        pass

    @staticmethod
    def update_json_to_db(json_path):
        pass

    @staticmethod
    def del_json_from_db(json_path):
        pass

    @staticmethod
    def get_uc(img_md5):
        pass

    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _check_json_img_consistence(json_path, img_path):
        uc_1 = FileOperationUtil.bang_path(json_path)[1]
        uc_2 = FileOperationUtil.bang_path(img_path)[1]
        if os.path.exists(json_path) and os.path.exists(img_path):
            if uc_1 == uc_2:
                return True
        return False

    def add_uc_to_root(self, json_path, img_path, is_clip=False):
        """将 json 存放到 root 目录中去"""
        if not self._check_json_img_consistence(json_path, img_path):
            raise ValueError("* json img uc not equal")

        uc = FileOperationUtil.bang_path(json_path)[1]
        json_path_dst, img_path_dst = self.get_json_img_path_from_uc(uc)
        #
        json_dir = os.path.split(json_path_dst)[0]
        img_dir = os.path.split(img_path_dst)[0]
        os.makedirs(json_dir, exist_ok=True)
        os.makedirs(img_dir, exist_ok=True)
        #
        if is_clip:
            shutil.move(json_path, json_path_dst)
            shutil.move(img_path, img_path_dst)
        else:
            shutil.copy(json_path, json_path_dst)
            shutil.copy(img_path, img_path_dst)

        print("* add {0} [xml,img] to root".format(uc))

    def del_uc_from_root(self, json_path, img_path):
        pass

    def update_uc_from_root(self, json_path, img_path):

        # todo del_uc_from_root
        # todo add_uc_to_root

        pass

    # ------------------------------------------------------------------------------------------------------------------

    def get_json_img_path_from_uc(self, uc):
        """输入 uc 号，返回对应的 img 和 json 路径, 可用于存储和读取"""
        json_path = os.path.join(self.json_dir, uc[:3], "{0}.json".format(uc))
        img_path = os.path.join(self.json_dir, uc[:3], "{0}.jpg".format(uc))
        return (json_path, img_path)

    def uc_in_root(self, uc):
        """uc 是不是存在于缓存空间"""
        json_path, img_path = self.get_json_img_path_from_uc(uc)
        if os.path.exists(json_path) or os.path.exists(img_path):
            return True
        else:
            return False
    # ------------------------------------------------------------------------------------------------------------------

    def get_json_from_xml(self, xml_path, img_path):
        """输入一个 xml img 得到 json 文件"""
        # todo 申请 uc
        uc = str(random.randrange(1, 50000)).rjust(7, '0')
        # 解析 xml
        a = JsonInfo()
        a.parse_xml(xml_path=xml_path, img_path=img_path, uc=uc)
        a.unique_code = uc
        #
        json_path = os.path.join(self.tmp_dir, "{0}.json".format(uc))
        save_img_path = os.path.join(self.tmp_dir, "{0}.jpg".format(uc))
        a.save_to_json(json_path)
        # 将 img 重命名之后
        img_ndarry = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), 1)
        cv2.imwrite(save_img_path, img_ndarry)
        return json_path, save_img_path

    @staticmethod
    def get_json_from_labelme_json(self, json_path, save_path):
        pass

    @staticmethod
    def get_json_from_img(self, save_path):
        pass


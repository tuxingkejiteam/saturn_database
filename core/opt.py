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
from db_tools.CRUD.MySQL_class import SaturnSQL
from JoTools.utils.HashlibUtil import HashLibUtil
from JoTools.utils.DecoratorUtil import DecoratorUtil
from JoTools.utils.PickleUtil import PickleUtil
this_dir = os.path.dirname(__file__)

# fixme 为了增加速度，可以使用缓存模式，就是除非是强制进行更新并筛选，否者，只在已缓存的部分内容中进行删选


class Opt(object):

    def __init__(self, config_path=None):
        self.config_path = config_path
        self.root_dir = None
        self.sql_path = None
        self.json_dir = None
        self.img_dir = None
        self.tmp_dir = None
        #
        self.sql_zy = None
        # 缓存的数据
        self.object_buffer_dir = None
        self.parse_config()
        self._json_info_dict = {}

    def parse_config(self):
        """解析配置参数"""

        if self.config_path is None:
            # config_path = r"./config.ini"
            config_path = os.path.join(this_dir, '..', 'config.ini')
            print(os.path.abspath(config_path))
            if os.path.exists(config_path):
                self.config_path = config_path
            else:
                raise ValueError("* config path not exist")

        cf = configparser.ConfigParser()
        cf.read(self.config_path, encoding='utf-8')
        self.sql_path = cf.get('common', 'sql_path')
        self.root_dir = cf.get('common', 'root_dir')
        self.tmp_dir = cf.get('common', 'tmp_dir')
        #
        self.json_dir = self.img_dir = os.path.join(self.root_dir, "json_img")
        self.object_buffer_dir = os.path.join(self.root_dir, 'buffer')
        os.makedirs(self.json_dir, exist_ok=True)
        os.makedirs(self.img_dir, exist_ok=True)
        os.makedirs(self.object_buffer_dir, exist_ok=True)
        #
        host = cf.get('sql', 'host')
        user = cf.get('sql', 'user')
        password = cf.get('sql', 'password')
        db_name = cf.get('sql', 'db_name')
        self.sql_zy = SaturnSQL(host=host, user=user, password=password, db_name=db_name)
        #
        print('-' * 30)
        print("* sql path : {0}".format(self.sql_path))
        print("* root dir : {0}".format(self.root_dir))
        print("* json dir : {0}".format(self.json_dir))
        print("* img dir : {0}".format(self.img_dir))
        print("* tmp dir : {0}".format(self.tmp_dir))
        print("* object_buffer_dir dir : {0}".format(self.object_buffer_dir))
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

    def update_json_attr(self, uc_list, attr_list):
        """更新 json 的信息 [[attr_name, attr_value]]"""
        json_list = []
        for each_uc in uc_list:
            each_json_path = self.get_json_img_path_from_uc(each_uc)[0]
            each_json_info = JsonInfo(each_json_path)
            for attr_name, attr_value in attr_list:
                setattr(each_json_info, attr_name, attr_value)
                json_list.append(each_json_path)

        # 将 json 信息全部导入到数据库中
        self.sql_zy.update_json_list_to_db(json_list)

    # ------------------------------------------------------------------------------------------------------------------

    def get_all_uc_list_from_root(self):
        """查询本地存储的 json 的 uc 名列表"""
        pass

    def get_all_uc_list_from_db(self):
        """查询已记录的 uc 名列表，或者 已分类的 uc 名列表"""
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
        if os.path.exists(json_path) and os.path.exists(img_path):
            return True
        else:
            return False
    # ------------------------------------------------------------------------------------------------------------------

    @DecoratorUtil.time_this
    def get_json_from_xml(self, xml_path, img_path):
        """输入一个 xml img 得到 json 文件"""
        # 申请 uc
        each_hash = HashLibUtil.get_file_md5(img_path)
        uc = self.sql_zy.get_uc_list([each_hash])[0]
        # 解析 xml
        a = JsonInfo()
        a.parse_xml(xml_path=xml_path, img_path=img_path, uc=uc)
        a.unique_code = uc
        a.MD5 = each_hash
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

    # ------------------------------------------------ find ------------------------------------------------------------

    def get_uc_list_by_attr_from_root(self, func, data):
        """从本地查询内容"""
        uc_list = []
        for index, each_json_path in enumerate(FileOperationUtil.re_all_file(self.json_dir, endswitch=['.json'])):
            print(index, each_json_path)
            each_json = JsonInfo(each_json_path)
            if func(each_json, data):
                uc_list.append(each_json.unique_code)
        return uc_list

    @DecoratorUtil.time_this
    def get_uc_list_by_label_from_root(self, need_label_list):
        """根据标签进行筛选"""
        uc_list = []
        for index, each_json_path in enumerate(FileOperationUtil.re_all_file(self.json_dir, endswitch=['.json'])):
            print(index, each_json_path)
            each_json = JsonInfo(each_json_path)
            if each_json.has_label(need_label_list):
                uc_list.append(each_json.unique_code)
        return uc_list

    @DecoratorUtil.time_this
    def get_uc_list_by_label_from_root_buffer(self, need_label_list):
        """根据标签进行筛选"""
        uc_list = []

        for each_uc_date in self._json_info_dict:
            for each_uc in self._json_info_dict[each_uc_date]:
                each_json = self._json_info_dict[each_uc_date][each_uc]
                if each_json.has_label(need_label_list):
                    uc_list.append(each_json.unique_code)
        return uc_list
    # ------------------------------------------------ stastic ---------------------------------------------------------

    @DecoratorUtil.time_this
    def count_tags(self):
        """统计标签"""
        count = {}
        for index, each_json_path in enumerate(FileOperationUtil.re_all_file(self.json_dir, endswitch=['.json'])):
            print(index, each_json_path)
            each_json = JsonInfo(each_json_path)
            each_count = each_json.count_tags()
            # 统计结果进行合并
            for each_type in each_count:
                if each_type not in count:
                    count[each_type] = each_count[each_type]
                else:
                    for each_label in each_count[each_type]:
                        if each_label not in count[each_type]:
                            count[each_type][each_label] = each_count[each_type][each_label]
                        else:
                            count[each_type][each_label] += each_count[each_type][each_label]
        return count

    @DecoratorUtil.time_this
    def count_buffer_tags(self):
        """统计缓冲区中的标签"""
        count = {}
        for each_uc_date in self._json_info_dict:
            for each_uc in self._json_info_dict[each_uc_date]:
                each_json = self._json_info_dict[each_uc_date][each_uc]
                each_count = each_json.count_tags()
                # 统计结果进行合并
                for each_type in each_count:
                    if each_type not in count:
                        count[each_type] = each_count[each_type]
                    else:
                        for each_label in each_count[each_type]:
                            if each_label not in count[each_type]:
                                count[each_type][each_label] = each_count[each_type][each_label]
                            else:
                                count[each_type][each_label] += each_count[each_type][each_label]
        return count

    # ------------------------------------------------ dataset ---------------------------------------------------------

    def get_xml_dataset_by_uc_list(self, uc_list, save_dir):
        """根据传入的 uc list 拷贝出数据"""
        for each_uc in uc_list:
            json_path, img_path = self.get_json_img_path_from_uc(each_uc)
            # 读取 json_path, 转为 xml
            save_xml_path = os.path.join(save_dir, FileOperationUtil.bang_path(json_path)[1] + '.xml')
            save_img_path = os.path.join(save_dir, FileOperationUtil.bang_path(json_path)[1] + '.jpg')
            json_info = JsonInfo(json_path)
            shutil.copy(img_path, save_img_path)
            json_info.save_to_xml(save_xml_path)

    def get_json_dataset_by_uc_list(self, uc_list, save_dir):
        """根据传入的 uc list 拷贝出数据"""
        pass

    def get_coco_dataset_by_uc_list(self, uc_list, save_dir):
        """根据传入的 uc list 拷贝出数据"""
        pass

    def get_voc_dataset_by_uc_list(self, uc_list, save_dir):
        """根据传入的 uc list 拷贝出数据"""
        pass

    # ------------------------------------------------ tmp_data --------------------------------------------------------

    def update_buffer_objects(self, mode='new'):
        """更新缓存数据，两种模式 new:只读取新的数据，all:所有的数据全部重新读取"""

        # uc 日期一致的话存在同一个 pkl 中

        # 读取历史 pkl
        print("* read history buffer")
        for each_pkl_path in FileOperationUtil.re_all_file(self.object_buffer_dir, endswitch=['.pkl']):
            each_json_info_dict = PickleUtil.load_data_from_pickle_file(each_pkl_path)
            uc_date = FileOperationUtil.bang_path(each_pkl_path)[1][:3]
            self._json_info_dict[uc_date] = each_json_info_dict

        # 更新最新的 json
        print("* pase new json")
        for each_json_path in FileOperationUtil.re_all_file(self.json_dir, endswitch=['.json']):
            uc = FileOperationUtil.bang_path(each_json_path)[1]
            uc_date = uc[:3]
            if (uc not in self._json_info_dict[uc_date]) or (mode == 'all'):
                each_json_info = JsonInfo(each_json_path)
                if uc_date in self._json_info_dict:
                    self._json_info_dict[uc_date][uc] = each_json_info
                else:
                    self._json_info_dict[uc_date] = {uc:each_json_info}

        # 存储 pkl 到缓存中去
        print("* save objects to pkl")
        for each_uc_date in self._json_info_dict:
            each_pkl_path = os.path.join(self.object_buffer_dir, "{0}.pkl".format(each_uc_date))
            PickleUtil.save_data_to_pickle_file(self._json_info_dict[each_uc_date], each_pkl_path)

    def load_buffer(self):
        # 读取历史 pkl
        print("* read history buffer")
        for each_pkl_path in FileOperationUtil.re_all_file(self.object_buffer_dir, endswitch=['.pkl']):
            each_json_info_dict = PickleUtil.load_data_from_pickle_file(each_pkl_path)
            uc_date = FileOperationUtil.bang_path(each_pkl_path)[1][:3]
            self._json_info_dict[uc_date] = each_json_info_dict










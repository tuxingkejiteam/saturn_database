# -*- coding: utf-8  -*-
# -*- author: jokker -*-


import json
from JoTools.utils.JsonUtil import JsonUtil



class JsonInfo(object):

    def __init__(self, json_path=None):
        self.org_name = None
        self.unique_code = None
        self.size = None
        self.H = None
        self.W = None
        self.MD5 = None
        self.trace = None
        self.objects = None
        self.mode = None                # 输配变模式, 输电，配电还是变点
        self.train_info = None
        self.extra_info = None
        self.objects_num = None
        self.json_path = json_path
        #
        self.parse_json(json_path)

    def __getitem__(self, item):
        if item > self.objects_num:
            print('目标索引越界！')
            return None
        dix = str(item)
        return self.objects[dix]

    def __len__(self):
        return self.objects_num

    def __str__(self):
        return self.unique_code + ' ' + self.org_name

    def __iter__(self):
        return self.objects.items()

    def __add__(self, other):
        """两个要素相加"""
        if not hasattr(other, "MD5"):
            raise ValueError("* dont has attr MD5")

        if not other.MD5 == self.MD5:
            raise ValueError("* MD5 must be equal")

        for each_obj in other.objects:
            # todo 判断元素是否已存在
            # todo 要增加的要素需要进行处理，点，线，面
            self.objects.append(each_obj)

    # ------------------------------------------------------------------------------------------------------------------

    def parse_json(self, json_path):
        """从json文件中获取图像信息"""

        if json_path is None:
            return

        with open(json_path, 'r') as load_f:
            json_dic = json.load(load_f)

        self.org_name = json_dic['org_name']
        self.unique_code = json_dic['unique_code']
        self.size = json_dic['size']
        self.H = self.size['height']
        self.W = self.size['width']
        self.MD5 = json_dic['MD5']
        self.trace = bool(json_dic['trace'])
        self.objects = json_dic['objects']
        self.mode = json_dic['mode']                            # 输配变模式
        self.train_info = json_dic['train_info']
        self.extra_info = json_dic['extra_info']
        self.objects_num = len(self.objects)

    def parse_xml(self, xml_path, img_path=None):
        pass

    def parse_labelme_json(self, json_path, img_path):
        pass

    # ------------------------------------------------------------------------------------------------------------------

    def save_to_json(self, sabe_path):
        """转为存入数据库的 json 样式"""
        jsontext = {}
        jsontext['org_name']        = self.org_name
        jsontext['unique_code']     = self.unique_code
        jsontext['size']            = {'width': self.W, 'height': self.H}
        jsontext["train_info"]      = self.train_info
        jsontext["trace"]           = self.trace
        jsontext['MD5']             = self.MD5
        jsontext["extra_info"]      = self.extra_info
        jsontext["mode"]            = self.mode
        jsontext['objects']         = self.objects
        #
        JsonUtil.save_data_to_json_file(jsontext, sabe_path)

    def save_to_json_label_me(self):
        """生成labelme软件可以识别的json格式"""
        pass

    def save_to_coco(self):
        """生成coco数据集对应的样式"""
        pass

    def save_to_voc(self):
        """保存为voc数据集对应的样式"""
        pass

    def save_to_xml(self):
        """转为我们现在 xml 的样式"""
        pass

    # ------------------------------------------------------------------------------------------------------------------









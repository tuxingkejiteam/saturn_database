# -*- coding: utf-8  -*-
# -*- author: jokker -*-


import json


class ImgLabel(object):

    def __init__(self, json_path):
        self.org_name = None
        self.unique_code = None
        self.size = None
        self.H = None
        self.W = None
        self.class_code = None
        self.MD5 = None
        self.trace = None
        self.objects = None
        self.train_info = None
        self.extra_info = None
        self.objects_num = None
        self.json_data=None
        #
        self.parse_json_info(json_path)

    def __getitem__(self, item):
        if item > self.objects_num:
            print('目标索引越界！')
            return None
        dix = str(item)
        return self.objects[dix]

    def __len__(self):  # 使得len可作用于实例化的类上，返回的是标注含有多少个目标
        return self.objects_num

    def __str__(self):  # 若打印此类，则会输出图片的编码和原名。
        return self.unique_code + ' ' + self.org_name

    def __iter__(self):
        return self.objects.items()  # 返回一个可迭代对象。

    def __add__(self, other):
        """两个要素相加"""
        if not hasattr(other, "MD5"):
            raise ValueError("* dont has attr MD5")

        if not other.MD5 == self.MD5:
            raise ValueError("* MD5 must be equal")

        # todo 判断元素是否已存在

        # todo 要增加的要素需要进行处理，点，线，面


    # ------------------------------------------------------------------------------------------------------------------

    def parse_json_info(self, json_path):
        """从json文件中获取图像信息"""

        # fixme 这边输入的 json 必须符合一定的样式，使用 GetJson 从其他样式的数据中获取

        with open(json_path, 'r') as load_f:
            json_dic = json.load(load_f)
        self.org_name = json_dic['org_name']
        self.unique_code = json_dic['unique_code']
        self.size = json_dic['size']
        self.H = self.size['height']
        self.W = self.size['width']
        self.class_code = json_dic['class_code']
        self.MD5 = json_dic['MD5']
        self.trace = bool(json_dic['trace'])
        self.objects = json_dic['objects']
        self.train_info = json_dic['train_info']
        self.extra_info = json_dic['extra_info']
        self.objects_num = len(self.objects)
        self.json_data=json_dic

    # ------------------------------------------------------------------------------------------------------------------

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



class GetJson(object):

    def get_json_from_xml(self):
        pass

    def get_json_from_json_label_me(self):
        pass









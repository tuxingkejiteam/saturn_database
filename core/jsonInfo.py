# -*- coding: utf-8  -*-
# -*- author: jokker -*-


import json
from JoTools.utils.JsonUtil import JsonUtil
from JoTools.txkjRes.deteRes import DeteRes, DeteObj, DeteAngleObj
from JoTools.utils.HashlibUtil import HashLibUtil

class Object(object):

    def __init__(self):
        self.label = None
        self.shape_type = None
        self.points = None

    def __eq__(self, other):
        if self.label != other.label:
            return False

        if len(self.points) != len(other.label):
            return False

        for index in range(self.points):
            if self.points[index] != other.points[index]:
                return False
        return True


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

    def __contains__(self, item):
        for each_obj in self.objects:
            if item == each_obj:
                return True
        return False

    def __add__(self, other):
        """两个要素相加"""
        if not hasattr(other, "MD5"):
            raise ValueError("* dont has attr MD5")

        if not other.MD5 == self.MD5:
            raise ValueError("* MD5 must be equal")

        for each_obj in other.objects:
            # 判断元素是否已存在
            if each_obj not in self:
                self.objects.append(each_obj)
            else:
                print("* 存在重复元素，需要进行处理")

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

    def parse_xml(self, xml_path, uc, img_path):

        a = DeteRes(xml_path)
        a.img_path = img_path

        self.org_name = a.file_name
        self.unique_code = uc
        self.H = a.height
        self.W = a.width
        if self.MD5 is None:
            self.MD5 = HashLibUtil.get_file_md5(img_path)
        #
        self.objects = []
        for each_dete_obj in a:
            obj = Object()
            if isinstance(each_dete_obj, DeteObj):
                obj.label = each_dete_obj.tag
                obj.shape_type = 'rectangle'
                obj.points = [[each_dete_obj.x1, each_dete_obj.y1], [each_dete_obj.x2, each_dete_obj.y2]]
            elif isinstance(each_dete_obj, DeteAngleObj):
                obj.label = each_dete_obj.tag
                obj.shape_type = 'robndbox'
                obj.points = each_dete_obj.get_points()
            else:
                raise ValueError("* just support DeteObj or DeteAngleObj")
            self.objects.append(obj)

    def parse_labelme_json(self, json_path, img_path):
        pass

    # ------------------------------------------------------------------------------------------------------------------

    def save_to_json(self, save_path):
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
        # fixme 这边要处理一下，存放的对象要转为字典形式
        # jsontext['objects']         = self.objects
        #
        jsontext['objects'] = []
        for each_obj in self.objects:
            jsontext['objects'].append({
                'label':each_obj.label,
                'shape_type':each_obj.shape_type,
                'points':each_obj.points,
            })
        JsonUtil.save_data_to_json_file(jsontext, save_path)

    def save_to_json_label_me(self):
        """生成labelme软件可以识别的json格式"""
        pass

    def save_to_coco(self):
        """生成coco数据集对应的样式"""
        pass

    def save_to_voc(self):
        """保存为voc数据集对应的样式"""
        pass

    def save_to_xml(self, xml_path):
        """转为我们现在 xml 的样式"""
        pass

    # ------------------------------------------------------------------------------------------------------------------









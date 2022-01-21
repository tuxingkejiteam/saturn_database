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
        self.id = None                  # 用于给每一个元素

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
        self.objects = []
        self.mode = None                # 输配变模式, 输电，配电还是变点
        self.train_info = None
        self.extra_info = None
        self.json_path = json_path
        #
        self.parse_json(json_path)

    def __str__(self):
        return self.unique_code

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
        self.H = json_dic['size']['height']
        self.W = json_dic['size']['width']
        self.MD5 = json_dic['MD5']
        self.trace = bool(json_dic['trace'])
        self.mode = json_dic['mode']                            # 输配变模式
        self.train_info = json_dic['train_info']
        self.extra_info = json_dic['extra_info']

        for each_obj_dict in json_dic['objects']:
            obj = Object()
            if each_obj_dict['shape_type'] == 'rectangle':
                obj.label = each_obj_dict['label']
                obj.shape_type = 'rectangle'
                obj.id = each_obj_dict['id']
                obj.points = each_obj_dict['points']
                self.objects.append(obj)
            elif each_obj_dict['shape_type'] == 'robndbox':
                obj.label = each_obj_dict['label']
                obj.shape_type = 'robndbox'
                obj.id = each_obj_dict['id']
                obj.points = each_obj_dict['points']
                self.objects.append(obj)

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
        #
        for each_dete_obj in a:
            obj = Object()
            if isinstance(each_dete_obj, DeteObj):
                obj.label = each_dete_obj.tag
                obj.shape_type = 'rectangle'
                obj.id = each_dete_obj.id

                # if obj.id in [None, -1]:
                #     raise ValueError("* obj.id should not be in [None, -1]")

                obj.points = [[each_dete_obj.x1, each_dete_obj.y1], [each_dete_obj.x2, each_dete_obj.y2]]
            elif isinstance(each_dete_obj, DeteAngleObj):
                obj.label = each_dete_obj.tag
                obj.shape_type = 'robndbox'
                # obj.points = each_dete_obj.get_points()
                obj.points = [each_dete_obj.cx, each_dete_obj.cy, each_dete_obj.w, each_dete_obj.h, each_dete_obj.angle]
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
                'id':each_obj.id,
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

    def save_to_xml(self, xml_path, img_path=None):
        """转为我们现在 xml 的样式"""
        a = DeteRes()
        a.img_path = img_path
        #
        if img_path is None:
            a.file_name = self.unique_code + ".jpg"
            a.height = self.H
            a.width = self.W
        #
        for each_obj in self.objects:
            if each_obj.shape_type == 'rectangle':
                each_dete_obj = DeteObj()
                each_dete_obj.tag = each_obj.label
                each_dete_obj.x1, each_dete_obj.y1 = each_obj.points[0]
                each_dete_obj.x2, each_dete_obj.y2 = each_obj.points[1]
                each_dete_obj.id = each_obj.id
                a.add_obj_2(each_dete_obj)
            elif each_obj.shape_type == 'robndbox':
                each_dete_obj = DeteAngleObj()
                each_dete_obj.tag = each_obj.label
                each_dete_obj.cx = each_obj.points[0]
                each_dete_obj.cy = each_obj.points[1]
                each_dete_obj.w = each_obj.points[2]
                each_dete_obj.h = each_obj.points[3]
                each_dete_obj.angle = each_obj.points[4]
                a.add_obj_2(each_dete_obj)
            else:
                print("* {0} 类型暂时无法转为 xml ".format(each_obj.shape_type))
                pass
        a.save_to_xml(xml_path)

    # ------------------------------------------------------------------------------------------------------------------

    def count_tags(self):
        """分类型统计标签"""
        count = {}
        for each_obj in self.objects:
            if each_obj.shape_type not in count:
                count[each_obj.shape_type] = {}
            if each_obj.label not in count[each_obj.shape_type]:
                count[each_obj.shape_type][each_obj.label] = 1
            else:
                count[each_obj.shape_type][each_obj.label] += 1
        return count

    def has_label(self, label_list):
        """是否含有某个 label"""

        if isinstance(label_list, str):
            label_list = [label_list]

        for each_obj in self.objects:
            if each_obj.label in label_list:
                return True
        return False








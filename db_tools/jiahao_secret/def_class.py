import json


class ImgLabel:
    def __init__(self, json_path):
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

    #def __add__(self,other):  这个特殊方法，可以定义类的加法.
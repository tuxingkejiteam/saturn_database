import json
from pathlib import Path


# 图片标注信息的大类，一口气将json文件中的信息全部读取出来。
class LabelInfo:
    def __init__(self, json_path):  # 初始化
        with open(json_path, 'r') as load_f:
            self.json_dic = json.load(load_f)
        self.org_name = self.json_dic['org_name']
        self.unique_code = self.json_dic['unique_code']
        self.size = self.json_dic['size']
        self.H = self.size['height']
        self.W = self.size['width']
        self.class_code = self.json_dic['class_code']
        self.MD5 = self.json_dic['MD5']
        self.trace = bool(self.json_dic['trace'])
        self.visible = bool(self.json_dic['visible'])
        self.objects = self.json_dic['objects']
        self.train_info = self.json_dic['train_info']
        self.extra_info = self.json_dic['extra_info']
        self.hanming = self.json_dic['hanming']
        self.objects_num = len(self.objects)
        self.path = Path(json_path)

    def __getitem__(self, item):  # 访问json中标注的物体
        if item > self.objects_num:  # 若下标越界则打印出错误信息，并返回None，但并不会触发程序报错。
            print('目标索引越界！')
            return None
        dix = str(item)
        return self.objects[dix]

    def __len__(self):  # 使得len可作用于实例化的类上，返回的是标注含有多少个目标
        return self.objects_num

    def __str__(self):  # 若打印此类，则会输出图片的编码。
        return self.unique_code



    # todo 需要增加最基础的属性操作等，这样会在后面方便很多






















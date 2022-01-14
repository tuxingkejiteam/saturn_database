import datetime
import pymysql as sql
import os
import json
import sys


# 字母数值对照表
comparison_tabel = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'a', 11: 'b',
                    12: 'c', 13: 'd', 14: 'e', 15: 'f', 16: 'g', 17: 'h', 18: 'j', 19: 'k', 20: 'l', 21: 'm',
                    22: 'n', 23: 'p', 24: 'q', 25: 'r', 26: 's', 27: 't', 28: 'u', 29: 'v', 30: 'w', 31: 'x',
                    32: 'y', 33: 'z'}
year_dict = {2019: 'A', 2020: 'B', 2021: 'C', 2022: 'D', 2023: 'E', 2024: 'F', 2025: 'G'}


def first_3_letters() -> str:
    date = datetime.datetime.now()
    year = date.year
    month = date.month
    day = date.day
    letter_1 = year_dict[year]

    if day <= 15:
        letter_2 = comparison_tabel[month + 9]  # 上半月，月份从a开始
        letter_3 = comparison_tabel[day + 9]
    else:
        letter_2 = comparison_tabel[month + 9 + 12]  # 下半月，月份从m开始
        letter_3 = comparison_tabel[day - 15 + 9]

    return letter_1 + letter_2 + letter_3


def coding_rank(serial_number) -> str:
    # 将不多于4万6的需要，编码至三位。每位有36种选择。
    # 方法：整除取余法
    assert serial_number <= 1679616, "编码溢出"
    remainder_1 = serial_number % 34  # 取余数
    quotient_1 = serial_number // 34

    remainder_2 = quotient_1 % 34  # 取余数
    quotient_2 = quotient_1 // 34

    remainder_3 = quotient_2 % 34  # 取余数
    assert quotient_2 // 34 == 0, '编码溢出'
    letter_4 = comparison_tabel[remainder_3]
    letter_5 = comparison_tabel[remainder_2]
    letter_6 = comparison_tabel[remainder_1]

    return letter_4 + letter_5 + letter_6


def binary2ten(number_2_str) -> str:
    if number_2_str == '000000000000000':
        return 'unlabeled'
    number_10 = int(number_2_str, 2)
    if number_10 > 32767 or len(number_2_str) != 15:
        return 'xxxxx'  # 标注错误
    else:
        add_zeros = ''
        number_10_str = str(number_10)
        for i in range(5 - len(number_10_str)):
            add_zeros += '0'
        return add_zeros + number_10_str


def get_json_path(UC) -> str:
    json_path = 'output_json/' + UC + '.json'
    return json_path


def subclass():
    pass


def get_small_img(UC_list: list, label_list: list, save_dir: str) -> None:
    # 保存小图数据集
    # 入参：唯一编码列表，标签列表，保存路径
    # 出参：无

    for label in label_list:  # 有几个标签，就在保存路径下，创建几个文件夹。
        dataset_path = os.path.join(save_dir, label)
        if os.path.exists(dataset_path):
            print('输出目录已存在，操作已终止。')
            sys.exit(-2)
        else:
            os.mkdir(dataset_path)
    print('{}个类别目录已被创建。'.format(len(label_list)))
    i = 0
    # 遍历唯一编码列表。
    for UC in UC_list:
        json_path = get_json_path(UC)
        with open(json_path) as f:
            json_dic = json.load(f)
        objects_dic = json_dic['objects']
        for item_key in objects_dic:  # 遍历json中所有物体
            item = objects_dic[item_key]
            if item['label'] in label_list:
                assert item['shape_type'] == 'bndbox', '标注方式错误，请检查标签。'
                points = item['points']
                i += 1
                save_name = UC + '_' + str(i) + '_' + item['label'] + '_[' + points['xmin'] + ',' + points[
                    'ymax'] + ',' + points['xmax'] + ',' + points['ymin'] + '.jpg'  # 拼接小图的保存名称。
                class_dir = os.path.join(save_dir, item['label'])  # 获取小类别目录。
                save_path = os.path.join(class_dir, save_name)  # 拼接小图的保存路径。

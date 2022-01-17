# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
* uiique code 简称 UC

* UC 的具体说明

"""

import os
import shutil
import datetime
from JoTools.utils.JsonUtil import JsonUtil

comparison_tabel = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'a', 11: 'b',
                    12: 'c', 13: 'd', 14: 'e', 15: 'f', 16: 'g', 17: 'h', 18: 'i', 19: 'j', 20: 'k', 21: 'm',
                    22: 'n',  23: 'p', 24: 'q', 25: 'r', 26: 's', 27: 't', 28: 'u', 29: 'v', 30: 'w', 31: 'x',
                    32: 'y', 33: 'z'}

comparison_tabel1 = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10, 'b': 11,
                    'c': 12, 'd': 13, 'e': 14, 'f': 15, 'g': 16, 'h': 17, 'i': 18, 'j': 19, 'k': 20, 'm':21 ,
                    'n': 22, 'p': 23, 'q': 24, 'r': 25, 's': 26, 't': 27, 'u': 28, 'v': 29, 'w': 30, 'x': 31,
                    'y': 32, 'z': 33}

year_dict = {2019: 'A', 2020: 'B', 2021: 'C', 2022: 'D', 2023: 'E', 2024: 'F', 2025: 'G'}

year_dict1 = {'A': 2019, 'B': 2020, 'C': 2021, 'D': 2022, 'E': 2023, 'F': 2024, 'G': 2025}


def get_uc(record_path, assign_date_str=None):
    """获取图像的唯一编码"""
    uc_date = get_uc_date(assign_date_str)
    serial_number = get_serial_number_list(uc_date, record_path)[0]
    uc_rank = get_uc_rank(serial_number)
    return uc_date + uc_rank

def get_uc_list(record_path, uc_numb, assign_date_str=None):
    """获取指定数目的 uc"""
    uc_list = []
    uc_date = get_uc_date(assign_date_str)
    serial_number_list = get_serial_number_list(uc_date, record_path, count=uc_numb)
    for serial_number in serial_number_list:
        uc_rank = get_uc_rank(serial_number)
        uc_list.append(uc_date + uc_rank)
    return uc_list

def get_uc_date(assign_time_str=None):
    """获取 uc 前三位，如果不指定日期的话，就使用现在的时间"""
    if assign_time_str:
        year, month, day = assign_time_str[:4], assign_time_str[4:6], assign_time_str[6:8]
    else:
        date = datetime.datetime.now()
        year, month, day = date.year, date.month, date.day

    letter_1 = year_dict[year]

    if day <= 15:
        letter_2 = comparison_tabel[month + 9]          # 上半月，月份从a开始
        letter_3 = comparison_tabel[day + 9]
    else:
        letter_2 = comparison_tabel[month + 9 + 12]     # 下半月，月份从m开始
        letter_3 = comparison_tabel[day - 15 + 9]

    return letter_1 + letter_2 + letter_3

def get_date_from_uc_date(uc_date):
    """将uc_date转为正常的年月日"""
    year = year_dict1[uc_date[0]]
    # month =
    # pass

def get_uc_rank(serial_number, system=34):
    # 将不多于4万6的需要，编码至三位。每位有34种选择。
    # 方法：整除取余法
    assert serial_number <= 1336336, "编码溢出"
    remainder_1 = serial_number % system  # 取余数
    quotient_1 = serial_number // system

    remainder_2 = quotient_1 % system  # 取余数
    quotient_2 = quotient_1 // system

    remainder_3 = quotient_2 % system  # 取余数
    quotient_3 = quotient_2 // system

    remainder_4 = quotient_3 % system  # 取余数
    assert quotient_3 // system == 0, '编码溢出'

    letter_4 = comparison_tabel[remainder_4]
    letter_5 = comparison_tabel[remainder_3]
    letter_6 = comparison_tabel[remainder_2]
    letter_7 = comparison_tabel[remainder_1]
    return letter_4 + letter_5 + letter_6 + letter_7

def get_rank_from_uc_rank(serial_string):
    # 将36进制字符转换回十进制
    # 方法：整除取余法
    letter_1=int(comparison_tabel1[serial_string[0]])
    letter_2 = int(comparison_tabel1[serial_string[1]])
    letter_3 = int(comparison_tabel1[serial_string[2]])
    letter_4 = int(comparison_tabel1[serial_string[3]])
    count=letter_1*34*34*34+letter_2*34*34+letter_3*34+letter_4
    return str(count)

def get_serial_number_list(uc_date, record_path, count=1):
    """获取插入图片的index"""

    if os.path.exists(record_path):
        record_path_new = record_path+'.lock'
        # 删除历史 lock 文件防止冲突
        if os.path.exists(record_path_new):
            os.remove(record_path_new)
        shutil.move(record_path, record_path_new)
    else:
        return None

    record = JsonUtil.load_data_from_json_file(record_path_new)

    res = []
    if uc_date not in record:
        record[uc_date] = 0

    for i in range(count):
        record[uc_date] = record[uc_date] + 1
        res.append(record[uc_date])

    JsonUtil.save_data_to_json_file(record, record_path)
    return res



if __name__ == "__main__":

    record_json_path = r"C:\Users\14271\Desktop\del\record.json"

    print(get_uc(record_json_path))

    print(get_uc_list(record_json_path, uc_numb=50))




































import datetime
import json
import os
import xml.etree.ElementTree as ET
# 字母数值对照表
import cv2

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

object_count=1


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
    # 将不多于4万6的需要，编码至三位。每位有34种选择。
    # 方法：整除取余法
    assert serial_number <= 1336336, "编码溢出"
    remainder_1 = serial_number % 34  # 取余数
    quotient_1 = serial_number // 34

    remainder_2 = quotient_1 % 34  # 取余数
    quotient_2 = quotient_1 // 34

    remainder_3 = quotient_2 % 34  # 取余数
    quotient_3 = quotient_2 // 34

    remainder_4 = quotient_3 % 34  # 取余数
    assert quotient_3 // 34 == 0, '编码溢出'
    letter_4 = comparison_tabel[remainder_4]
    letter_5 = comparison_tabel[remainder_3]
    letter_6 = comparison_tabel[remainder_2]
    letter_7 = comparison_tabel[remainder_1]


    return letter_4 + letter_5 + letter_6+letter_7


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

def already_rename(name)-> bool:                   #通过图片前三位命名日期和当天日期进行比较，或者是否符合命名规则来判断图片是否已经入库
    date = datetime.datetime.now()
    year = date.year
    month = date.month
    day = date.day
    old_name=list(name)
    if old_name[0] not in year_dict1:
        return False
    elif old_name[1]not in comparison_tabel1:
        return False
    elif old_name[2]not in comparison_tabel1:
        return False
    elif int(year_dict1[old_name[0]]) <= year:
        com_year = year_dict1[old_name[0]]
        com_month = comparison_tabel1[old_name[1]]
        com_day = comparison_tabel1[old_name[2]]
        if com_month >= 10 and com_month <= 22:
            pic_month = com_month - 9
            pic_day = com_day - 9
        else:
            pic_month = com_month - 21
            pic_day = com_day + 6

        if pic_month < month:
            return True
        elif pic_month > month:
            if com_year < year:
                return True
            else:
                return False
        elif pic_month == month:
            if pic_day < day:
                return True
            elif pic_day==day:
                pic_no=old_name[3]+old_name[4]+old_name[5]+old_name[6]
                count_pic=coding_rank_back(pic_no)
                today_count=get_record(old_name[0]+old_name[1]+old_name[2])
                if int(count_pic)<=today_count:
                    return True
                else:
                    #print('NO.号超出当日记录')
                    return False
            elif com_year < year:
                return True
            else:
                return False
    else:
        return False

def coding_rank_back(serial_string) -> str:                            #将36进制返还会10进制来计数
    # 将36进制字符转换回十进制
    # 方法：整除取余法
    letter_1=int(comparison_tabel1[serial_string[0]])
    letter_2 = int(comparison_tabel1[serial_string[1]])
    letter_3 = int(comparison_tabel1[serial_string[2]])
    letter_4 = int(comparison_tabel1[serial_string[3]])
    count=letter_1*34*34*34+letter_2*34*34+letter_3*34+letter_4
    return str(count)

def img_filter(file_list) -> list:                                     #list中.jpg文件筛选函数
    if file_list[-4:]in['.jpg','.JPG','.png','.PNG','.bmp','BMP']:
        return True
    else:
        return False

def xml_filter(file_list)-> list:                                      #list中.xml文件筛选函数
    if file_list[-4:] in ['.xml']:
         return True
    else:
         return False

def json_filter(file_list)-> list:                                     #list中.json文件筛选函数
    if file_list[-5:] in ['.json']:
         return True
    else:
         return False
def get_xml_objects(xml_name)-> dict:                                  #从xml中读取objects
    with open('finish.txt', 'w', encoding='utf-8') as f1:
        # 路径信息
        # for xml_name in os.listdir(path):
        #     if xml_name.endswith(".xml"):
        #         xml_path = os.path.join(path, xml_name)
        tree = ET.parse(xml_name)
        root = tree.getroot()
        objects = {}
        global object_count
        object_count = 1
        # for name in root.iter('path'):
        #     rect['path'] = name.text
        for ob in root.iter('object'):
            rect = {}
            for bndbox in ob.iter('bndbox'):
                # 坐标信息
                for xmin in bndbox.iter('xmin'):
                    rect['xmin'] = xmin.text
                for ymin in bndbox.iter('ymin'):
                    rect['ymin'] = ymin.text
                for xmax in bndbox.iter('xmax'):
                    rect['xmax'] = xmax.text
                for ymax in bndbox.iter('ymax'):
                    rect['ymax'] = ymax.text
                line = rect['xmin'] + ' ' + rect['ymin'] + ' ' + rect['xmax'] + ' ' + rect['ymax'] + " "
                f1.write(line)
                # 文本信息
                for t in ob.iter('name'):
                    # print(t.text)
                    f1.write(t.text + '\n')
                for s in ob.iter('pose'):
                    # print(s.text)
                    f1.write(t.text + s.text + '\n')
                for h in ob.iter('truncated'):
                    # print(h.text)
                    f1.write(t.text + s.text + h.text)

                rect = {'label': t.text, 'shape_type': 'bndbox',
                        'points': {'xmin': rect['xmin'], 'ymin': rect['ymin'], 'xmax': rect['xmax'],
                                   'ymax': rect['ymax']}}
                objects[object_count] = rect
                object_count += 1
            for robndbox in ob.iter('robndbox'):
                # for l in bndbox:
                #     print(l.text)
                # 坐标信息
                for cx in robndbox.iter('cx'):
                    rect['cx'] = cx.text
                for cy in robndbox.iter('cy'):
                    rect['cy'] = cy.text
                for w in robndbox.iter('w'):
                    rect['w'] = w.text
                for h in robndbox.iter('h'):
                    rect['h'] = h.text
                for angle in robndbox.iter('angle'):
                    rect['angle'] = angle.text
                # print(rect['xmin']+ ' '+rect['ymin']+' '+rect['xmax']+' '+rect['ymax'])
                # line = rect['xmin'] + ' ' + rect['ymin'] + ' ' + rect['xmax'] + ' ' + rect['ymax'] + " "
                # f1.write(line)
                # 文本信息
                for t in ob.iter('name'):
                    # print(t.text)
                    f1.write(t.text + '\n')
                # for s in ob.iter('pose'):
                #     # print(s.text)
                #     f1.write(t.text + s.text + '\n')
                # for h in ob.iter('truncated'):
                #     # print(h.text)
                #     f1.write(t.text + s.text + h.text)
                rect = {'label': t.text, 'shape_type': 'robndbox',
                        'points': {'cx': rect['cx'], 'cy': rect['cy'], 'w': rect['w'], 'h': rect['h'],
                                   'angle': rect['angle']}}
                objects[object_count] = rect
                object_count += 1
        return objects

def get_json_objects(json_file)-> dict:                                      #从json中读取标注的objects
    json_objects = {}
    global object_count
    with open(json_file,'rb') as data:
        result = json.load(data)
    for dict in result['shapes']:
        dict.pop("group_id")
        dict.pop('flags')
        json_objects[object_count]=dict
        object_count+=1
    object_count=1
    return json_objects

def object_count2one():                                               #全局变量object_count归一
    global object_count
    object_count=1

def get_all_MD5(JSON_DIR)-> dict:                                    #获取out_json中所有json中的MD5值放入一个list
    json_list = os.listdir(JSON_DIR)
    all_MD5={}
    for json_file in json_list:
        with open(os.path.join(JSON_DIR,json_file) ,'r') as data:
            result = json.load(data)
        all_MD5[result['MD5']]=result['unique_code']
    return all_MD5


def get_xml_objects_with_count(xml_name,count)-> dict:                                  #从xml中读取objects
    with open('finish.txt', 'w', encoding='utf-8') as f1:
        # 路径信息
        # for xml_name in os.listdir(path):
        #     if xml_name.endswith(".xml"):
        #         xml_path = os.path.join(path, xml_name)
        tree = ET.parse(xml_name)
        root = tree.getroot()
        objects = {}
        object_count = count
        # for name in root.iter('path'):
        #     rect['path'] = name.text
        for ob in root.iter('object'):
            rect = {}
            for bndbox in ob.iter('bndbox'):
                # 坐标信息
                for xmin in bndbox.iter('xmin'):
                    rect['xmin'] = xmin.text
                for ymin in bndbox.iter('ymin'):
                    rect['ymin'] = ymin.text
                for xmax in bndbox.iter('xmax'):
                    rect['xmax'] = xmax.text
                for ymax in bndbox.iter('ymax'):
                    rect['ymax'] = ymax.text
                line = rect['xmin'] + ' ' + rect['ymin'] + ' ' + rect['xmax'] + ' ' + rect['ymax'] + " "
                f1.write(line)
                # 文本信息
                for t in ob.iter('name'):
                    # print(t.text)
                    f1.write(t.text + '\n')
                for s in ob.iter('pose'):
                    # print(s.text)
                    f1.write(t.text + s.text + '\n')
                for h in ob.iter('truncated'):
                    # print(h.text)
                    f1.write(t.text + s.text + h.text)

                rect = {'label': t.text, 'shape_type': 'bndbox',
                        'points': {'xmin': rect['xmin'], 'ymin': rect['ymin'], 'xmax': rect['xmax'],
                                   'ymax': rect['ymax']}}
                objects[object_count] = rect
                object_count += 1
            for robndbox in ob.iter('robndbox'):
                # for l in bndbox:
                #     print(l.text)
                # 坐标信息
                for cx in robndbox.iter('cx'):
                    rect['cx'] = cx.text
                for cy in robndbox.iter('cy'):
                    rect['cy'] = cy.text
                for w in robndbox.iter('w'):
                    rect['w'] = w.text
                for h in robndbox.iter('h'):
                    rect['h'] = h.text
                for angle in robndbox.iter('angle'):
                    rect['angle'] = angle.text
                # print(rect['xmin']+ ' '+rect['ymin']+' '+rect['xmax']+' '+rect['ymax'])
                # line = rect['xmin'] + ' ' + rect['ymin'] + ' ' + rect['xmax'] + ' ' + rect['ymax'] + " "
                # f1.write(line)
                # 文本信息
                for t in ob.iter('name'):
                    # print(t.text)
                    f1.write(t.text + '\n')
                # for s in ob.iter('pose'):
                #     # print(s.text)
                #     f1.write(t.text + s.text + '\n')
                # for h in ob.iter('truncated'):
                #     # print(h.text)
                #     f1.write(t.text + s.text + h.text)
                rect = {'label': t.text, 'shape_type': 'robndbox',
                        'points': {'cx': rect['cx'], 'cy': rect['cy'], 'w': rect['w'], 'h': rect['h'],
                                   'angle': rect['angle']}}
                objects[object_count] = rect
                object_count += 1
        return objects

def get_json_objects_with_count(json_file,count)-> dict:                                      #从json中读取标注的objects
    json_objects = {}
    object_count=count
    with open(json_file,'rb') as data:
        result = json.load(data)
    for dict in result['shapes']:
        dict.pop("group_id")
        dict.pop('flags')
        json_objects[object_count]=dict
        object_count+=1
    return json_objects



def have_record(code_date)->bool:
    with open ('record.json') as data:
        record = json.load(data)
        if  code_date in record:
            return True
        else:
            return False

def get_record(code_date)->int:
    with open('record.json') as data:
        record = json.load(data)
        return record[code_date]

def save_record(code_date,count):
    with open ('record.json') as data:
        record = json.load(data)
        record[code_date]=count
        new_record=json.dumps(record)
    with open('record.json','w') as data:
        data.write(new_record)

def split_box(img_filename,xml_name,obj_img_path,img_name):     #把图片按xml中的标注框，把标注目标分割出来
    #if os.path.exists(xml_name):  # 判断与图片同名的标签是否存在，因为图片不一定每张都打标
    img_cv = cv2.imread(img_filename)
    root = ET.parse(xml_name).getroot()  # 利用ET读取xml文件
    for obj in root.iter('object'):
        label = obj.find('name').text
        bndbox = obj.find('bndbox')
        xmin = int(float(bndbox.find('xmin').text))
        xmax = int(float(bndbox.find('xmax').text))
        ymin = int(float(bndbox.find('ymin').text))
        ymax = int(float(bndbox.find('ymax').text))
        obj_img = img_cv[int(ymin):int(ymax), int(xmin):int(xmax)]
        path=obj_img_path+'\\'+label
        if not os.path.exists(path):
            os.mkdir(path)
        cv2.imwrite(os.path.join(path,img_name+'_'+label+'_'+'['+str(xmin)+','+str(ymax)+','+str(xmax)+','+str(ymin)+']'+'.jpg'),obj_img)


def already_in_database(unique_code)-> bool:
    with open ('record.json') as data:
        record=json.load(data)
    key_as_date=unique_code[0:3]
    value_as_num=coding_rank_back(unique_code[-4:])
    if (int(record[key_as_date])>=int(value_as_num)):
        return True
    else:
        return False


# root=r'E:\测试库\绝缘子-60\云南绝缘子雷击-6\lalalalal'
# root1=r'E:\测试库\绝缘子-60'
# root2=r'E:\测试库\绝缘子-59'
# print(os.path.join(root2,root.lstrip(root1)))
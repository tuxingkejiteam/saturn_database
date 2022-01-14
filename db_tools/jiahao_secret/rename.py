import os
import shutil

from tqdm import tqdm
from useful_funtion import *  # first_3_letters, coding_rank, binary2ten,already_rename,img_filter,xml_filter,json_filter,get_xml_objects,get_json_objects,object_count2one
from PIL import Image
import json
import hashlib
import time


def load_data(img_org_dir, img_output_dir, json_output_dir):
    data_list = os.listdir(img_org_dir)  # 获取导入数据目录下的所有文件
    img_name_list = list(filter(img_filter, data_list))  # 导入数据中的jpg文件放入对应list
    xml_name_list = list(filter(xml_filter, data_list))  # 导入数据中的xml文件放入对应list
    json_name_list = list(filter(json_filter, data_list))  # 导入数据中的json文件放入对应list
    img_num = len(img_name_list)  # 这批数据中图片数据的数量
    already_store_count = 0  # 计数器，数据中多少张已经入过库
    print("共有{}张图片将被重命名并创建json。".format(img_num))

    letters_1_3 = first_3_letters()  # 日期位，代表年月日
    #  重命名图片从0开始命名4~7位
    if not have_record(letters_1_3):  # 是就接着命名，不是就从0开始。
        save_record(letters_1_3, 0)
        i = 0
    else:
        i = get_record(letters_1_3)

    # TODO：这里要修改为查数据库
    with open('all_MD5.json', 'r') as file:
        MD5_list = json.load(file)

    for img_name in img_name_list:
        jsontext = {}  # 建立一个用以存储图片标注信息的字典。
        if already_rename(img_name):  # 靠名字判断是否已入库
            already_store_count += 1
            continue

        im = Image.open(os.path.join(img_org_dir, img_name))  # 返回一个Image对象
        if im.mode != 'RGB':
            im = im.convert('RGB')
            im.save(os.path.join(img_org_dir, img_name[:-4] + '.jpg'))
        if img_name[-4:] not in ['.jpg', 'JPG']:
            im.save(os.path.join(img_org_dir, img_name[:-4] + '.jpg'))

        # 这里又打开了一次图片。感觉莫名的不爽。
        with open(os.path.join(img_org_dir, img_name), 'rb') as fp:  # 读取对Image对象的MD5值，来帮助我们确定数据唯一入库
            data = fp.read()
        file_md5 = hashlib.md5(data).hexdigest()

        # TODO：这里要修改为查数据库
        if file_md5 in MD5_list:
            already_store_count += 1
            img_org_path = os.path.join(img_org_dir, img_name)
            img_output_path = os.path.join(img_output_dir, MD5_list[file_md5] + '.jpg')
            shutil.copy(img_org_path, img_output_path)
            continue
        else:
            letters_4_7 = coding_rank(i)  # 序号位，代表这是本批次图片的第几张。
            img_new_name = letters_1_3 + letters_4_7
            MD5_list[file_md5] = img_new_name  # TODO：这里没必要再更新json的md5字典了

        #  -------------------------------这一块要单独拆分为一个函数---------------------------------
        # 函数要传入一组参数，用以写入所需信息。
        jsontext['org_name'] = img_name
        letters_4_7 = coding_rank(i)  # 序号位，代表这是本批次图片的第几张。
        img_new_name = letters_1_3 + letters_4_7  # 图片重命名1~3：日期 4~7：当日的入库NO.  当前默认为未添加标注编码
        jsontext['unique_code'] = letters_1_3 + letters_4_7  # 独立编码：日期+NO.
        jsontext['size'] = {'width': str(im.width), 'height': str(im.height)}  # 图片尺寸
        jsontext['objects'] = {}  # 包含的标注文件的objects信息
        if img_name.split('.')[0] + '.xml' in xml_name_list:  # 从xml中获取objects
            xml_objects = get_xml_objects(os.path.join(img_org_dir, img_name[:-4] + '.xml'))
            jsontext['objects'].update(xml_objects)
        else:
            object_count2one()
        if img_name.split('.')[0] + '.json' in json_name_list:  # 从json中获取onjects
            json_objects = get_json_objects(os.path.join(img_org_dir, img_name[:-4] + '.json'))
            jsontext['objects'].update(json_objects)
        jsontext["train_info"] = ""  # 新数据无需写入这个
        jsontext["trace"] = "1"  # 作为参数传入，默认是可溯源的。
        jsontext["visible"] = "1"  # 作为参数传入，默认是可见光的。
        jsontext['MD5'] = file_md5
        jsontext["extra_info"] = []  # TODO：这里要调用一个形成额外信息的函数。
        #  -------------------------------这一块要单独拆分为一个函数---------------------------------

        json_data = json.dumps(jsontext, indent=4, ensure_ascii=False)
        img_org_path = os.path.join(img_org_dir, img_name[:-4] + '.jpg')
        i += 1
        # binary = '000000000000000'  # 2进制类别列表------------有点问题的地方----------------------
        # if binary != 0:
        #     ten_str = binary2ten(str(binary))
        #     img_new_name = img_new_name.replace('unlabeled', ten_str)  # 添加类别索引后缀  # 这里不用再添加类别索引了。

        img_output_path = os.path.join(img_output_dir, img_new_name + '.jpg')  # 将图片重命名后拷贝至out目录
        json_output_path = os.path.join(json_output_dir, img_new_name + '.json')  # 在json_out目录中生成对应的json文件
        shutil.copy(img_org_path, img_output_path)
        with open(json_output_path, 'w') as f:
            f.write(json_data)

    print('其中%d张已存储过' % already_store_count)  # 通过命名和MD5值两重筛选，判断图片是否已经入库过，打印处从中筛选出的图片数量
    # file=open( os.path.join(os.getcwd(), letters_1_3 + '.txt'),'w')  #将经过循环遍历的当日i值（当日入库图片数量）写入36进制日期同名txt文件中
    # file.write(str(i))
    # file.close()

    # TODO：这里就不需要了，直接通过数据库完成。
    save_record(letters_1_3, i)
    with open('all_MD5.json', 'w') as data:  # 这里又读了一遍md5列表。
        result = json.dumps(MD5_list)
        data.write(result)

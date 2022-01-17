import os
import shutil

import numpy as np
from tqdm import tqdm
from useful_funtion import *#first_3_letters, coding_rank, binary2ten,already_rename,img_filter,xml_filter,json_filter,get_xml_objects,get_json_objects,object_count2one
from PIL import Image
import json
import hashlib
import time

def load_data(img_org_dir,img_output_dir,json_output_dir):
    # data_list = os.listdir(img_org_dir)                              #获取导入数据目录下的所有文件
    # img_name_list=list(filter(img_filter,data_list))                 #导入数据中的jpg文件放入对应list
    # xml_name_list = list(filter(xml_filter, data_list))              #导入数据中的xml文件放入对应list
    # json_name_list = list(filter(json_filter, data_list))            #导入数据中的json文件放入对应list
    # img_num = len(img_name_list)                                     #这批数据中图片数据的数量
    already_store_count=0                                            #计数器，数据中多少张已经入过库
    #print("共有{}张图片将被重命名并创建json。".format(img_num))
    letters_1_3 = first_3_letters()                                  # 日期位，代表年月日
    # if not os.path.exists(os.getcwd()+ '/' + letters_1_3+'.txt'):    #创建对应36位计数的当天txt文件记录当日入库图片数量
    #     file=open(os.path.join(os.getcwd(), letters_1_3 + '.txt'), 'w')
    #     file.write('0')
    #     file.close()
    #     i = 0
    #     #重命名图片从0开始命名4~7位
    if not have_record(letters_1_3):
        save_record(letters_1_3, 0)
        i=0
    else:
        # file = open(os.path.join(os.getcwd(), letters_1_3 + '.txt'), 'r')
        # i=int(file.readline())                                       #这批重命名图片从txt中的数字开始命名（图片从0开始命名）
        # file.close()
        i=get_record(letters_1_3)
    #MD5_list=get_all_MD5(r'E:\测试库\output_json1')                            #从已生成json中获取所有已入库的MD5值，放入list
    with open ('all_MD5.json','r') as file:
        MD5_list=json.load(file)
    for root,dirs,files in os.walk(img_org_dir):                             #进度条
        for img_name in files:
            if img_name[-4:]not in['.jpg','.JPG','.png','.PNG','.bmp','.BMP']:
                 continue
            if already_rename(img_name)==True:                           #靠名字判断是否已入库
                #print(img_name+'xxx')
                already_store_count += 1
                continue
            try:
                im = Image.open(os.path.join(root, img_name))         # 返回一个Image对象
            except:
                img_org_path = os.path.join(root, img_name[:-4] + '.jpg')
                img_output_dir2 = os.path.join(img_output_dir, root.lstrip(img_org_dir))
                #img_output_dir2 = img_output_dir + img_output_dir1
                # print(img_output_dir2)
                if not os.path.isdir(img_output_dir2):
                    os.makedirs(img_output_dir2)
                img_output_path1 = os.path.join(img_output_dir2, img_name)  # 将图片重命名后拷贝至out目录
                shutil.copy(img_org_path, img_output_path1)
                continue
            if im.mode!='RGB':
                im=im.convert('RGB')
                im.save(os.path.join(root, img_name[:-4]+'.jpg'))
            if img_name[-4:] not in ['.jpg','JPG']:
                #newName = img_name.replace(img_name[-4:], '.jpg')
                im.save(os.path.join(root, img_name[:-4] + '.jpg'))


            with open(os.path.join(root, img_name), 'rb') as fp:  # 读取对Image对象的MD5值，来帮助我们确定数据唯一入库
                data = fp.read()
            file_md5 = hashlib.md5(data).hexdigest()

            if file_md5 in MD5_list:
                print(img_name)
                already_store_count+=1
                img_org_path = os.path.join(root, img_name[:-4] + '.jpg')
                print(img_org_path)
                img_output_dir2 = os.path.join(img_output_dir, root.lstrip(img_org_dir))
                # print(img_output_dir1)
                # img_output_dir2 = img_output_dir + img_output_dir1
                # print(img_output_dir2)
                if not os.path.isdir(img_output_dir2):
                    os.makedirs(img_output_dir2)
                img_output_path1 = os.path.join(img_output_dir2, MD5_list[file_md5]+'.jpg')  # 将图片重命名后拷贝至out目录
                shutil.copy(img_org_path, img_output_path1)
                print(MD5_list[file_md5]+'.jpg')
                continue
            else:
                letters_4_7 = coding_rank(i)  # 序号位，代表这是本批次图片的第几张。
                img_new_name = letters_1_3 + letters_4_7
                MD5_list[file_md5]=img_new_name
            jsontext = {}
            jsontext['org_name'] = img_name
            # letters_4_7 = coding_rank(i)                                 # 序号位，代表这是本批次图片的第几张。
            # img_new_name = letters_1_3 + letters_4_7      #图片重命名1~3：日期 4~7：当日的入库NO.  当前默认为未添加标注编码
            jsontext['unique_code'] = letters_1_3 + letters_4_7          #独立编码：日期+NO.
            jsontext['size']={'width':str(im.width),'height':str(im.height)}  #图片尺寸
            jsontext['class_code'] = 'unlabelled'
            jsontext['objects'] ={}                                      #包含的标注文件的objects信息
            # if img_name.split('.')[0]+'.xml' in xml_name_list:           #从xml中获取objects
            #     xml_objects=get_xml_objects(os.path.join(img_org_dir, img_name.strip('.jpg')+'.xml'))
            #     jsontext['objects'].update(xml_objects)
            #     #split_box(os.path.join(img_org_dir, img_name),os.path.join(img_org_dir,img_name.split('.')[0]+'.xml'),'split_boxes',img_new_name)
            # else:
            #     object_count2one()
            # if img_name.split('.')[0]+'.json' in json_name_list:          #从json中获取onjects
            #     json_objects=get_json_objects(os.path.join(img_org_dir, img_name.strip('.jpg')+'.json'))
            #     jsontext['objects'].update(json_objects)
            jsontext["train_info"] = ""
            jsontext["trace"] = "1"
            jsontext["visible"] = "1"
            jsontext['MD5'] = file_md5
            jsontext["extra_info"] = ['销钉安装不规范训练集','历史遗留小图']
            json_data = json.dumps(jsontext, indent=4,ensure_ascii=False)
            img_org_path = os.path.join(root, img_name[:-4]+'.jpg')
            i += 1
            binary = '000000000000000'  # 2进制类别列表------------有点问题的地方----------------------
            if binary != 0:
                ten_str = binary2ten(str(binary))
                img_new_name = img_new_name.replace('unlabeled', ten_str)            # 添加类别索引后缀
            img_output_path = os.path.join(img_output_dir, img_new_name + '.jpg')    #将图片重命名后拷贝至out目录
            print(img_output_path)
            img_output_dir2=os.path.join(img_output_dir,root.lstrip(img_org_dir))
            #img_output_dir2 = img_output_dir+img_output_dir1
            print(img_output_dir2)
            if not os.path.isdir(img_output_dir2):
                os.makedirs(img_output_dir2)
            img_output_path1 = os.path.join(img_output_dir2, img_new_name + '.jpg')  # 将图片重命名后拷贝至out目录
            #print(img_output_path1)
            json_output_path = os.path.join(json_output_dir, img_new_name + '.json') #在json_out目录中生成对应的json文件
            shutil.copy(img_org_path, img_output_path)
            shutil.copy(img_org_path, img_output_path1)
            f = open(json_output_path, 'w')
            f.write(json_data)
            f.close()
    time.sleep(0.01)
    print('其中%d张已存储过'%already_store_count)                                #通过命名和MD5值两重筛选，判断图片是否已经入库过，打印处从中筛选出的图片数量
    # file=open( os.path.join(os.getcwd(), letters_1_3 + '.txt'),'w')             #将经过循环遍历的当日i值（当日入库图片数量）写入36进制日期同名txt文件中
    # file.write(str(i))
    # file.close()
    save_record(letters_1_3,i)

import pymysql
import os
import datetime
import json
import hashlib
import shutil
import label_check
from PIL import Image
import xml.etree.ElementTree as ET


# TODO：读取xml和json信息的函数，独立功能拆分
class DataLoader(object):  # 数据入库类
    def __init__(self, host='localhost', user='root', password='', db_name='Saturn_Database'):
        # 链接数据库。
        # 入参：数据库服务器地址，用户名，密码，数据库名
        # 出参：用户名，地址，数据库名，密码，数据库，游标形式的数据库，大类小类对照表，json标注信息类。
        self.user = user
        self.host = host
        self.db_name = db_name

        if password == '':
            # TODO:输入密码时，需使用暗文显示。当前为明文。
            self.password = input('请输入{}用户密码：'.format(self.user))
        else:
            self.password = password
        self.database = pymysql.connect(host=self.host,
                                        user=self.user,
                                        password=self.password,
                                        database=self.db_name
                                        )
        print('数据库连接成功！版本号：1.0')
        self.db_cursor = self.database.cursor()
        with open('docs/record.json') as data:
            record = json.load(data)
        self.record = record

        # TODO：根据当前日期生成数据仓库中，图片和json的目录。
        self.img_output_dir = ''  # 图片输出地址
        self.json_output_dir = ''  # json输出地址

        self.comparison_tabel = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9',
                                 10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f', 16: 'g', 17: 'h', 18: 'i',
                                 19: 'j', 20: 'k', 21: 'm', 22: 'n', 23: 'p', 24: 'q', 25: 'r', 26: 's', 27: 't',
                                 28: 'u', 29: 'v', 30: 'w', 31: 'x', 32: 'y', 33: 'z'}
        self.year_dict = {2019: 'A', 2020: 'B', 2021: 'C', 2022: 'D', 2023: 'E', 2024: 'F', 2025: 'G'}

    def DataLoader(self, data_dir):
        # 数据入库时调用，外部接口,传入新增数据所在目录
        # TODO:首先进行标注质量检查，若标注检查不通过则不能会继续入库操作。
        check_pass = label_check(data_dir)  # 将xml检测脚本写为一个bool型的函数。
        # TODO：暂时先这样，之后将检查逻辑并入get_json_objects和get_xml_objects当中。

        if check_pass:
            log_info = self.__data_loader(data_dir)  # TODO:返回一个用于打印log的字典。
            '''
            该函数理想逻辑：
            读取一张图片的md5，查询数据库。生成新图列表和旧图列表。
            if 新图：并生成一个json字典，若目录下有标注文件，则将标注文件中的信息写入字典。保存。
            if 旧图：将进行标注合并操作。
            '''
            # TODO：打印导入的log
            print(log_info)
        else:
            print("标注存在问题，请查看检查记录。")

    def __data_loader(self, img_org_dir) -> dict:
        # 传入数据所在目录。返回已给打印log信息的字典。
        # TODO：这里要修改为查数据库之后，就不必调用了。
        with open('all_MD5.json', 'r') as file:
            MD5_list = json.load(file)

        data_list = os.listdir(img_org_dir)  # 获取导入数据目录下的所有文件
        img_name_list = list(filter(self.__img_filter, data_list))  # 导入数据中的jpg文件放入对应list
        xml_name_list = list(filter(self.__xml_filter, data_list))  # 导入数据中的xml文件放入对应list
        json_name_list = list(filter(self.__json_filter, data_list))  # 导入数据中的json文件放入对应list
        # img_num = len(img_name_list)  # 这批数据中图片数据的数量
        already_store_count = 0  # 计数器，数据中多少张已经入过库
        # print("共有{}张图片将被重命名并创建json。".format(img_num))

        letters_1_3 = self.__first_3_letters()  # 日期位，代表年月日
        date_code = letters_1_3  # 给日期编码起个别名而已，没有特别的用处。

        # 重命名图片从第几张开始。如果是个新日期，那么就在record的记录文件中添加一条记录。
        if date_code not in self.record:
            self.record[date_code] = 0
            img_num = 0
        else:
            img_num = self.record[date_code]

        # 这里暂时只考虑了新图+标注的情况。
        for img_name in img_name_list:
            # TODO:手动实现进度条。

            # TODO：实际的IO操作，要到不得不进行的时候再进行。这里先读取之后，后面还会有md5的判断。要在md5判断之后读取。毕竟不满足条件的数据是少数。
            im = Image.open(os.path.join(img_org_dir, img_name))  # 返回一个Image对象
            if im.mode != 'RGB':
                im = im.convert('RGB')
                im.save(os.path.join(img_org_dir, img_name[:-4] + '.jpg'))
            if img_name[-4:] not in ['.jpg', 'JPG']:  # TODO：少一个点，小错误
                im.save(os.path.join(img_org_dir, img_name[:-4] + '.jpg'))  # TODO：这里重复还是操作了。

            # 这里又打开了一次图片。但是似乎也没有很好的办法。
            with open(os.path.join(img_org_dir, img_name), 'rb') as fp:
                # 读取对Image对象的MD5值，来帮助我们确定数据唯一入库
                data = fp.read()
            file_md5 = hashlib.md5(data).hexdigest()

            # TODO：这里要修改为查数据库
            if file_md5 in MD5_list:  # 如果是已经存在的图片，则跳过
                already_store_count += 1
                img_org_path = os.path.join(img_org_dir, img_name)
                img_output_path = os.path.join(self.img_output_dir, MD5_list[file_md5] + '.jpg')
                shutil.copy(img_org_path, img_output_path)  # TODO：这里为什么要覆盖一下？
                continue
            # else:
            # letters_4_7 = coding_rank(i)  # 序号位，代表这是本批次图片的第几张。
            # img_new_name = letters_1_3 + letters_4_7
            # MD5_list[file_md5] = img_new_name  # TODO：这里没必要再更新json的md5字典了
            letters_4_7 = self.__coding_rank(img_num)  # 序号位，代表这是本批次图片的第几张。
            img_new_name = letters_1_3 + letters_4_7  # 图片重命名1~3：日期 4~7：当日的入库NO.  当前默认为未添加标注编码

            json_data = self.__create_json_dic(img_name, img_new_name, im, file_md5, img_org_dir, xml_name_list,
                                               json_name_list)  # 将信息写入json
            img_org_path = os.path.join(img_org_dir, img_name[:-4] + '.jpg')
            img_num += 1

            img_output_path = os.path.join(self.img_output_dir, img_new_name + '.jpg')  # 将图片重命名后拷贝至out目录
            json_output_path = os.path.join(self.json_output_dir, img_new_name + '.json')  # 在json_out目录中生成对应的json文件
            shutil.copy(img_org_path, img_output_path)

            with open(json_output_path, 'w') as f:
                f.write(json_data)

        print('其中%d张已存储过' % already_store_count)  # 通过命名和MD5值两重筛选，判断图片是否已经入库过，打印处从中筛选出的图片数量

        # TODO：这里还是通过数据库完成。
        self.__save_record(letters_1_3, img_num)
        with open('all_MD5.json', 'w') as data:  # 这里又读了一遍md5列表。
            result = json.dumps(MD5_list)
            data.write(result)

    def __create_json_dic(self, img_name, img_new_name, im, file_md5, img_org_dir, xml_name_list,
                          json_name_list):
        # --------------------------------------
        # TODO：汉明距离编码写入
        from tools.similar_search import difference
        diff = difference(im)  # TODO：修改函数内部，形成字符串
        # --------------------------------------

        # 函数要传入一组参数，用以写入所需信息。
        json_dic = {'org_name': img_name, 'unique_code': img_new_name,
                    'size': {'width': str(im.width), 'height': str(im.height)}, 'objects': {}}  # 创建一个字典。

        if img_name.split('.')[0] + '.xml' in xml_name_list:  # 从xml中获取objects
            xml_objects = self.__get_xml_objects(os.path.join(img_org_dir, img_name[:-4] + '.xml'))
            json_dic['objects'].update(xml_objects)
        else:
            self.__object_count2one()
        if img_name.split('.')[0] + '.json' in json_name_list:  # 从json中获取objects
            json_objects = self.__get_json_objects(os.path.join(img_org_dir, img_name[:-4] + '.json'))
            json_dic['objects'].update(json_objects)
        json_dic["train_info"] = ""  # 新数据无需写入这个
        json_dic["trace"] = "1"  # TODO:作为参数传入，默认是可溯源的。
        json_dic["visible"] = "1"  # TODO:作为参数传入，默认是可见光的。
        json_dic['MD5'] = file_md5
        json_dic["extra_info"] = []  # TODO：这里弄一个形成额外信息的函数。
        json_dic["diff"] = diff

        json_data = json.dumps(json_dic, indent=4, ensure_ascii=False)

        return json_data

    @staticmethod
    def __get_xml_objects(xml_name) -> dict:  # 从xml中读取objects
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

    def __coding_rank(self, serial_number) -> str:
        # 编码至四位。每位有34种选择。
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
        letter_4 = self.comparison_tabel[remainder_4]
        letter_5 = self.comparison_tabel[remainder_3]
        letter_6 = self.comparison_tabel[remainder_2]
        letter_7 = self.comparison_tabel[remainder_1]

        return letter_4 + letter_5 + letter_6 + letter_7

    @staticmethod
    def __img_filter(file_list) -> bool:  # list中.jpg文件筛选函数
        if file_list[-4:] in ['.jpg', '.JPG', '.png', '.PNG', '.bmp', 'BMP']:
            return True
        else:
            return False

    @staticmethod
    def __xml_filter(file_list) -> bool:  # list中.xml文件筛选函数
        if file_list[-4:] in ['.xml']:
            return True
        else:
            return False

    @staticmethod
    def __json_filter(file_list) -> bool:  # list中.json文件筛选函数
        if file_list[-5:] in ['.json']:
            return True
        else:
            return False

    def __first_3_letters(self) -> str:
        date = datetime.datetime.now()
        year = date.year
        month = date.month
        day = date.day
        letter_1 = self.year_dict[year]

        if day <= 15:
            letter_2 = self.comparison_tabel[month + 9]  # 上半月，月份从a开始
            letter_3 = self.comparison_tabel[day + 9]
        else:
            letter_2 = self.comparison_tabel[month + 9 + 12]  # 下半月，月份从m开始
            letter_3 = self.comparison_tabel[day - 15 + 9]

        return letter_1 + letter_2 + letter_3

    @staticmethod
    def __save_record(code_date, count):
        with open('record.json') as data:
            record = json.load(data)
            record[code_date] = count
            new_record = json.dumps(record)
        with open('record.json', 'w') as data:
            data.write(new_record)

    @staticmethod
    def __object_count2one():  # 全局变量object_count归一
        global object_count  # TODO:不要搞全局变量
        object_count = 1

    @staticmethod
    def __get_json_objects(json_file) -> dict:  # 从json中读取标注的objects
        json_objects = {}
        global object_count  # TODO：绝对不要搞全局变量。
        with open(json_file, 'rb') as data:
            result = json.load(data)
        for dict in result['shapes']:  # TODO:这里要重命名，不要和python的字段重复
            dict.pop("group_id")
            dict.pop('flags')
            json_objects[object_count] = dict
            object_count += 1
        object_count = 1
        return json_objects

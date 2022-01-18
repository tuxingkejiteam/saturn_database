# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from JoTools.txkjRes.deteRes import DeteRes
from JoTools.utils.FileOperationUtil import FileOperationUtil


# get json

# save_to_json



def get_json_from_xml(xml_path, uc, save_path, img_path=None):

    jsontext = {}
    jsontext['org_name'] = img_name

    letters_4_7 = coding_rank(i)                                            # 序号位，代表这是本批次图片的第几张。
    img_new_name = letters_1_3 + letters_4_7                                # 图片重命名1~3：日期 4~7：当日的入库NO.  当前默认为未添加标注编码

    jsontext['unique_code'] = letters_1_3 + letters_4_7                     # 独立编码：日期+NO.

    jsontext['size'] = {'width': str(im.width), 'height': str(im.height)}   # 图片尺寸

    jsontext['class_code'] = 'unlabelled'

    jsontext['objects'] = {}  # 包含的标注文件的objects信息

    if img_name.split('.')[0] + '.xml' in xml_name_list:  # 从xml中获取objects
        xml_objects = get_xml_objects(os.path.join(img_org_dir, img_name[:-4] + '.xml'))
        jsontext['objects'].update(xml_objects)
    else:
        object_count2one()
    if img_name.split('.')[0] + '.json' in json_name_list:  # 从json中获取onjects
        json_objects = get_json_objects(os.path.join(img_org_dir, img_name[:-4] + '.json'))
        jsontext['objects'].update(json_objects)
    jsontext["train_info"] = []
    jsontext["trace"] = "1"
    jsontext["visible"] = "1"
    jsontext['MD5'] = file_md5
    jsontext["extra_info"] = ['瓷瓶棒']
    jsontext["mode"] = ''
    json_data = json.dumps(jsontext, indent=4, ensure_ascii=False)


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







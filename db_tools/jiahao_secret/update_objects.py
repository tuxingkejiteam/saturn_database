import os
import json
import time
from 嘉浩的秘密宝藏.def_class import ImgLabel
from tqdm import tqdm

from useful_funtion import get_xml_objects_with_count, xml_filter, json_filter, get_json_objects_with_count


def update_objects(update_dir, json_dir):
    data_list = os.listdir(update_dir)
    xml_name_list = list(filter(xml_filter, data_list))
    json_name_list = list(filter(json_filter, data_list))

    for xml_name in tqdm(xml_name_list):
        # with open(os.path.join(json_dir,xml_name.strip('.xml')+".json")) as file:
        #     result = json.load(file)
        # count=len(result['objects'])+1
        img_label = ImgLabel(os.path.join(json_dir, xml_name[:-4] + ".json"))
        count = img_label.objects_num + 1
        update_objects = get_xml_objects_with_count(os.path.join(update_dir, xml_name), count)
        img_label.objects.update(update_objects)
        # result['objects'].update(update_objects)
        # json_data = json.dumps(result, indent=4)
        with open(os.path.join(json_dir, xml_name[:-4] + ".json"), 'w') as file:
            file.write(json.dumps(img_label.json_data, indent=4, ensure_ascii=False))
    time.sleep(0.001)
    print('%d份xml文件已合并' % len(xml_name_list))
    time.sleep(0.001)

    for json_name in tqdm(json_name_list):
        # with open(os.path.join(json_dir,json_name)) as file:
        #     result = json.load(file)
        img_label = ImgLabel(os.path.join(json_dir, json_name))
        count = img_label.objects_num + 1
        update_objects = get_json_objects_with_count(os.path.join(update_dir, json_name), count)
        # result['objects'].update(update_objects)
        img_label.objects.update(update_objects)
        # json_data = json.dumps(result, indent=4)
        with open(os.path.join(json_dir, json_name), 'w') as file:
            file.write(json.dumps(img_label.json_data, indent=4, ensure_ascii=False))
    time.sleep(0.01)
    print('%d份json文件已合并' % len(xml_name_list))

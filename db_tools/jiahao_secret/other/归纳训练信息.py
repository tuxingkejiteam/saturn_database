import hashlib
import json
import os
import xml.etree.ElementTree as ET

from tqdm import tqdm

lbd_path=r'\\192.168.3.80\算法-数据交互\铝包带标注\lbd'
model='lbd'
model_name='lbd_v1.0.0.0'
version='v1.0.0.0'
label_list=[]
train_list=[]
with open('all_MD5.json', 'r') as file:
    MD5_list = json.load(file)
for img_file in tqdm(os.listdir(lbd_path)):
    if img_file[-4:] in ['.jpg','.JPG']:
        with open(os.path.join(lbd_path, img_file), 'rb') as fp:  # 读取对Image对象的MD5值，来帮助我们确定数据唯一入库
            data = fp.read()
        file_md5 = hashlib.md5(data).hexdigest()
        train_list.append(MD5_list[file_md5])
    if img_file[-4:] in ['.xml']:
        tree = ET.parse(os.path.join(lbd_path, img_file))
        root = tree.getroot()
        objects = {}
        # for name in root.iter('path'):
        #     rect['path'] = name.text
        for ob in root.iter('object'):
            for t in ob.iter('name'):
                if t.text not in label_list:
                    label_list.append(t.text)

train_dict={
    'model':model,
    'model_version':version,
    'label_used':label_list,
    'train_data_list':train_list
}

# with open ('train_info.json','r') as json_data:
#     data=json.load(json_data)
#     data[model_name]=train_dict
#
#
# if not os.path.exists(model+'_'+version+'.json'):


with open (model+'_'+version+'.json','w') as json_data:
    new_record=json.dumps(train_dict,indent=4)
    json_data.write(new_record)
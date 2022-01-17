import hashlib
import json
import os

from PIL import Image
from tqdm import tqdm

path = r'\\192.168.3.80\算法-数据交互\销钉安装不到位\Normal_feets 侧面一脚'
outpath = r'\\192.168.3.80\算法-数据交互\json_output'
with open('all_MD5.json', 'r') as file:
    MD5_list = json.load(file)



for file in tqdm(os.listdir(path)):
    with open(os.path.join(path, file), 'rb') as fp:  # 读取对Image对象的MD5值，来帮助我们确定数据唯一入库
        data = fp.read()
    file_md5 = hashlib.md5(data).hexdigest()
    if file_md5 not in MD5_list:
        continue
    jsontext={}
    jsontext['org_name'] = file
    #letters_4_7 = coding_rank(i)  # 序号位，代表这是本批次图片的第几张。
    #img_new_name = letters_1_3 + letters_4_7  # 图片重命名1~3：日期 4~7：当日的入库NO.  当前默认为未添加标注编码
    jsontext['unique_code'] = MD5_list[file_md5]  # 独立编码：日期+NO.
    im = Image.open(os.path.join(path, file))
    jsontext['size'] = {'width': str(im.width), 'height': str(im.height)}  # 图片尺寸
    jsontext['class_code'] = 'unlabelled'
    jsontext['objects'] = {
        "1": {
            "label": "kkx_nor_侧面一脚",
            "shape_type": "bndbox",
            "points": {
                "xmin": "0",
                "ymin": "0",
                "xmax": str(im.width),
                "ymax": str(im.height)
            }
        }
    }
    if MD5_list[file_md5][:3]!='Czp':
        jsontext["train_info"] = ['销钉安装不规范']
        jsontext["trace"] = "0"
        jsontext["visible"] = "1"
        jsontext['MD5'] = file_md5
        jsontext["extra_info"] = ['销钉安装不规范训练集', '历史遗留小图']
    else:
        jsontext["train_info"] = ['销钉安装不规范','开口销缺失']
        jsontext["trace"] = "0"
        jsontext["visible"] = "1"
        jsontext['MD5'] = file_md5
        jsontext["extra_info"] = ['销钉安装不规范训练集', '历史遗留小图','开口销缺失训练集']
    json_data = json.dumps(jsontext, indent=4, ensure_ascii=False)
    with open(os.path.join(outpath,MD5_list[file_md5]+'.json'),'w') as data:
        data.write(json_data)
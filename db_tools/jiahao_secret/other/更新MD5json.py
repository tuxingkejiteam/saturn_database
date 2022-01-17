import hashlib
import json
import os

from tqdm import tqdm

with open('all_MD5.json', 'r') as file:
    MD5_list = json.load(file)

path = r'\\192.168.3.80\算法-数据交互\销钉安装不到位 命名\Normal_feets 侧面一脚'
for img in tqdm(os.listdir(path)):
    with open(os.path.join(path, img), 'rb') as fp:  # 读取对Image对象的MD5值，来帮助我们确定数据唯一入库
        data = fp.read()
    file_md5 = hashlib.md5(data).hexdigest()
    MD5_list[file_md5]=img[:-4]





with open ('all_MD5.json','w') as data:
    result = json.dumps(MD5_list)
    data.write(result)
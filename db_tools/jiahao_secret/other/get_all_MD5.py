import json
import os
# path=r'\\192.168.3.80\原始数据\图片数据管理库'
# all_MD5={}
# for root, dirs, files in os.walk(path):  # 进度条
#      for json_name in files:
#          if json_name[-5:] in ['.json']:
#              with open(os.path.join(root, json_name), 'r') as data:
#                  result = json.load(data)
#              all_MD5[result['MD5']] = result['unique_code']

#json_data=json.dumps(all_MD5)
from tqdm import tqdm

f = open('all_MD5.json', 'r')
all_MD5=json.load(f)
f.close()

json_list = os.listdir('output_json1')
for json_file in tqdm (json_list):
    with open(os.path.join('output_json1',json_file) ,'r') as data:
        result = json.load(data)
    all_MD5[result['MD5']]=result['unique_code']


with open('all_MD5.json' ,'w') as data:
    result = json.dumps(all_MD5)
    data.write(result)
import json
import os

from tqdm import tqdm

dir=r'F:\绝缘子污秽\json'
json_list = os.listdir(dir)
for jsonfile in tqdm(json_list):
    with open(os.path.join(dir,jsonfile),'r') as json_data:
        a=json.load(json_data)
    a['extra_info']=['绝缘子污秽']
    a['train_info']=[]
    a['mode'] = '配'

    # if '10kV' in a['org_name']:
    #     a['extra_info'].append('10kV')
    # if '220kV' in a['org_name']:
    #     a['extra_info'].append('220kV')
    with open(os.path.join(dir, jsonfile), 'w') as json_data:
        json_data.write(json.dumps(a,indent=4,ensure_ascii=False))

# def get_all_MD5(JSON_DIR)-> list:                                    #获取out_json中所有json中的MD5值放入一个list
#     json_list = os.listdir(JSON_DIR)
#     all_MD5=[]
#     for json_file in json_list:
#         with open(os.path.join(JSON_DIR,json_file) ,'r') as data:
#             result = json.load(data)
#         all_MD5.append(result['MD5'])
#     return all_MD5
#
# print(get_all_MD5(dir))
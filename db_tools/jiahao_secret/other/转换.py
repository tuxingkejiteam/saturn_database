import json
import os
import shutil

from tqdm import tqdm

dir=r'E:\大棚\json'
dict={}
for json_file in os.listdir(dir):
    with open(os.path.join(dir,json_file),'r') as file:
        a = json.load(file)
    dict[a['org_name'][:-4]]=a['unique_code']

path=r"G:\大棚\已完成"
output=r'F:\大棚训练集'
for file in tqdm(os.listdir(path)):
    if file[-4:] in ['.jpg']:
        if file[:-4] not in dict:
            continue
        else:
            shutil.copy(os.path.join(path,file),os.path.join(output,dict[file[:-4]])+'.jpg' )
    if file[-4:] in ['.xml']:
        if file[:-4] not in dict:
            continue
        else:
            shutil.copy(os.path.join(path,file),os.path.join(output,dict[file[:-4]])+'.xml' )



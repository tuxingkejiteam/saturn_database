import os

dir=r'\\192.168.3.80\原始数据\图片数据管理库-2021-12-9\output_json'
file_names = os.listdir(dir)
for name in file_names:
    os.rename(os.path.join(dir,name),os.path.join(dir,(name.strip('unlabeled.json')).replace('_','')+'.json'))


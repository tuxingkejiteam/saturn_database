import os
path=r'F:\中山项目10.8\sjz'
from PIL import Image
from time import time
from tqdm import tqdm
T1=time()
for name in tqdm(os.listdir(path)):
    Imgpath=os.path.join(path,name)
    aaa=Image.open(Imgpath)
T2=time()

print((T2-T1)/len(os.listdir(path)))
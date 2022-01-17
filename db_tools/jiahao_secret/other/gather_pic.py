import os
import shutil
path=r'E:\陈卓'
new_path=r'C:\Users\zzc\Desktop\入库器\data1'

for root ,dirs,files in os.walk(path):
    for i in range(len(files)):
        if (files[i][-3:] == 'jpg') or (files[i][-3:] == 'png')or (files[i][-3:] == 'PNG') or (files[i][-3:] == 'JPG'):
            file_path = root +'/'+files[i]
            new_file_path = new_path+'/'+files[i]
            shutil.copy(file_path,new_file_path)



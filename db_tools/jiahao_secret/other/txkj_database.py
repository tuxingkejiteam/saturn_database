import os

import pymysql

#打开数据库连接，不指定数据库
from def_class import ImgLabel

conn = pymysql.connect(host='localhost',port=3306,user = "root",passwd = "chana961221",db = "mysql",charset='utf8')
cur=conn.cursor()#获取游标
json_dir=r'C:\Users\zzc\Desktop\output_json'
for json_file in os.listdir(json_dir):
    img_label = ImgLabel(os.path.join(json_dir,json_file))
    #另一种插入数据的方式，通过字符串传入值
    sql="insert into all_pic values(%s,%s,%s,%s,%s)"
    cur.execute(sql,(img_label.unique_code,img_label.W,img_label.H,img_label.class_code,img_label.MD5))

cur.close()
conn.commit()
conn.close()
print('sql执行成功')


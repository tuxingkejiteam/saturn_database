from db_tools.CRUD.MySQL_class import SaturnSQL


# 数据库初始化
mysql = SaturnSQL(host='192.168.3.101', user='root', password='root123', db_name='Saturn_Database')
# 假装有一个list
MD5_list = ['5a96a260a93dd004364be81589f10161', 'f341a333a4bb011aa8bf0f2fce395041',
            '0fbeb8aec7eb843811f9fce4462ce681', 'wojiushiyishinengbunengyouxindu1']*100
UC_list = mysql.get_uc_list(MD5_list)
print(UC_list)

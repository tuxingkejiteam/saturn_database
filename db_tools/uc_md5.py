from db_tools.CRUD.MySQL import MySQL

mysql = MySQL(password='fly1031')


def md5_in_db(md5: str):
    return mysql.R.md5_in_db(md5)


def get_uc_from_md5(json_path):
    pass


def insert_md5_uc_to_db(json_path):
    # 将json中必然含有的信息写入数据库（md5占坑）
    mysql.C.add_necessary_info(json_path)
    pass

# --------------------------

def get_uc(md5):
    pass
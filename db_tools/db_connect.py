from useful_funtion import get_small_img
from CRUD.MySQL import MySQL


if __name__ == "__main__":
    mysql = MySQL(password='fly1031')  # 启动数据库，并实例化数据库接口的方法类。
    mysql.R.all_label()
    # json_path = 'output_json/Clc0007.json'
    # mysql.create(json_path)
    # uc = 'Clc0007'
    # mysql.delete(uc)

    # label_list = ['cpb_ps']
    # mysql.read(label_list)
    pass

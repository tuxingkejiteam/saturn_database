from CRUD.MySQL_class import SaturnSQL
import os


def main():
    mysql = SaturnSQL(user='root', password='root123', host='192.168.3.101',
                      db_name='Saturn_Database_V1')  # 启动数据库，并实例化数据库接口的方法类。

    # # 清空数据库中所有表中的数据-----------------
    # a = mysql.clear_all_table()

    # # 根据json的路径列表写入数据库示例---------------------
    # data_dir = '功能测试用数据'
    # json_list = []  # 这里先计算一个json的路径列表。
    # for data in os.listdir(data_dir):
    #     if data.endswith('.json'):
    #         json_path = os.path.join(data_dir, data)
    #         json_list.append(json_path)
    #
    # label_list = ['Fnormal', 'zd_yt', 'no_mark', 'aaa']  # 定义一个标签列表，可为空，就是什么都传入，如果非空就按照列表导入。
    # result = mysql.add_json_to_db(json_list, label_list=label_list, confidence=True)

    # # md5_list申请UC_list示例----------------------------
    # MD5_list = ['5a96a260a93dd004364be81589f10161', 'f341a333a4bb011aa8bf0f2fce395041',
    #             '0fbeb8aec7eb843811f9fce4462ce681', 'wojiushiyishinengbunengyouxindu1']
    # UC_list = mysql.get_uc_list(MD5_list)
    # print(UC_list)


if __name__ == "__main__":
    main()

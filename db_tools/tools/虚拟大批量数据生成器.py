# 虚拟一堆md5和UC，在20个标签里，随机选10个标签作为UC的目标。
# 脚本独立运行，无任何外部函数依赖。
# 为目标标注表，插入大批量以及20个标签。
import pymysql
import datetime
from tqdm import tqdm
import hashlib

comparison_tabel = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9',
                    10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f', 16: 'g', 17: 'h', 18: 'i',
                    19: 'j', 20: 'k', 21: 'm', 22: 'n', 23: 'p', 24: 'q', 25: 'r', 26: 's', 27: 't',
                    28: 'u', 29: 'v', 30: 'w', 31: 'x', 32: 'y', 33: 'z'}
year_dict = {2019: 'A', 2020: 'B', 2021: 'C', 2022: 'D', 2023: 'E', 2024: 'F', 2025: 'G'}
database = pymysql.connect(host='192.168.3.101', user='root', password='root123', database='Saturn_Database_V1')


def first_3_letters() -> str:
    # 获取日期编码
    date = datetime.datetime.now()
    year = date.year
    month = date.month
    day = date.day
    letter_1 = year_dict[year]

    if day <= 15:
        letter_2 = comparison_tabel[month + 9]  # 上半月，月份从a开始
        letter_3 = comparison_tabel[day + 9]
    else:
        letter_2 = comparison_tabel[month + 9 + 12]  # 下半月，月份从m开始
        letter_3 = comparison_tabel[day - 15 + 9]

    return letter_1 + letter_2 + letter_3


def coding_rank(serial_number) -> str:
    # 获取序列，编码至四位。每位有34种选择。
    # 方法：整除取余法
    assert serial_number <= 1336336, "编码溢出，操作终止！"
    remainder_1 = serial_number % 34  # 取余数
    quotient_1 = serial_number // 34

    remainder_2 = quotient_1 % 34  # 取余数
    quotient_2 = quotient_1 // 34

    remainder_3 = quotient_2 % 34  # 取余数
    quotient_3 = quotient_2 // 34

    remainder_4 = quotient_3 % 34  # 取余数
    assert quotient_3 // 34 == 0, '编码溢出，操作终止！'
    letter_4 = comparison_tabel[remainder_4]
    letter_5 = comparison_tabel[remainder_3]
    letter_6 = comparison_tabel[remainder_2]
    letter_7 = comparison_tabel[remainder_1]

    return letter_4 + letter_5 + letter_6 + letter_7


def million_insert():
    uc_date = first_3_letters()
    count = 0
    for i in tqdm(range(1000000)):
        count += 1
        fake_file = str(i)
        fake_md5 = hashlib.md5(fake_file.encode()).hexdigest()
        uc = uc_date + coding_rank(i)

        sql_statement = "INSERT INTO `MD5对照表` (`MD5`, `UC`) VALUES('{}', '{}');".format(fake_md5, uc)
        database.cursor().execute(sql_statement)
        if count > 100000:
            database.commit()
            count = 0


if __name__ == "__main__":
    for j in tqdm(range(0, 10000, 1000000)):
        print(j)
        fake_file = str(j)
        fake_md5 = hashlib.md5(fake_file.encode()).hexdigest()
        sql_statement = "SELECT UC FROM `MD5对照表` WHERE `MD5`='{}';".format(fake_md5)
        database.cursor().execute(sql_statement)
        uc_info = database.cursor().fetchall()
        print(uc_info)
    pass

import json

comparison_tabel = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'a', 11: 'b',
                    12: 'c', 13: 'd', 14: 'e', 15: 'f', 16: 'g', 17: 'h', 18: 'i', 19: 'j', 20: 'k', 21: 'm',
                    22: 'n', 23: 'p', 24: 'q', 25: 'r', 26: 's', 27: 't', 28: 'u', 29: 'v', 30: 'w', 31: 'x',
                    32: 'y', 33: 'z'}
comparison_tabel1 = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10, 'b': 11,
                     'c': 12, 'd': 13, 'e': 14, 'f': 15, 'g': 16, 'h': 17, 'i': 18, 'j': 19, 'k': 20, 'm': 21,
                     'n': 22, 'p': 23, 'q': 24, 'r': 25, 's': 26, 't': 27, 'u': 28, 'v': 29, 'w': 30, 'x': 31,
                     'y': 32, 'z': 33}
year_dict = {2019: 'A', 2020: 'B', 2021: 'C', 2022: 'D', 2023: 'E', 2024: 'F', 2025: 'G'}
year_dict1 = {'A': 2019, 'B': 2020, 'C': 2021, 'D': 2022, 'E': 2023, 'F': 2024, 'G': 2025}


def coding_rank_back(serial_string) -> str:  # 将36进制返还会10进制来计数
    # 将36进制字符转换回十进制
    # 方法：整除取余法
    letter_1 = int(comparison_tabel1[serial_string[0]])
    letter_2 = int(comparison_tabel1[serial_string[1]])
    letter_3 = int(comparison_tabel1[serial_string[2]])
    letter_4 = int(comparison_tabel1[serial_string[3]])
    count = letter_1 * 34 * 34 * 34 + letter_2 * 34 * 34 + letter_3 * 34 + letter_4
    return str(count)


def already_in_database(unique_code) -> bool:
    with open('record.json') as data:
        record = json.load(data)
    key_as_date = unique_code[0:3]
    value_as_num = coding_rank_back(unique_code[-4:])
    if int(record[key_as_date]) >= int(value_as_num):
        return True
    else:
        return False

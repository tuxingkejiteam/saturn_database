import random
def get_random_sum(total, num):
    random_list = []
    random_value = total
    for i in range(num):
        random_value = total - sum(random_list) - num + i + 1
        value = float(format(random.uniform(0, random_value), f'.{2}f'))
        random_list.append(value)
    random_list.append(float(format(total - sum(random_list), f'.{2}f')))
    return random_list

print(get_random_sum(3.58,30))
from read_files import *
from func_s import write_csv_r


temp_list =[]

for item in main_list:
    str_num = main_list.index(item)
    col_a = item[0]
    if type(col_a) != int and 'ДО/УРО' in col_a:
        print(col_a)
        if col_a not in dict_sroki:
            temp_list.append([col_a])

write_csv_r(temp_list, 'dog_bez_srokov')
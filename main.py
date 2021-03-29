from read_files import *
from func_s import make_dicts_from_temp_list, make_res_dir, make_res_list, write_csv_r


srok_postavki = 0
temp_list = []
result_list = make_res_list()
tmp_dir = 'head'
temp_item = '0'

for item in main_list:
    str_num = main_list.index(item)
    col_a = item[0]
    if type(col_a) != int and 'ДО/УРО' in col_a:
        print(col_a)
        y = make_dicts_from_temp_list(temp_list, srok_postavki, tmp_dir, temp_item[0])
        if len(y) > 1:
            result_list.append(temp_item)
            for yrow in y:
                result_list.append(yrow)
        result_list.append([item[0], item[1]])
        tmp_dir = col_a.split('-')[1][:4]
        make_res_dir(f'./tmpr/{tmp_dir}')
        srok_postavki = dict_sroki[col_a]
        button = True
    elif type(col_a) == int or len(col_a) < 5:
        if button == False:
            y = make_dicts_from_temp_list(temp_list, srok_postavki, tmp_dir, temp_item[0])
            if len(y) > 1:
                result_list.append(temp_item)
                for yrow in y:
                    result_list.append(yrow)
        else:
            button = False
        temp_list = []
        temp_item = [item[0], item[1]]
    else:
        temp_list.append(item)

y = make_dicts_from_temp_list(temp_list, srok_postavki, tmp_dir, temp_item[0])
if len(y) > 1:
    result_list.append(temp_item)
for yrow in y:
    result_list.append(yrow)
write_csv_r(result_list, 'result')
print('Finish')
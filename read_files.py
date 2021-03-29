import csv
from datetime import datetime, date


__all__ = ['main_list', 'holidays', 'dict_sroki', 'postavka_col_names', 'current_date',
           'svodnaya_col_names', 'park_col_names']

FILES_DIR = './files/'

def read_csv_list(file_name):
    with open(file_name, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data


# Data File
file_main = FILES_DIR + '21_15_03_21.csv'
main_list = read_csv_list(file_main)

# Holidays File
file_holidays = FILES_DIR + 'holidays.csv'
holidays_f = read_csv_list(file_holidays)

# Sroki Dogovorov File
file_sroki = FILES_DIR + '21dogovor_sroki.csv'
dogovor_sroki_f = read_csv_list(file_sroki)

column_a = 'dog_poznum_doc'
column_b = 'dogname_pozname'
column_c = 'supplier_pozhar'

postavka_col_names = {}
svodnaya_col_names = {}
park_col_names = {}
for x in main_list[0]:
    if 'pos' in x:
        postavka_col_names[x] = main_list[0].index(x)
    elif 'raz' in x:
        svodnaya_col_names[x] = main_list[0].index(x)

foo = 3
for x in postavka_col_names:
    key = x[4:]
    park_col_names[key] = [foo]
    foo += 1

# Make Holidays list. Получаем из файла и запихиваем в список.
holidays = []
for item_day in holidays_f:
    holiday = datetime.strptime(item_day[0], '%m/%d/%Y').date()
    holidays.append(holiday)

# Sroki dogovora. Получаем из файла и запихиваем в словарь.
dict_sroki = {}
for item in dogovor_sroki_f:
    dict_sroki[item[0]] = int(item[1])

current_date = date.today()

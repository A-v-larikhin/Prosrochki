from read_files import *
from datetime import datetime
from data_holidays import srok_postavki_fact
import os
import csv


def make_res_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def write_csv(data, dir, file):
    '''
    Функция для записи исходного массива временных данных в файл для анализа при поиске багов
    (путь /data_in/номер договора/номер позиции.csv)
    :param data: temp list from datafile
    :param dir: contract number
    :param file: position number
    :return: nothing, just write file
    '''
    make_res_dir(f'./data_in/{dir}')
    with open(f'./data_in/{dir}/{file}.csv', 'w') as file:
        writer = csv.writer(file)
        for i in data:
            writer.writerow(i)


def write_csv_r(data, file):
    '''
    Функция для записи расчитанных значений в итоговый файл.
    :param data: result list
    :param file: filename
    :return: nothing, just write file
    '''
    #encoding = 'cp1251'
    with open(f'./result/{file}.csv', 'w') as file:
        writer = csv.writer(file)
        for i in data:
            writer.writerow(i)


def make_tmp_list():
    tmp_list = []
    for j in range(len(park_col_names) + 3):
        tmp_list.append('')
    return tmp_list


def make_temp_list():
    list = []
    for i in range(len(make_res_list()[0])):
        list.append('')
    return list


def make_res_list():
    res_list = [['dog_poznum_doc', 'dogname_pozname', 'supplier_pozhar']]
    for i in park_col_names:
        res_list[0].append(i)
    return res_list


def make_clear_dicts():
    svodnaya_dict = {}
    for i in svodnaya_col_names:
        svodnaya_dict[i[4:]] = []
    postavka_dict = {}
    for i in postavka_col_names:
        postavka_dict[i[4:]] = []
    korrektirovka_dict = {}
    for i in postavka_col_names:
        korrektirovka_dict[i[4:]] = []
    return svodnaya_dict, postavka_dict, korrektirovka_dict


def make_dicts_from_temp_list(temp_list, srok_postavki, dir, file):
    '''
    - Создаем словари {ключи - парки (ap1), значения - списки [документ, дата, кол-во...]}
    - Запускаем функцию poisk_v_dictax для поиска просрочек
    - Запускаем функцию make_list_from_dict для перекладывания списков в словари
    :param temp_list: список документов (исходные строки) по одной позиции спецификации
    :param srok_postavki: и так понятно
    :param dir: папка для сохранения исходных данных (номер договора) АТАВИЗМ
    :param file: номер позиции спецификации АТАВИЗМ
    :return: список просрочек
    '''
    svodnaya_dict, postavka_dict, korrektirovka_dict = make_clear_dicts()
 #   write_csv(temp_list, dir, file)    # Для проверки можно писать исходные данные в файл
                                        #   (путь - /data_in/номер_договора/номер_позиции.csv)
    for row in temp_list:
        if 'Сводная' in row[0]:
            data_sv = datetime.strptime(row[0].split()[6], '%d.%m.%Y').date()
            for column in svodnaya_col_names:
                # svodnaya_col_names - словарь {raz_ap1: номер столбца}
                col = svodnaya_col_names[column]
                if row[col] != '':
                    sv_value = int(row[col])
                    # создаем временный лист для сводных
                    # [Название документа, дата, кол-во, 'не закрыта Х дней']
                    sv_temp_list = [row[0], data_sv, sv_value, f'not closed: {srok_postavki_fact(current_date, data_sv)} days']
                    # добавляем список в словарь по имени парка {ap1: [[],[]]}
                    svodnaya_dict[column[4:]].append(sv_temp_list)
        elif 'Приобретение' in row[0]:
            data_pr = datetime.strptime(row[0].split()[6], '%d.%m.%Y').date()
            for column in postavka_col_names:
                # postavka_col_names - словарь {pos_ap1: номер столбца}
                col = postavka_col_names[column]
                if row[col] != '':
                    pr_value = int(row[col])
                    # создаем временный лист для приобретений
                    # [Название документа, дата, кол-во]
                    pr_temp_list = [row[0], data_pr, pr_value]
                    # добавляем список в словарь по имени парка {ap1: [[],[]]}
                    postavka_dict[column[4:]].append(pr_temp_list)
        elif 'Корректировка' in row[0]:
            data_pr = datetime.strptime(row[0].split()[7], '%d.%m.%Y').date()
            for column in svodnaya_col_names:
                col = svodnaya_col_names[column]
                if row[col] != '':
                    pr_value = int(row[col])
                    # создаем временный лист для корректировок
                    # [Название документа, дата, кол-во]
                    pr_temp_list = [row[0], data_pr, pr_value]
                    # добавляем список в словарь ПОСТАВОК по имени парка {ap1: [[],[]]}
                    postavka_dict[column[4:]].append(pr_temp_list)
    x = poisk_v_dictax(svodnaya_dict, postavka_dict, srok_postavki)
    some_list = make_list_from_dict(x)
    return some_list


def poisk_v_dictax(svodnaya_dict, postavka_dict, srok_postavki):
    for ap in postavka_dict:
        post_perem = 0
        temp_list_postavka = postavka_dict[ap]
        for item in temp_list_postavka:
            while True:
                temp_list_svodnaya = svodnaya_dict[ap]
                if len(temp_list_svodnaya) < 1:
                    temp_list_svodnaya.append(['Peace Death', datetime.strptime('1/1/2020', '%m/%d/%Y').date(), -10000, 0])
                if item[2] + temp_list_svodnaya[0][2] == 0:
                    srok = srok_postavki_fact(item[1], temp_list_svodnaya[0][1])
                    if srok > srok_postavki:
                        temp_list_svodnaya[0][3] = srok - srok_postavki
                        temp_list_svodnaya.append(temp_list_svodnaya[0])
                    temp_list_svodnaya.pop(0)
                    svodnaya_dict[ap] = temp_list_svodnaya
                    break
                elif item[2] + temp_list_svodnaya[0][2] < 0:
                    temp_list_svodnaya[0][2] += item[2] + post_perem
                    svodnaya_dict[ap] = temp_list_svodnaya
                    break
                elif item[2] + temp_list_svodnaya[0][2] > 0:
                    srok = srok_postavki_fact(item[1], temp_list_svodnaya[0][1])
                    item[2] = temp_list_svodnaya[0][2] + item[2]
                    if srok > srok_postavki:
                        temp_list_svodnaya[0][3] = srok - srok_postavki
                        temp_list_svodnaya.append(temp_list_svodnaya[0])
                    temp_list_svodnaya.pop(0)
                    svodnaya_dict[ap] = temp_list_svodnaya
    return svodnaya_dict


def make_list_from_dict(some_dict):
    n_list = make_temp_list()
    some_dict = some_dict
    x = 0
    new_list = [[]]
    c = 3
    for i in some_dict:
        for j in some_dict[i]:
            n_list[0] = j[0]
            n_list[c] = j[3]
            new_list.append(n_list)
            n_list = make_temp_list()
        c += 1
    return new_list
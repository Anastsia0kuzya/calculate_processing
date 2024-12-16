import linecache
import re
import os
import csv
import pandas
import atomic_number as at
atomic_number = at.atomic_number
from itertools import islice
def energy_ORCA(orca_opt_nohup):
# TODO:выводит список энергий каждого большого и маленького шага
    total_energy = 'Total Energy'
    with open(orca_opt_nohup) as file:
        list_total_energy = []
        for index, line in enumerate(file):
            if total_energy in line:
                index -= 1
                interection = linecache.getline(orca_opt_nohup, index).strip().replace(' ', '').replace('!', '')#форматирую интерекшн
                list_total_energy.append(interection)
                list_total_energy.append(line.replace('   Total Energy        :   ', '').replace( 'Eh\n', '').replace(' ', ''))
    #Определяют границы обрезки
    key_1 = '----------------' #с какого символа удаляем
    idx_1=[x[0] for x in enumerate(list_total_energy) if x[1] == key_1] #список первого ключа
    key_2 = 'ITERATION0' #до какого удаляем
    idx_2=[x[0] for x in enumerate(list_total_energy) if x[1] == key_2] #список второго ключа
    idx_2.pop(0) #удаляем начальный, тк он не учавсвует в удалении
    for i in range(len(idx_2)):
        del list_total_energy[idx_1[i]:idx_2[i]]
    idx_1=[x[0] for x in enumerate(list_total_energy) if x[1] == key_1]
    del list_total_energy[idx_1[-1]:] #убераем лишние строки

    '''выдает списки с подсписками всех интерекшенов'''
    for i in range(1, len(list_total_energy), 2):
        list_total_energy[i] = float(list_total_energy[i])
    l_first = [] #первый список
    for i in range(0, len(list_total_energy)//2, 2):
        l_first.append([list_total_energy[i], list_total_energy[i+1]])
    l_end = [] #конечный список
    for i in range(len(list_total_energy)//2 + 1, len(list_total_energy) - 1, 2):
        l_end.append([list_total_energy[i], list_total_energy[i+1]]) #разбили последний и первый
    list_total_energy.clear()
    start_line_energy = [] #Список сокращенных интеракшенов, приводим к общему виду
    with open(orca_opt_nohup) as file:
        for index, k in enumerate(file):
            if 'ITER      Energy       Delta-E        Grad      Rot      Max-DP    RMS-DP' in k:
                start_line_energy.append(index)
    with open(orca_opt_nohup) as file:
        lines = file.readlines()
        energy = []
        for i in range(len(start_line_energy)):
            for line in lines[start_line_energy[i]+1:]:
                if line.strip() == '':  # Проверяем на пустую строку
                        break
                if 'Restarting incremental' not in line:
                    line = line.strip().split(' ')
                    line = ' '.join(line[:3])
                    index = line.find(' ')
                    while line[0].isdigit():
                        line = 'ITERATION' + str(int(line[:3]) - 1) + line[index + 1:]
                        energy.append(line)
    l_intermediate = []
    for i in energy:
        l_intermediate.append(i.split())
    for i in range(len(l_intermediate)):
        l_intermediate[i][1] = float(l_intermediate[i][1])
    list_total_energy = l_first + l_intermediate + l_end
    del l_first, l_end, l_intermediate
    # получили один огромный список интерекшенов
    list_total_energy_def = []
    current_list = []
    for i in range(len(list_total_energy)):
        if list_total_energy[i][0] == "ITERATION0":
            if current_list:
                list_total_energy_def.append(current_list)
            current_list = [list_total_energy[i]]
        else:
            current_list.append(list_total_energy[i])
    if current_list:
        list_total_energy_def.append(current_list)
    for i in list_total_energy_def:
        for k in range(len(i)):
            i[k] = i[k][1]
    del current_list, list_total_energy
    final_list_energy = [] #вытаскиваем последние энергии
    for i in list_total_energy_def:
        if i is not str:
            final_list_energy.append(i[-1])
    return list_total_energy_def



def symbol_to_atomic(atom):
    #TODO: преобразует симолы эллементов в атомные нормера (подхидт только для тройного списка, где элемент на 0 позиции)
    if atom in atomic_number:
        number = atomic_number[atom][0]
    return number


def coords_ORCA(orca_opt_nohup):
    #TODO: выводит список координат молекулы по каджому большому шагу
    '''Список списков координат'''
    start_line_coord = []
    end_line_coord = []
    total_time = ''
    with open(orca_opt_nohup) as file:
        for index, k in enumerate(file):
            if 'CARTESIAN COORDINATES (ANGSTROEM)' in k:
                start_line_coord.append(index)
            if 'CARTESIAN COORDINATES (A.U.)' in k:
                end_line_coord.append(index)
            if 'TOTAL RUN TIME: ' in k:
                total_time = k[16:-1]
    with open(orca_opt_nohup, 'r') as file:
        lines = file.readlines()
        coord = []
        #Считываем нужные строки (корректируем номера строк для индексации с 0)
        for i in range(len(start_line_coord)):
            for line_coord in lines[start_line_coord[i]+3:end_line_coord[i]]:
                coord.append(line_coord)
    list_CARTESIAN_COORDINATES = []
    current_sublist = []
    input_list = coord
    value = '----------------------------\n'
    for item in input_list:
        if item == value:
            if current_sublist:  # Если текущий подсписок не пуст, добавляем его в результат
                del current_sublist[-1]
                list_CARTESIAN_COORDINATES.append(current_sublist)

                current_sublist = []  # Обнуляем текущий подсписок
        else:
            current_sublist.append(item)
    if current_sublist: # Добавляем последний подсписок, если он не пуст
        list_CARTESIAN_COORDINATES.append(current_sublist)
    #разбиваем координаты на списки
    for i in range(len(list_CARTESIAN_COORDINATES)):
        list_CARTESIAN_COORDINATES[i] = [s.split() for s in list_CARTESIAN_COORDINATES[i]]
    for s in list_CARTESIAN_COORDINATES:
        for k in s:
            k[1] = float(k[1])
            k[2] = float(k[2])
            k[3] = float(k[3])
    if list_CARTESIAN_COORDINATES[0][0][0] is not int:
        for i in list_CARTESIAN_COORDINATES:
            for k in i:
                k[0] = symbol_to_atomic(k[0])
    final_coord = list_CARTESIAN_COORDINATES[5]
    return list_CARTESIAN_COORDINATES, total_time, final_coord

def final_energy_ORCA(orca_opt_nohup):
    final_total_energy_val = [] #список значений для последнего списка
    all_energy = []
    with open(orca_opt_nohup) as file:
        for k in file:
            if 'FINAL SINGLE POINT ENERGY ' in k:
                final_total_energy_val.append(k)
            if "Electronic energy" in k:
                all_energy.append(k.strip())
            if "Zero point energy " in k:
                all_energy.append(k.strip())
            if "Total Enthalpy " in k:
                all_energy.append(k.strip())
            if "Final entropy term" in k:
                all_energy.append(k.strip())
            if "Final Gibbs free energy" in k:
                all_energy.append(k.strip())
    final_total_energy = float(final_total_energy_val[-1][30:])
    final_total_energy_val.clear()
    if len(all_energy) == 5:
        k = []
        for i in all_energy:
            parts = i.split()
            for part in parts:
                    k.append(part)
        all_final_energy = [float(k[3]), float(k[9]), float(k[16]), float(k[22]), float(k[31])]
        return final_total_energy, all_final_energy
    else:
        return final_total_energy, all_energy


def dict_ORCA(orca_opt_nohup):
    # TODO: выводит словарь с ионными шагами, большими словами, финальным временем, финальным результатом
    list_total_energy_def = energy_ORCA(orca_opt_nohup)[0], energy_ORCA(orca_opt_nohup)[1]
    list_CARTESIAN_COORDINATES, total_time, final_coord = coords_ORCA(orca_opt_nohup)[0], coords_ORCA(orca_opt_nohup)[1], coords_ORCA(orca_opt_nohup)[2]
    final_energy = final_energy_ORCA(orca_opt_nohup)[0]
    all_final_energy = final_energy_ORCA(orca_opt_nohup)[1]
    '''словари'''
    STEP = {} #один большой словарь, где содержатся все ионные шаги
    step_range = []
    for i in range(len(list_total_energy_def)):
        step_range.append('STEP' + str(i))
    for key, value_1, value_2 in zip(step_range, list_total_energy_def, list_CARTESIAN_COORDINATES):
        STEP[key] = {
            "energy": value_1,
            "coords": value_2
        }
    #добавляем финальную энергию в подсовари
    for key, subdict in STEP.items():
        first_key = list(subdict.keys())[0]
        subdict['final_energy'] = subdict[first_key][-1]
    #добавляем финальный подсловарь
    if len(all_final_energy) == 5:
        final_miny_dict = {
            "total_time": total_time,
            "final_energy": final_energy,
            "electronic_energy": all_final_energy[0],
            "zero_point_energy": all_final_energy[1],
            "final_enthalpy": all_final_energy[2],
            "final_entropy": all_final_energy[3],
            "final_gibbs_free_energy": all_final_energy[4]
        }
    else:
        final_miny_dict = {
        "total_time": total_time,
        "final_energy": final_energy,
        }
    STEP['final_data'] = final_miny_dict
    #print(STEP)
    print("ORCA STOP")

    return STEP


def energy_GAUSSIAN(guassian_opt_nohup):
#TODO: выводит список энергий по каждому шагу
    with open(guassian_opt_nohup) as file:
        list_total_energy = []
        for line in file:
            if ' Iteration ' in line and 'EE' in line:
                k = line.split()[0] + line.split()[1] + ' ' + line.split()[3]
                list_total_energy.append(k)

    '''Делаем список с подсписками интерекшенов каждого шага'''
    list_total_energy_fin = []
    current_subscription = []
    for string in list_total_energy:
        # Проверяем, начинается ли строка с определенного значения
        if string.startswith("Iteration1 "):
            if current_subscription:
                list_total_energy_fin.append(current_subscription)
                current_subscription = []
            current_subscription.append(string)
        else:
            current_subscription.append(string)
    if current_subscription:
        list_total_energy_fin.append(current_subscription)
    del current_subscription, list_total_energy
    for i in list_total_energy_fin:
        for t in range(len(i)):
            val = float(i[t].split()[1])
            i[t] = val
    final_energy = list_total_energy_fin[-1][-1]
    return list_total_energy_fin, final_energy

def coords_GAUSSIAN(guassian_opt_nohup):
    start_line_coord = []
    end_line_coord = []
    '''Вытаскиваем из файла координаты'''
    with open(guassian_opt_nohup) as file:
        for index, k in enumerate(file):
            if 'Standard orientation:' in k:
                start_line_coord.append(index)
            if ' Rotational constants ' in k:
                end_line_coord.append(index)
            if ' Job cpu time:  ' in k:
                total_time_job = k[19:60]
    with open(guassian_opt_nohup, 'r') as file:
        lines = file.readlines()
        coord = []
        # Считываем нужные строки (корректируем номера строк для индексации с 0)
        for i in range(len(start_line_coord)):
            for line_coord in lines[start_line_coord[i] + 5:end_line_coord[i]]:
                coord.append(line_coord)

    '''Разделяем координаты на списки для каждого шага'''
    list_COORDINATES = []
    current_sublist = []
    value = ' ---------------------------------------------------------------------\n'
    for item in coord:
        if item != value:
            current_sublist.append(item)
        else:
            list_COORDINATES.append(current_sublist)
            current_sublist = []

    '''Разбиваем на подсписки, содержащие X, Y, Z'''
    for i in list_COORDINATES:
        for k in range(len(i)):
            i[k] = i[k].split()[1:2] + i[k].split()[3:]
    #делаем координаты не строками
    for i in list_COORDINATES:
        for k in range(len(i)):
            i[k][0] = int(i[k][0])
            i[k][1] = float(i[k][1])
            i[k][2] = float(i[k][2])
            i[k][3] = float(i[k][3])
    final_coord = list_COORDINATES[-1]
    return list_COORDINATES, total_time_job, final_coord

def dict_GAUSSIAM(guassian_opt_nohup):
    STEP = {}  # один большой словарь, где содержатся все ионные шаги
    step_range = []
    list_energy= energy_GAUSSIAN(guassian_opt_nohup)[0]
    final_energy = energy_GAUSSIAN(guassian_opt_nohup)[1]
    list_coord = coords_GAUSSIAN(guassian_opt_nohup)[0]
    total_time = coords_GAUSSIAN(guassian_opt_nohup)[1]
    for i in range(len(list_energy)):
        step_range.append('STEP' + str(i))
    for key, value_1, value_2 in zip(step_range, list_energy, list_coord):
        STEP[key] = {
            "energy": value_1,
            "coords": value_2
        }
    final_miny_dict = {
        "final_energy": final_energy,
        "total_time": total_time,
        }
    STEP['final_data'] = final_miny_dict
    #print(STEP)
    print("GAUSSIAN STOP")
    return STEP


def energy_XTB(xtb_opt_nohub):
    # TODO: выводит список энергий по каждому шагу + финальная энергия
    list_total_energy = []
    final_energy = ''
    enerdy_for_coord = ''
    with open(xtb_opt_nohub, 'r', encoding='utf-8') as file:
        start_reading = False
        for line in file:
            if "TOTAL ENERGY" in line:
                final_energy = float(line.strip()[27:45])
                enerdy_for_coord = float(line.strip()[27:39])
            if ".............................. CYCLE  " in line:
                start_reading = True
                continue
            if ' * total energy  :' not in line:
                continue
            if start_reading:
                list_total_energy.append(float(line.strip()[19:32]))
    return list_total_energy, final_energy, enerdy_for_coord

def coord_XTB(xtb_opt_nohub):
    list_COORDINATES = []
    start = False
    time = False
    with open(xtb_opt_nohub, 'r', encoding='utf-8') as file:
        for line in file:
            if "total:" in line:
                time = True
                continue
            if time:
                if " *  cpu-time:" in line:
                    cpu_time = line.strip()[17:]
            if "ratio c/w: " in line:
                time = False
            if "final structure:" in line:
                start = True
                continue
            if "END" in line:
                start = False
            if start:
                list_COORDINATES.append(line.strip()[31:84])
    list_COORDINATES.pop(0)
    list_CARTESIAN = []
    for r in list_COORDINATES:
        if (len(r) != 0):
            list_CARTESIAN.append(r)
    list_CARTESIAN_COORDINATES =  [s.split() for s in list_CARTESIAN]
    for i in list_CARTESIAN_COORDINATES:
        del i[3:5]
    """Перетаскивает элемент атом в начало списка и делает числом координаты"""
    for i in list_CARTESIAN_COORDINATES:
        atom = i.pop()
        i.insert(0, atom)
    for i in list_CARTESIAN_COORDINATES:
        i[0] = symbol_to_atomic(i[0])
        for k in range(1, len(i)):
            i[k] = float(i[k])
    return list_CARTESIAN_COORDINATES, cpu_time

def dict_XTB(xtb_opt_nohub):
    STEP = {}  # один большой словарь, где содержатся все ионные шаги
    step_range = []
    list_energy = energy_XTB(xtb_opt_nohub)[0]
    final_energy = energy_XTB(xtb_opt_nohub)[1]
    energy_for_coord = energy_XTB(xtb_opt_nohub)[2]
    list_final_coord = coord_XTB(xtb_opt_nohub)[0]
    final_time = coord_XTB(xtb_opt_nohub)[1]
    for i in range(len(list_energy)):
        step_range.append('STEP' + str(i))
    for key, value_1 in zip(step_range, list_energy):
        if value_1 == energy_for_coord:
            STEP[key] = {
                "energy": value_1,
                "coords": list_final_coord
            }
        else:
            STEP[key] = {
                "energy": value_1,
                "coords": 0
            }
    final_miny_dict = {
        "final_energy": final_energy,
        "total_time": final_time
    }
    STEP['final_data'] = final_miny_dict
    #print(STEP)
    print("XTB STOP")
    return STEP




# Функция для записи в CSV
def write_to_csv(data, filename):
    # Получаем уникальные названия для столбцов
    column_names = set()
    for entry in data:
        for step_key in entry.keys():
            if 'step' in step_key:
                for energy_item in entry[step_key]['energy']:
                    column_names.add(energy_item[0])

    # Добавляем дополнительные ключи
    column_names.update(['final_energy', 'total_time'])

    # Сортируем столбцы
    column_names = sorted(column_names)

    # Запись в CSV
    with open(filename, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=column_names)
        writer.writeheader()

        for entry in data:
            row = {key: None for key in column_names}
            # Заполняем строки данными
            for step_key in entry.keys():
                if 'step' in step_key:
                    energy_list = entry[step_key]['energy']
                    for energy_item in energy_list:
                        row[energy_item[0]] = energy_item[1]
                    row['final_energy'] = entry[step_key]['final_energy']

            # Заполняем финальные данные
            row['final_energy'] = entry['final_data']['final_energy']
            row['total_time'] = entry['final_data']['total_time']

            writer.writerow(row)





def main(file_list: list):
    result_process = []
    for file_open in file_list:
        with open(file_open, 'r') as file:
            for line in file:
                if 'O   R   C   A' in line:
                    #result_process.append("ORCA:")
                    result_process.append(dict_ORCA(file_open))
                if 'Entering Gaussian System' in line:
                    #result_process.append("GAUSSIAN:")
                    result_process.append(dict_GAUSSIAM(file_open))
                if '        x T B        ' in line:
                    #result_process.append("XTB:")
                    result_process.append(dict_XTB(file_open))

    print(result_process)
    write_to_csv(result_process, 'results.csv')

    return result_process


if __name__ == '__main__':
    orca_opt_nohup = '/Users/anastasiakuznetsova/Documents/НИР/calculate_processing/Elsulfaverin/orca/opt/1/1.out'
    guassian_opt_nohup = '/Users/anastasiakuznetsova/Documents/НИР/calculate_processing/2.log'
    xtb_opt_nohup = '/Users/anastasiakuznetsova/Documents/НИР/calculate_processing/6LUD.out'
    file_list = [orca_opt_nohup, guassian_opt_nohup, xtb_opt_nohup]
    main(file_list)














































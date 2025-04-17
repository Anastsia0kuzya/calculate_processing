import linecache
import re
import os
import csv
import pandas
import math
import atomic_number as at
atomic_number = at.atomic_number
from itertools import islice

def rmsd(final_energy_list, final_energy):
# TODO: находит среднеквадратичное отклонение
    rdsm = 0
    for i in final_energy_list:
        rdsm += (i - final_energy)**2
    rdsm = math.sqrt(rdsm/len(final_energy_list))
    return rdsm
def various(file_path):
    with open(file_path) as file:
        version = 0
        for l in file:
            if 'Program Version 5' in l:
                version = 5
            elif 'Program Version 6' in l:
                version = 6
    return version



def energy_ORCA(orca_opt_nohup):
# TODO:выводит список энергий каждого большого и маленького шага
    total_energy = 'Total Energy'
    list_total_energy = []
    with open(orca_opt_nohup) as file:

        if various(orca_opt_nohup) == 5:
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

        if various(orca_opt_nohup) == 6:
            pr_list = []
            #with open(orca_opt_nohup, 'r', encoding='utf-8') as file:
            start_s = []
            end_s = []
            start_symbol = '----------------------------------------D-I-I-S--------------------------------------------'
            end_symbol = 'SCF CONVERGED AFTER'
            for index, line in enumerate(file):
                if start_symbol in line:
                    start_s.append(index)
                elif end_symbol in line:
                    end_s.append(index)
            with open(orca_opt_nohup, 'r') as file:
                lines = file.readlines()
            for i in range(len(start_s)):
                start_index = start_s[i]
                end_index = end_s[i]
                pr_list.append(lines[start_index + 4:end_index - 3])
            for i in pr_list:
                for j in i:
                    # Разделяем строку на части
                    parts = j.split()

                    for p in range(len(parts)):
                        try:
                            # Пробуем преобразовать строку в число
                            number = int(parts[p])

                            # Проверяем, является ли число натуральным
                            if number > 0 and number.is_integer():
                                found_natural = True
                                list_total_energy.append('ITERATION'+str(int(parts[p]) - 1))  # Добавляем натуральное число
                                list_total_energy.append(parts[p+1])

                        except ValueError:
                            continue  # Игнорируем строки, которые не могут быть преобразованы в число

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
    list_energy = list_total_energy_def[0], list_total_energy_def[1]
    list_final_steps = []
    for f in list_energy:
        list_final_steps.append(f[-1])
    return list_total_energy_def, list_final_steps



def symbol_to_atomic(atom):
    #TODO: преобразует симолы эллементов в атомные нормера (подхидт только для тройного списка, где элемент на 0 позиции)
    if atom in atomic_number:
        number = atomic_number[atom][0]
    return number


def coords_ORCA(orca_opt_nohup):
    #TODO: выводит список координат молекулы по каджому большому шагу, время и финальные координаты
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
    list_total_energy_def = energy_ORCA(orca_opt_nohup)[0][0], energy_ORCA(orca_opt_nohup)[0][1]
    list_final_energy_steps = energy_ORCA(orca_opt_nohup)[1]
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
        "final_energy": final_energy,
        "total_time": total_time,
        }
    STEP['final_data'] = final_miny_dict
    rsdm_orca = rmsd(list_final_energy_steps, final_energy)
    STEP['standard deviation'] = rsdm_orca
    STEP['name programm'] = 'ORCA'
    #print(STEP)
    print("ORCA DONE")
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
    list_final_steps = []
    for i in list_total_energy_fin:
        list_final_steps.append(i[-1])
    return list_total_energy_fin, final_energy, list_final_steps

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
    list_final_for_step_energy = energy_GAUSSIAN(guassian_opt_nohup)[2]
    #print(list_final_for_step_energy)
    final_energy = energy_GAUSSIAN(guassian_opt_nohup)[1]
    list_coord = coords_GAUSSIAN(guassian_opt_nohup)[0]
    total_time = coords_GAUSSIAN(guassian_opt_nohup)[1]
    for i in range(len(list_energy)):
        step_range.append('STEP' + str(i))
    for key, value_1, value_2, value_3 in zip(step_range, list_energy, list_coord, list_final_for_step_energy):
        STEP[key] = {
            "energy": value_1,
            "coords": value_2,
            "final_energy": value_3
        }
    final_miny_dict = {
        "final_energy": final_energy,
        "total_time": total_time,
        }
    STEP['final_data'] = final_miny_dict
    rmsd_gaussian = rmsd(list_final_for_step_energy, final_energy)
    STEP['standard deviation'] = rmsd_gaussian
    STEP['name programm'] = 'GAUSSIAN'
    #print(STEP)
    print("GAUSSIAN DONE")
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
                "coords": list_final_coord,
                "final_energy": value_1,
            }
        else:
            STEP[key] = {
                "coords": 0,
                "final_energy": value_1,
            }
    final_miny_dict = {
        "final_coord": list_final_coord,
        "final_energy": final_energy,
        "total_time": final_time,

    }
    STEP['final_data'] = final_miny_dict
    rmsd_xtb = rmsd(list_energy, final_energy)
    STEP['standard deviation'] = rmsd_xtb
    STEP['name programm'] = 'XTB'
    #print(STEP)
    print("XTB DONE")
    return STEP


def list_for_csv(data):
    data_for_csv = [['Stage', 'Energy', 'Coords', 'Final energy', 'Total Time', 'standard deviation', 'name programm']] #ЗАГОЛОВКИ

    for key in data:
        if "STEP" in key:
            pr_data_s = []
            pr_data_s.append(key)
            for s in data[key]:
                if data['name programm'] == 'XTB' and data[key][s] == 0:
                    pr_data_s.append('-')
                else:
                    pr_data_s.append(data[key][s])

            pr_data_s.append('-')
            pr_data_s.append('-')
            if data['name programm'] == 'ORCA':
                pr_data_s.append('ORCA')
            elif data['name programm'] == 'GAUSSIAN':
                pr_data_s.append('GAUSSIAN')
            elif data['name programm'] == 'XTB':
                pr_data_s = pr_data_s[:1] + ['-'] + pr_data_s[1:]
                pr_data_s.append('XTB')
            data_for_csv.append(pr_data_s)

        elif key == "final_data":
            pr_data_f = ["FINAL", "-"]
            for f in data[key]:
                pr_data_f.append(data[key][f])
            pr_data_f.append(data['standard deviation'])
            if data['name programm'] == 'ORCA' or data['name programm'] == 'GAUSSIAN':
                a = []
                a.append(pr_data_s[-5])
                pr_data_f = pr_data_f[:2] + a + pr_data_f[2:]
                if data['name programm'] == 'ORCA':
                    pr_data_f.append('ORCA')
                elif data['name programm'] == 'GAUSSIAN':
                    pr_data_f.append('GAUSSIAN')
            elif data['name programm'] == 'XTB':
                pr_data_f.append('XTB')
            data_for_csv.append(pr_data_f)
    return data_for_csv

def write_csv(data_for_csv, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data_for_csv) # Записываем данные в файл

def write_sort_csv(data):
    final_data_for_csv = [['Stage', 'Coords', 'Final energy', 'Total Time', 'Standard deviation', 'Name programm']]
    i = 1
    for step in data:
        data_for_csv = list_for_csv(step)
        p = []
        p.append(data_for_csv[-1][0])
        p = p + data_for_csv[-1][2:]
        final_data_for_csv.append(p)
        if step['name programm'] == 'ORCA':
            write_csv(data_for_csv, 'orca'+str(i)+'.csv')
            print("Данные успешно записаны в data.csv для ORCA")
        elif step['name programm'] == 'GAUSSIAN':
            write_csv(data_for_csv, 'gaussian'+str(i)+'.csv')
            print("Данные успешно записаны в data.csv для GAUSSIAN")
        elif step['name programm'] == 'XTB':
            write_csv(data_for_csv, 'xtb'+str(i)+'.csv')
            print("Данные успешно записаны в data.csv для XTB")
        i+=1
    write_csv(final_data_for_csv, 'comparison table.csv')
    print("Финальные данные успешно записаны в comparison table.csv")

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

    #print(result_process)
    write_sort_csv(result_process)
    return result_process


if __name__ == '__main__':
    orca_opt_nohup = '/Users/anastasiakuznetsova/Documents/НИР/calculate_processing/Elsulfaverin/orca/opt/1/1.out'
    guassian_opt_nohup = '/Users/anastasiakuznetsova/Documents/НИР/calculate_processing/2.log'
    xtb_opt_nohup = '/Users/anastasiakuznetsova/Documents/НИР/calculate_processing/6LUD.out'
    n_0_s_orca = '/Users/anastasiakuznetsova/Documents/НИР/Результаты расчета нитрена/nitren_D3BJ_B3LYP_singlet_orca.out'

    file_list = [orca_opt_nohup, n_0_s_orca]
    main(file_list)














































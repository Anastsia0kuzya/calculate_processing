import linecache
import re
atomic_number = {"H":[1,[255,255,255],"FFFFFF"],"D":[1,[255,255,192],"FFFFC0"],"T":[1,[255,255,160],"FFFFA0"],
                 "He":[2,[217,255,255],"D9FFFF"],"Li":[3,[204,128,255],"CC80FF"],"Be":[4,[194,255,0],"C2FF00"],
                 "B":[5,[255,181,181],"FFB5B5"],"C":[6,[144,144,144],"909090"],"N":[7,[48,80,248],"3050F8"],
                 "O":[8,[255,13,13],"FF0D0D"],"F":[9,[144,224,80],"90E050"],"Ne":[10,[179,227,245],"B3E3F5"],
                 "Na":[11,[171,92,242],"AB5CF2"],"Mg":[12,[138,255,0],"8AFF00"],"Al":[13,[191,166,166],"BFA6A6"],
                 "Si":[14,[240,200,160],"F0C8A0"],"P":[15,[255,128,0],"FF8000"],"S":[16,[255,255,48],"FFFF30"],
                 "Cl":[17,[31,240,31],"1FF01F"],"Ar":[18,[128,209,227],"80D1E3"],"K":[19,[143,64,212],"8F40D4"],
                 "Ca":[20,[61,255,0],"3DFF00"],"Sc":[21,[230,230,230],"E6E6E6"],"Ti":[22,[191,194,199],"BFC2C7"],
                 "V":[23,[166,166,171],"A6A6AB"],"Cr":[24,[138,153,199],"8A99C7"],"Mn":[25,[156,122,199],"9C7AC7"],
                 "Fe":[26,[224,102,51],"E06633"],"Co":[27,[240,144,160],"F090A0"],"Ni":[28,[80,208,80],"50D050"],
                 "Cu":[29,[200,128,51],"C88033"],"Zn":[30,[125,128,176],"7D80B0"],"Ga":[31,[194,143,143],"C28F8F"],
                 "Ge":[32,[102,143,143],"668F8F"],"As":[33,[189,128,227],"BD80E3"],"Se":[34,[255,161,0],"FFA100"],
                 "Br":[35,[166,41,41],"A62929"],"Kr":[36,[92,184,209],"5CB8D1"],"Rb":[37,[112,46,176],"702EB0"],
                 "Sr":[38,[0,255,0],"00FF00"],"Y":[39,[148,255,255],"94FFFF"],"Zr":[40,[148,224,224],"94E0E0"],
                 "Nb":[41,[115,194,201],"73C2C9"],"Mo":[42,[84,181,181],"54B5B5"],"Tc":[43,[59,158,158],"3B9E9E"],
                 "Ru":[44,[36,143,143],"248F8F"],"Rh":[45,[10,125,140],"0A7D8C"],"Pd":[46,[0,105,133],"006985"],
                 "Ag":[47,[192,192,192],"C0C0C0"],"Cd":[48,[255,217,143],"FFD98F"],"In":[49,[166,117,115],"A67573"],
                 "Sn":[50,[102,128,128],"668080"],"Sb":[51,[158,99,181],"9E63B5"],"Te":[52,[212,122,0],"D47A00"],
                 "I":[53,[148,0,148],"940094"],"Xe":[54,[66,158,176],"429EB0"],"Cs":[55,[87,23,143],"57178F"],
                 "Ba":[56,[0,201,0],"00C900"],"La":[57,[112,212,255],"70D4FF"],"Ce":[58,[255,255,199],"FFFFC7"],
                 "Pr":[59,[217,255,199],"D9FFC7"],"Nd":[60,[199,255,199],"C7FFC7"],"Pm":[61,[163,255,199],"A3FFC7"],
                 "Sm":[62,[143,255,199],"8FFFC7"],"Eu":[63,[97,255,199],"61FFC7"],"Gd":[64,[69,255,199],"45FFC7"],
                 "Tb":[65,[48,255,199],"30FFC7"],"Dy":[66,[31,255,199],"1FFFC7"],"Ho":[67,[0,255,156],"00FF9C"],
                 "Er":[68,[0,230,117],"00E675"],"Tm":[69,[0,212,82],"00D452"],"Yb":[70,[0,191,56],"00BF38"],
                 "Lu":[71,[0,171,36],"00AB24"],"Hf":[72,[77,194,255],"4DC2FF"],"Ta":[73,[77,166,255],"4DA6FF"],
                 "W":[74,[33,148,214],"2194D6"],"Re":[75,[38,125,171],"267DAB"],"Os":[76,[38,102,150],"266696"],
                 "Ir":[77,[23,84,135],"175487"],"Pt":[78,[208,208,224],"D0D0E0"],"Au":[79,[255,209,35],"FFD123"],
                 "Hg":[80,[184,184,208],"B8B8D0"],"Tl":[81,[166,84,77],"A6544D"],"Pb":[82,[87,89,97],"575961"],
                 "Bi":[83,[158,79,181],"9E4FB5"],"Po":[84,[171,92,0],"AB5C00"],"At":[85,[117,79,69],"754F45"],
                 "Rn":[86,[66,130,150],"428296"],"Fr":[87,[66,0,102],"420066"],"Ra":[88,[0,125,0],"007D00"],
                 "Ac":[89,[112,171,250],"70ABFA"],"Th":[90,[0,186,255],"00BAFF"],"Pa":[91,[0,161,255],"00A1FF"],
                 "U":[92,[0,143,255],"008FFF"],"Np":[93,[0,128,255],"0080FF"],"Pu":[94,[0,107,255],"006BFF"],
                 "Am":[95,[84,92,242],"545CF2"],"Cm":[96,[120,92,227],"785CE3"],"Bk":[97,[138,79,227],"8A4FE3"],
                 "Cf":[98,[161,54,212],"A136D4"],"Es":[99,[179,31,212],"B31FD4"],"Fm":[100,[179,31,186],"B31FBA"],
                 "Md":[101,[179,13,166],"B30DA6"],"No":[102,[189,13,135],"BD0D87"],"Lr":[103,[199,0,102],"C70066"],
                 "Rf":[104,[204,0,89],"CC0059"],"Db":[105,[209,0,79],"D1004F"],"Sg":[106,[217,0,69],"D90045"],
                 "Bh":[107,[224,0,56],"E00038"],"Hs":[108,[230,0,46],"E6002E"],"Mt":[109,[235,0,38],"EB0026"],
                 "Ds":[110,[0,0,0],"000000"],"Rg":[111,[0,0,0],"000000"],"Cn":[112,[0,0,0],"000000"],"Nh":[113,[0,0,0],"000000"],
                 "Fl":[114,[0,0,0],"000000"],"Mc":[115,[0,0,0],"000000"],"Lv":[116,[0,0,0],"000000"],"Ts":[117,[0,0,0],"000000"],
                 "Og":[118,[0,0,0],"000000"],"UND": [999,[0,0,0],"000000"]}

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


def symbol_to_atomic(list_values):
    #TODO: преобразует симолы эллементов в атомные нормера (подхидт только для тройного списка, где элемент на 0 позиции)
    for s in list_values:
        for k in s:
            if k[0] in atomic_number:
                k[0] = atomic_number[k[0]][0];
    return list_values


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
    #print(list_CARTESIAN_COORDINATES)
    if list_CARTESIAN_COORDINATES[0][0][0] is not int:
        list_CARTESIAN_COORDINATES = symbol_to_atomic(list_CARTESIAN_COORDINATES)
    final_coord = list_CARTESIAN_COORDINATES[5]
    return list_CARTESIAN_COORDINATES, total_time, final_coord

def final_values(orca_opt_nohup):
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
    final_energy = final_values(orca_opt_nohup)[0]
    all_final_energy = final_values(orca_opt_nohup)[1]
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
    print(STEP)
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
    print (len(list_energy), len(list_coord))
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
    print(STEP)


def main(file_path: str):
    dict_GAUSSIAM(file_path)
    #coords_GAUSSIAN(file_path)
    #dict_ORCA(file_path)
    # if 'orca' in file_path:
    #     dict_coord_and_energy = dict_ORCA(file_path)
    #     #print(dict_coord_and_energy)
    # if 'log' in file_path:
    #     dict_coord_and_energy



if __name__ == '__main__':
    #orca_opt_nohup = './Elsulfaverin/orca/opt/1/1.out'
    #orca_opt_nohup = '/Users/anastasiakuznetsova/Documents/НИР/calculate_processing/orca230505/1/1.out'
    guassian_opt_nohup = '/Users/anastasiakuznetsova/Documents/НИР/calculate_processing/2.log'
    main(guassian_opt_nohup)
    #main(orca_opt_nohup)












































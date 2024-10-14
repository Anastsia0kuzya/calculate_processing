import linecache
import re
orca_opt_nohup = './Elsulfaverin/orca/opt/1/1.out'

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

'''общий список всех интерекшенов'''
'''выдает списки с подсписками всех интерекшенов'''
for i in range(1, len(list_total_energy), 2):
    list_total_energy[i] = float(list_total_energy[i])
#l = list(map(lambda x,y:[x,y],list_total_energy[::2],list_total_energy[1::2]))
l_first = [] #первый список
for i in range(0, len(list_total_energy)//2, 2):
    l_first.append([list_total_energy[i], list_total_energy[i+1]])
l_end = [] #конечный список
for i in range(len(list_total_energy)//2, len(list_total_energy) - 1, 2):
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
    final_list_energy.append(i[-1])
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
final_miny_dict = {
    "total_time": total_time,
    "final_energy": final_list_energy,
    "final_coords": list_CARTESIAN_COORDINATES[-1]
}
STEP['final_data'] = final_miny_dict
print(STEP)
















































import linecache
import re
orca_opt_nohup = '/Users/anastasiakuznetsova/Documents/НИР/pars/Elsulfaverin/orca/opt/1/1.out'

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
for i in range(1, len(list_total_energy), 2):
    list_total_energy[i] = float(list_total_energy[i])
#l = list(map(lambda x,y:[x,y],list_total_energy[::2],list_total_energy[1::2]))

#первый список
l_first = []
for i in range(len(list_total_energy)//2):
    l_first.append(list_total_energy[i])
l_end = [] #конечный список
for i in range(len(list_total_energy)//2 + 1, len(list_total_energy)):
    l_end.append(list_total_energy[i]) #разбили последний и первый
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
                line = 'ITERATION' + line
                energy.append(line)

l_intermediate = []
for i in energy:
    l_intermediate.append(i.split())
print(l_intermediate)
list_total_energy = l_first + l_intermediate + l_end
#print(list_total_energy)
for i in range(1, len(list_total_energy), 2):  # Начинаем с 1 и пропускаем каждую вторую строку
        list_total_energy[i] = float(list_total_energy[i])  # Преобразуем строку в число
#print(list_total_energy)

'''словари'''
# dict_total_energy={}
# for i in list_total_energy:
#     dict_total_energy = {item[0]: item[1:] for item in list_total_energy}
# print(dict_total_energy)

# l1 = list(map(lambda x,y:[x,y],list_total_energy[::2],list_total_energy[1::2]))
# dict_={}
# for i in l1:
#     dict_.setdefault(i[0], []).append(i[1])
# print(dict_)







'''Список списков координат'''
start_line_coord = []
end_line_coord = []
with open(orca_opt_nohup) as file:
    for index, k in enumerate(file):
        if 'CARTESIAN COORDINATES (ANGSTROEM)' in k:
            start_line_coord.append(index)
        if 'CARTESIAN COORDINATES (A.U.)' in k:
            end_line_coord.append(index)
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
            list_CARTESIAN_COORDINATES.append(current_sublist)
            current_sublist = []  # Обнуляем текущий подсписок
    else:
        current_sublist.append(item)
if current_sublist: # Добавляем последний подсписок, если он не пуст
    list_CARTESIAN_COORDINATES.append(current_sublist)



# for item in energy:
#     # Пытаемся найти подстроку и число в строке
#     parts = item.rsplit(' ', 1)  # Разбиваем с конца на две части
#     if len(parts) == 2: #Делим строку из интерекшенов на подсписки с числом и ITERATION
#         substring = parts[0]  # Подстрока
#         number = parts[1]  # Число в виде строки
#         l_intermediate.append([substring, float(number)])






































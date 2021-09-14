import os
import csv

file_dir = os.getcwd()
file_list = os.listdir(file_dir)

record_list = []
for file_name in file_list:
    if len(file_name) > 20:
        record_list.append(file_name)


read_file = open('RSSI_MAP.csv', 'r', encoding='utf-8')
rd = csv.reader(read_file)

write_file = open('bias_adjust.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(write_file)

rssi_map = []

for content in rd:

    if content[0] == 'Base Minor':
        wr.writerow(content)
    else:
        rssi_container = [content[0], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(1, 41):
            rssi_container[i] = float(content[i])
        rssi_map.append(rssi_container)

RSSI_BASE_AVG = 0
for i in range(1, 41):
    RSSI_BASE_AVG += rssi_map[i-1][i]

RSSI_BASE_AVG /= 40

for i in range(1, 41):
    bias = rssi_map[i-1][i] - RSSI_BASE_AVG
    for j in range(1, 41):
        rssi_map[i-1][j] = round(rssi_map[i-1][j] - bias, 5)

for rssi in rssi_map:
    wr.writerow(rssi)

read_file.close()
write_file.close()

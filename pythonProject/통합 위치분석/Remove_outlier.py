import csv
import os

#   outlier 제거 기준 BLE 수집 수
BASE_BLE = 6

fileDir = os.getcwd() + "/FILES/"
fileList = os.listdir(fileDir)

print(fileDir)

for file in fileList:
    read_file = open(fileDir + file, 'r', encoding='utf-8')
    rd = csv.reader(read_file)

    write_outlier = open(file[:16] + "_outlier.csv", 'w', encoding='utf-8', newline='')
    wr_outlier = csv.writer(write_outlier)

    write_file = open(file[:16] + "_no_outlier.csv", 'w', encoding='utf-8', newline='')
    wr = csv.writer(write_file)

    for content in rd:
        ble_ctr = 0
        if content[0] == 'reg_dt':
            wr.writerow(content)
            wr_outlier.writerow(content)
            continue
        for i in range(161, 201):
            if int(content[i]) < 0:
                ble_ctr += 1

        if ble_ctr <= BASE_BLE:
            wr_outlier.writerow(content)
            for i in range(161, 201):
                content[i] = 0
            wr.writerow(content)
        else:
            wr.writerow(content)
            for i in range(161, 201):
                content[i] = 0
            wr_outlier.writerow(content)

    write_outlier.close()
    write_file.close()

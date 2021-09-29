import csv
import os
import matplotlib.pyplot as plt

#   outlier 제거 기준 BLE 수집 수
BASE_BLE = 6

fileDir = os.getcwd() + "/FILES/"
fileList = os.listdir(fileDir)

frequency = []

for file in fileList:
    #   데이터 파일 읽기
    read_file = open(fileDir + file, 'r', encoding='utf-8')
    rd = csv.reader(read_file)

    for content in rd:
        #   속성 행은 연산에서 제외
        if content[0] == 'reg_dt':
            continue

        ble_ctr = 0
        for i in range(161, 201):
            if int(content[i]) < 0:
                ble_ctr += 1

        frequency.append(ble_ctr)

    plt.figure(figsize=(10, 10))
    plt.hist(frequency)
    plt.title("beacon frequency")
    plt.savefig("beacon_frequency.png")

    read_file.close()

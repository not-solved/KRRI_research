import csv
import os
import math
import numpy as np
import matplotlib.pyplot as plt
from queue import PriorityQueue

coord_idx = [[-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1],
       [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1],
       [1, 4], [1, 3], [2, 3], [2, 4], [3, 4], [3, 3], [4, 3], [4, 4], [5,  4], [5,  3],
       [6, 3], [6, 4], [7, 4], [7, 3], [8, 3], [8, 4], [9, 4], [9, 3], [10, 3], [10, 4],
       [1, 2], [1, 1], [2, 1], [2, 2], [3, 2], [3, 1], [4, 1], [4, 2], [5,  2], [5,  1],
       [6, 1], [6, 2], [7, 2], [7, 1], [8, 4], [8, 2], [9, 2], [9, 1], [10, 1], [10, 2]]

rssi_idx = ['21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
            '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
            '41', '42', '43', '44', '45', '46', '47', '48', '49', '50',
            '51', '52', '53', '54', '55', '56', '57', '58', '59', '60']

RSSImap = []        # Fingerprint Mapping Table
distMatrix = []     # Distance Vector Matrix
for i in range(0, 40):
    RSSImap.append(np.zeros(40))
    distMatrix.append(np.zeros(40))


#      Euclidean Distance
def get_distance(idx1, idx2):
    return pow((coord_idx[idx1][0] - coord_idx[idx2][0]) * 0.45, 2) + pow((coord_idx[idx1][1] - coord_idx[idx2][1]) * 0.45, 2)


#       RSSI 값을 이용한 Euclidean Distance 거리 계산 후 최소의 D 반환
def get_distance_by_RSSI(beaconList):
    pq = PriorityQueue()
    for i in range(21, 61):
        dist = 0
        for j in beaconList:
            dist += math.pow(RSSImap[i - 21][j[0] - 21] - j[1], 2)

        #   (거리값, 해당 기준 위치)
        #   거리 기준으로 정렬하여, 우선순위 큐 머리에는 최소 거리에 해당하는 값이 있다.
        pq.put([math.sqrt(dist), i])

    return pq.get()

#       RSSI Map 그리기
'''
#       Read data
filePath = "C:/Users/lab_408/Downloads/pythonProject/BLE 신호분석"
fileList = os.listdir(filePath)

for file in fileList:
    #   데이터 파일만 읽는다.
    if len(file) < 20:
        continue
    #   RSSI 신호 기록 파일 열기
    fread = open(file, 'r', encoding='utf-8')
    rd = csv.reader(fread)

    rssi_cnt = np.zeros(40)
    for line in rd:
        if line[0] == 'TIME':
            continue

        #   블록 별 RSSI 신호 누적
        for i in range(len(rssi_idx)):
            if rssi_idx[i] == line[2]:
                RSSImap[int(line[1]) - 21][i] += int(line[3])
                rssi_cnt[i] += 1

    #   RSSI 신호 평균치 계산
    for i in range(len(rssi_cnt)):
        if rssi_cnt[i] == 0:        # Zero division 방지
            continue
        RSSImap[int(file[7:9]) - 21][i] /= rssi_cnt[i]

#       RSSI Map 쓰기파일
fwrite = open("RSSI_MAP.csv", 'w', encoding='utf-8')
wr = csv.writer(fwrite, lineterminator='\n')

wr.writerow(['Base Minor', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
            '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
            '41', '42', '43', '44', '45', '46', '47', '48', '49', '50',
            '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '\n'])
for i in range(21, 61):
    data = []
    data.append(i)
    for a in range(0, 40):
        data.append(RSSImap[i-21][a])
    data.append('\n')
    wr.writerow(data)

fwrite.close()
'''

#       RSSI_MAP.csv 읽기 (사전에 정의한 MAP)
fread = open("RSSI_MAP.csv", 'r', encoding='utf-8')
rd = csv.reader(fread)

idx = 0
for line in rd:
    if line[0] == 'Base Minor':
        continue
    for i in range(1, 41):
        RSSImap[idx][i-1] = float(line[i])
    idx += 1

fread.close()


filePath = "C:/Users/lab_408/Downloads/pythonProject/BLE 신호분석"
fileList = os.listdir(filePath)

for file in fileList:
    #   데이터 파일만 읽는다.
    if len(file) < 20:
        continue
    Read = open(file, 'r', encoding='utf-8')
    rd = csv.reader(Read)

    time = ""
    minorList = []
    rmsList = []
    correct = 0
    cnt = 0

    for line in rd:
        #       속성 행은 넘긴다.
        if line[0] == 'TIME':
            continue

        #       주기 체크 (동일 시간은 같은 주기로 계산)
        if time != line[0]:
            time = line[0]

            #   첫 시작은 넘긴다
            if len(minorList) == 0:
                continue

            #   RSSI map을 참조하여 각각의 거리 계산 후 최소값을 반환
            answer = get_distance_by_RSSI(minorList)
            if answer[1] == int(file[7:9]):
                correct += 1
            minorList.clear()
            rmsList.append(answer[1])
            cnt += 1
            continue

        #   Minor, RSSI
        minorList.append([int(line[2]), int(line[3])])

    RMS = 0.0
    dist = 0
    for i in rmsList:
        dist = get_distance(int(file[7:9]), i)
        RMS += dist

    RMS /= len(rmsList)
    print(file[7:9], "\t", round(correct / cnt, 5), "\t", round(math.sqrt(RMS), 5))

import csv
import os
import math
import numpy as np
import matplotlib.pyplot as plt
from queue import PriorityQueue

#   Fingerprint Mapping Table
RSSImap = []
RSSImap_bias = []
for i in range(0, 40):
    RSSImap.append(np.zeros(40))
    RSSImap_bias.append(np.zeros(40))

#   BLE coord, 42번 블록 모서리를 기준점(0, 0)으로 측정
coord_rssi = [
    [1.575, 0.225], [1.125, 0.225], [1.125, 0.675], [1.575, 0.675], [1.575, 1.125], [1.125, 1.125],
    [1.125, 1.575], [1.575, 1.575], [1.575, 2.025], [1.125, 2.025], [1.125, 2.475], [1.575, 2.475],
    [1.575, 2.925], [1.125, 2.925], [1.125, 3.375], [1.575, 3.375], [1.575, 3.825], [1.125, 3.825],
    [1.125, 4.275], [1.575, 4.275],
    [0.675, 0.225], [0.225, 0.225], [0.225, 0.675], [0.675, 0.675], [0.675, 0.225], [0.225, 0.225],
    [0.225, 0.675], [0.675, 0.675], [0.675, 2.025], [0.225, 2.025], [0.225, 2.475], [0.675, 2.475],
    [0.675, 2.925], [0.225, 2.925], [0.225, 3.375], [0.675, 3.375], [0.675, 3.825], [0.225, 3.825],
    [0.225, 4.275], [0.675, 4.275]
]


#      Euclidean Distance
def get_distance(idx1, idx2):
    return pow(coord_rssi[idx1][0] - coord_rssi[idx2][0], 2) + pow(coord_rssi[idx1][1] - coord_rssi[idx2][1], 2)


#       RSSI 값을 이용한 Euclidean Distance 거리 계산 후 최소의 D 반환 (Fingerprinting)
def get_distance_by_RSSI(beaconList):
    minors = []
    for beacons in beaconList:
        minors.append(beacons[0])

    pq = PriorityQueue()
    for i in minors:
        dist = 0
        for j in beaconList:
            dist += math.sqrt(pow(RSSImap_bias[i - 21][j[0] - 21] - j[1], 2))

        #   (거리값, 해당 기준 위치)
        #   거리 기준으로 정렬하여, 우선순위 큐 머리에는 최소 거리에 해당하는 값이 있다.
        pq.put([dist, i])

    return pq.get()


#       RSSI_MAP.csv 읽기 (사전에 정의한 MAP)
def read_RSSI_MAP(fileName, map_name):
    read_map = open(fileName, 'r', encoding='utf-8')
    reader = csv.reader(read_map)

    idx = 0
    for content in reader:
        if content[0] == 'Base Minor':
            continue
        for i in range(1, 41):
            map_name[idx][i-1] = float(content[i])
        idx += 1

    read_map.close()


#   Map 으로 사용할 파일 읽기
file_name_list = ["RSSI_MAP.csv", "bias_adjust_avg.csv", "bias_adjust_mid.csv"]
file_name = file_name_list[2]

#   RSSI map 그리기
read_RSSI_MAP("RSSI_MAP.csv", RSSImap)
read_RSSI_MAP(file_name, RSSImap_bias)

write_file = open("result_" + file_name, 'w', encoding='utf-8', newline='')
wr = csv.writer(write_file)

wr.writerow(['BASE', 'MAX', 'MIN', 'AVG', 'RMS'])

minor_bias = []
for minor in range(0, 40):
    minor_bias.append(RSSImap[minor][minor] - RSSImap_bias[minor][minor])


filePath = os.getcwd()
fileList = os.listdir(filePath)
for file in fileList:
    #   데이터 파일만 읽는다.
    if len(file) != 25:
        continue

    Read = open(file, 'r', encoding='utf-8')
    rd = csv.reader(Read)

    time = ""
    minorList = []
    rmsList = []

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
            #   RSSI Map 을 참조하여 각각의 거리 계산 후 최소값을 반환
            answer = get_distance_by_RSSI(minorList)
            minorList.clear()
            rmsList.append(answer[1])
            continue

        #   Minor, RSSI
        minorList.append([int(line[2]), int(line[3]) - minor_bias[int(line[2]) - 21]])

    RMS = 0.0
    dist = 0
    max_dist = 0
    min_dist = 100
    avg_dist = 0
    result_list = []
    #   측정된 거리의 최대, 최소, 평균, RMS 계산
    for i in rmsList:
        dist = get_distance(int(file[7:9]) - 21, i - 21)
        RMS += dist
        result_list.append(math.sqrt(dist))
        dist = math.sqrt(dist)
        if max_dist < dist:
            max_dist = dist
        if min_dist > dist:
            min_dist = dist
        avg_dist += dist

    RMS /= len(rmsList)
    avg_dist /= len(rmsList)

    print(file[7:9], "\t",
          round(max_dist, 5), "\t",
          round(min_dist, 5), "\t",
          round(avg_dist, 5), "\t",
          round(math.sqrt(RMS), 5))

    wr.writerow([file[7:9], round(max_dist, 5), round(min_dist, 5), round(avg_dist, 5), round(math.sqrt(RMS), 5)])

    plt.xlim(0, 4.5)
    plt.hist(result_list)
    plt.title(file[7:9] + "--" + file_name[0:15])
    plt.savefig(file[7:9] + "--" + file_name[0:15] + '.png')
    plt.close()

write_file.close()

import csv
import math
import numpy as np
from queue import PriorityQueue
import matplotlib.pyplot as plt

RSSI_MAP = []
RSSI_MAP_bias = []
interval = 300

RSSI_count_list = np.zeros(40)

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
coord_lc = [
    [[1.6875, 0.1125], [1.4625, 0.1125], [1.4625, 0.3375], [1.6875, 0.3375]],
    [[1.2375, 0.1125], [1.0125, 0.1125], [1.0125, 0.3375], [1.2375, 0.3375]],
    [[1.2375, 0.5625], [1.0125, 0.5625], [1.0125, 0.7875], [1.2375, 0.7875]],
    [[1.6875, 0.5625], [1.4625, 0.5625], [1.4625, 0.7875], [1.6875, 0.7875]],
    [[1.6875, 1.0125], [1.4625, 1.0125], [1.4625, 1.2375], [1.6875, 1.2375]],
    [[1.2375, 1.0125], [1.0125, 1.0125], [1.0125, 1.2375], [1.2375, 1.2375]],
    [[1.2375, 1.4625], [1.0125, 1.4625], [1.0125, 1.6875], [1.2375, 1.6875]],
    [[1.6875, 1.4625], [1.4625, 1.4625], [1.4625, 1.6875], [1.6875, 1.6875]],
    [[1.6875, 1.9125], [1.4625, 1.9125], [1.4625, 2.1375], [1.6875, 2.1375]],
    [[1.2375, 1.9125], [1.0125, 1.9125], [1.0125, 2.1375], [1.2375, 2.1375]],

    [[1.2375, 2.3625], [1.0125, 2.3625], [1.0125, 2.5875], [1.2375, 2.5875]],
    [[1.6875, 2.3625], [1.4625, 2.3625], [1.4625, 2.5875], [1.6875, 2.5875]],
    [[1.6875, 2.8125], [1.4625, 2.8125], [1.4625, 3.0375], [1.6875, 3.0375]],
    [[1.2375, 2.8125], [1.0125, 2.8125], [1.0125, 3.0375], [1.2375, 3.0375]],
    [[1.2375, 3.2625], [1.0125, 3.2625], [1.0125, 3.4875], [1.2375, 3.4875]],
    [[1.6875, 3.2625], [1.4625, 3.2625], [1.4625, 3.4875], [1.6875, 3.4875]],
    [[1.6875, 3.7125], [1.4625, 3.7125], [1.4625, 3.9375], [1.6875, 3.9375]],
    [[1.2375, 3.7125], [1.0125, 3.7125], [1.0125, 3.9375], [1.2375, 3.9375]],
    [[1.2375, 4.1625], [1.0125, 4.1125], [1.0125, 4.3875], [1.2375, 4.3875]],
    [[1.6875, 4.1625], [1.4625, 4.1625], [1.4625, 4.3875], [1.6875, 4.3875]],

    [[0.7875, 0.1125], [0.5625, 0.1125], [0.5625, 0.3375], [0.7875, 0.3375]],
    [[0.3375, 0.1125], [0.1125, 0.1125], [0.1125, 0.3375], [0.3375, 0.3375]],
    [[0.3375, 0.5625], [0.1125, 0.5625], [0.1125, 0.7875], [0.3375, 0.7875]],
    [[0.7875, 0.5625], [0.5625, 0.5625], [0.5625, 0.7875], [0.7875, 0.7875]],
    [[0.7875, 1.0125], [0.5625, 1.0125], [0.5625, 1.2375], [0.7875, 1.2375]],
    [[0.3375, 1.0125], [0.1125, 1.0125], [0.1125, 1.2375], [0.3375, 1.2375]],
    [[0.3375, 1.4625], [0.1125, 1.4625], [0.1125, 1.6875], [0.3375, 1.6875]],
    [[0.7875, 1.4625], [0.5625, 1.4625], [0.5625, 1.6875], [0.7875, 1.6875]],
    [[0.7875, 1.9125], [0.5625, 1.9125], [0.5625, 2.1375], [0.7875, 2.1375]],
    [[0.3375, 1.9125], [0.1125, 1.9125], [0.1125, 2.1375], [0.3375, 2.1375]],

    [[0.3375, 2.3625], [0.1125, 2.3625], [0.1125, 2.5875], [0.3375, 2.5875]],
    [[0.7875, 2.3625], [0.5625, 2.3625], [0.5625, 2.5875], [0.7875, 2.5875]],
    [[0.7875, 2.8125], [0.5625, 2.8125], [0.5625, 3.0375], [0.7875, 3.0375]],
    [[0.3375, 2.8125], [0.1125, 2.8125], [0.1125, 3.0375], [0.3375, 3.0375]],
    [[0.3375, 3.2625], [0.1125, 3.2625], [0.1125, 3.4875], [0.3375, 3.4875]],
    [[0.7875, 3.2625], [0.5625, 3.2625], [0.5625, 3.4875], [0.7875, 3.4875]],
    [[0.7875, 3.7125], [0.5625, 3.7125], [0.5625, 3.9375], [0.7875, 3.9375]],
    [[0.3375, 3.7125], [0.1125, 3.7125], [0.1125, 3.9375], [0.3375, 3.9375]],
    [[0.3375, 4.1625], [0.1125, 4.1125], [0.1125, 4.3875], [0.3375, 4.3875]],
    [[0.7875, 4.1625], [0.5625, 4.1625], [0.5625, 4.3875], [0.7875, 4.3875]],
]

MAP_LIST = ["RSSI_MAP.csv", "bias_adjust_avg.csv", "bias_adjust_mid.csv"]


#       RSSI Map ????????????
def read_Map(map_idx, map_name):
    map_read = open(MAP_LIST[map_idx], 'r', encoding='utf-8')
    contents = csv.reader(map_read)

    idx = 0
    for line in contents:
        map_name.append(np.zeros(40))
        if line[0] == 'Base Minor':
            continue
        for loop in range(1, 41):
            map_name[idx][loop - 1] = float(line[loop])
        idx += 1

    map_read.close()


#       RSSI ?????? ????????? Euclidean Distance ?????? ?????? ??? ????????? D ??????
def get_location_by_RSSI(BLE_list):

    if len(BLE_list) == 0:
        RSSI_count_list[0] += 1
        return [0, 0]

    minors = []
    for beacons in BLE_list:
        minors.append(beacons[0])

    RSSI_count_list[len(minors)] += 1

    if len(minors) <= 10:
        return [0, 0]

    pq = PriorityQueue()
    #       RSSI Map ?????? ??????
    for loop in minors:
        dist = 0
        for ble in BLE_list:
            dist += math.pow(RSSI_MAP_bias[loop - 21][ble[0] - 21] - ble[1], 2)

        #   (?????????, ?????? ?????? ??????)
        #   ?????? ???????????? ????????????, ???????????? ??? ???????????? ?????? ????????? ???????????? ?????? ??????.
        pq.put([math.sqrt(dist), loop])

    return coord_rssi[pq.get()[1] - 21]


#       LC ?????? ????????? ????????? ?????? ??????
def get_location_by_LC(LC_list):
    if len(LC_list) == 0:
        return [0, 0]

    pq = PriorityQueue()
    for lc in LC_list:
        pq.put(lc)

    base_lc = 8
    #       LC??? ??????
    while pq.qsize() >= base_lc:
        pq.get()

    left_size = pq.qsize()
    result_coord = [0, 0]
    while pq.qsize() > 0:
        temp = pq.get()
        # result_coord.append([coord_lc[temp[1]][temp[2]][0], coord_lc[temp[1]][temp[2]][1]])
        result_coord[0] += coord_lc[temp[1] - 21][temp[2]][0]
        result_coord[1] += coord_lc[temp[1] - 21][temp[2]][1]

    result_coord[0] = round(result_coord[0] / left_size, 5)
    result_coord[1] = round(result_coord[1] / left_size, 5)
    return result_coord


#       ?????? ????????? ?????? ????????????
File_read = open('Files/signal_record_03.csv', 'r', encoding='utf-8')
rd = csv.reader(File_read)
read_Map(0, RSSI_MAP)
read_Map(2, RSSI_MAP_bias)


#       RSSI Map??? ?????? ?????? ??? ?????? ??????
bias_list = []
for idx in range(0, 40):
    bias_list.append(RSSI_MAP[idx][idx] - RSSI_MAP_bias[idx][idx])

print(bias_list)

#       ????????? BLE, LC ????????? ?????? ??????
BLE_content = []
LC_content = []

#       ?????? BLE, LC ??????
BLE_location = []
LC_location = []
TIME_log = []

x_ble = []
y_ble = []
x_lc = []
y_lc = []

BLE_base = -80
LC_base = 500

time = 'no'
#       ?????? ?????? ???????????? ??????
for content in rd:

    if content[0] == 'reg_dt':
        continue
    #   21 ~ 60??? ????????? BLE, LC ?????? ??????????????? ??????
    for i in range(0, 40):
        if (float(content[i + 161]) - bias_list[i]) > BLE_base and float(content[i + 161]) != 0:
            BLE_content.append([i + 21, float(content[i + 161]) - bias_list[i]])
        lc_value = [int(content[i * 4 + 1]), int(content[i * 4 + 2]), int(content[i * 4 + 3]), int(content[i * 4 + 4])]
        if lc_value[0] > LC_base:
            LC_content.append([lc_value[0], i + 21, 0])
        if lc_value[1] > LC_base:
            LC_content.append([lc_value[1], i + 21, 1])
        if lc_value[2] > LC_base:
            LC_content.append([lc_value[2], i + 21, 2])
        if lc_value[3] > LC_base:
            LC_content.append([lc_value[3], i + 21, 3])
    
    #   ?????? ??????
    TIME_log.append(content[0])
    #   BLE ?????? x, y?????? ??????
    ble_result = get_location_by_RSSI(BLE_content)

    x_ble.append(ble_result[0])
    y_ble.append(ble_result[1])
    #   LC ?????? x, y?????? ??????
    lc_result = get_location_by_LC(LC_content)
    x_lc.append(lc_result[0])
    y_lc.append(lc_result[1])

    BLE_content.clear()
    LC_content.clear()

File_read.close()
plt.axis([0.0, 1.8, 0.0, 4.5])

plt.figure(figsize=(6, 14))
plt.axis([0.0, 1.8, 0.0, 4.5])


#   ?????? ??? ????????? ????????? ???????????? ??????
for time in range(len(TIME_log)):

    plt.figure(figsize=(6, 14))
    plt.axis([0.0, 1.8, 0.0, 4.5])

    x_label = [0.0, 0.45, 0.9, 1.35, 1.8]
    y_label = [0.0, 0.45, 0.9, 1.35, 1.8, 2.25, 2.7,
               3.15, 3.6, 4.05, 4.5]

    plt.xticks(x_label)
    plt.yticks(y_label)
    plt.scatter(x_lc[time], y_lc[time], s=100)
    plt.scatter(x_ble[time], y_ble[time], s=100)
    plt.grid(True)
    plt.title("location : " + str(TIME_log[time]))
    plt.savefig("location_" + str(time) + ".png")
    plt.close()

print(RSSI_count_list)
''''
plt.figure(figsize=(6, 8))
plt.hist(RSSI_count_list)
plt.show()
'''
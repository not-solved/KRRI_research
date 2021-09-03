import csv
import numpy as np
import matplotlib.pyplot as plt
from queue import PriorityQueue

'''
Map = [
    [60[3], 60[4], 39[3], 39[4], 40[3], 40[4]],
    [60[2], 60[1], 39[2], 39[1], 40[2], 40[1]],
    [57[3], 57[4], 38[3], 38[4], 37[3], 37[4]],
    [57[2], 57[1], 38[2], 38[1], 37[2], 37[1]],
    [56[3], 56[4], 35[3], 35[4], 36[3], 36[4]],
    [56[2], 56[1], 35[2], 35[1], 36[2], 36[1]]
]
'''

m35 = [[0, 3], [0, 2], [1, 2], [1, 3]]
m36 = [[0, 5], [0, 4], [1, 4], [1, 5]]
m37 = [[2, 5], [2, 4], [3, 4], [3, 5]]
m38 = [[2, 3], [2, 2], [3, 2], [3, 3]]
m39 = [[4, 3], [4, 2], [5, 2], [5, 3]]
m40 = [[4, 5], [4, 4], [5, 4], [5, 5]]
m56 = [[0, 1], [0, 0], [1, 0], [1, 1]]
m57 = [[2, 1], [2, 0], [3, 0], [3, 1]]
m60 = [[4, 1], [4, 0], [5, 0], [5, 1]]

lcValue = [
    np.zeros(5),
    np.zeros(5),
    np.zeros(5),
    np.zeros(5),
    np.zeros(5),
    np.zeros(5),
    np.zeros(5),
    np.zeros(5),
    np.zeros(5)
]


def initialize():
    for i in range(0, 9):
        lcValue[i].fill(5)

def get_coord(minor, lc):
    if minor == '35':
        if lc == 5:     return m35[0]
        elif lc == 6:   return m35[1]
        elif lc == 7:   return m35[2]
        elif lc == 8:   return m35[3]
    elif minor == '36':
        if lc == 5:     return m36[0]
        elif lc == 6:   return m36[1]
        elif lc == 7:   return m36[2]
        elif lc == 8:   return m36[3]
    elif minor == '37':
        if lc == 5:     return m37[0]
        elif lc == 6:   return m37[1]
        elif lc == 7:   return m37[2]
        elif lc == 8:   return m37[3]
    elif minor == '38':
        if lc == 5:     return m38[0]
        elif lc == 6:   return m38[1]
        elif lc == 7:   return m38[2]
        elif lc == 8:   return m38[3]
    elif minor == '39':
        if lc == 5:     return m39[0]
        elif lc == 6:   return m39[1]
        elif lc == 7:   return m39[2]
        elif lc == 8:   return m39[3]
    elif minor == '40':
        if lc == 5:     return m40[0]
        elif lc == 6:   return m40[1]
        elif lc == 7:   return m40[2]
        elif lc == 8:   return m40[3]
    elif minor == '56':
        if lc == 5:     return m56[0]
        elif lc == 6:   return m56[1]
        elif lc == 7:   return m56[2]
        elif lc == 8:   return m56[3]
    elif minor == '57':
        if lc == 5:     return m57[0]
        elif lc == 6:   return m57[1]
        elif lc == 7:   return m57[2]
        elif lc == 8:   return m57[3]
    elif minor == '60':
        if lc == 5:     return m60[0]
        elif lc == 6:   return m60[1]
        elif lc == 7:   return m60[2]
        elif lc == 8:   return m60[3]


def record_Queue(PQ, lcValue, coord):
    PQ.put([lcValue * -1, coord])


def get_target_coord(PQ):
    cnt = 0;
    coord = np.zeros(2)
    temp = np.zeros(2)
    while (not PQ.empty()) and cnt < 8:
        temp = PQ.get()[1]
        coord += temp
        cnt += 1

    coord[0] /= cnt
    coord[1] /= cnt
    result = [coord[1], coord[0]]

    return result

fileList = ['task1.csv', 'task2.csv', 'task3.csv', 'task4.csv']

for file in fileList:
    fread = open(file, 'r', encoding='utf-8')
    rd = csv.reader(fread)

    initialize()
    Q = PriorityQueue()
    resultCoord = [-1, -1]
    minorList = ['35', '36', '37', '38', '39', '40', '56', '57', '60']
    breakCnt = 1
    for line in rd:
        if line[0] == 'board_id':
            continue

        #   다음 상태를 읽는다다
        if line[0] == "Break":
            for m in range(0, 9):
                for i in range(0, 4):
                    record_Queue(Q, lcValue[m][i] / lcValue[m][4], get_coord(minorList[m], i+5))

            resultCoord = get_target_coord(Q)
            print(file, breakCnt, " : ", resultCoord)
            breakCnt += 1
            initialize()
            continue

        if line[4] == '35':
            lcValue[0] += [int(line[5]), int(line[6]), int(line[7]), int(line[8]), 1]
        elif line[4] == '36':
            lcValue[1] += [int(line[5]), int(line[6]), int(line[7]), int(line[8]), 1]
        elif line[4] == '37':
            lcValue[2] += [int(line[5]), int(line[6]), int(line[7]), int(line[8]), 1]
        elif line[4] == '38':
            lcValue[3] += [int(line[5]), int(line[6]), int(line[7]), int(line[8]), 1]
        elif line[4] == '39':
            lcValue[4] += [int(line[5]), int(line[6]), int(line[7]), int(line[8]), 1]
        elif line[4] == '40':
            lcValue[5] += [int(line[5]), int(line[6]), int(line[7]), int(line[8]), 1]
        elif line[4] == '56':
            lcValue[6] += [int(line[5]), int(line[6]), int(line[7]), int(line[8]), 1]
        elif line[4] == '57':
            lcValue[7] += [int(line[5]), int(line[6]), int(line[7]), int(line[8]), 1]
        elif line[4] == '60':
            lcValue[8] += [int(line[5]), int(line[6]), int(line[7]), int(line[8]), 1]

    plt.figure(figsize=(7, 8))


    fread.close()

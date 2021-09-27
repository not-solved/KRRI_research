import csv
import os
import math
import numpy as np
import matplotlib.pyplot as plt
from queue import PriorityQueue

idx = np.array([[-1, -1],
       [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1],
       [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1],
       [1, 4], [1, 3], [2, 3], [2, 4], [3, 4], [3, 3], [4, 3], [4, 4], [5,  4], [5,  3],
       [6, 3], [6, 4], [7, 4], [7, 3], [8, 3], [8, 4], [9, 4], [9, 3], [10, 3], [10, 4],
       [1, 2], [1, 1], [2, 1], [2, 2], [3, 2], [3, 1], [4, 1], [4, 2], [5,  2], [5,  1],
       [6, 1], [6, 2], [7, 2], [7, 1], [8, 4], [8, 2], [9, 2], [9, 1], [10, 1], [10, 2]])

Map = [[42, 41, 22, 21], [43, 44, 23, 24], [46, 45, 26, 25], [47, 48, 27, 28], [50, 49, 30, 29],
       [51, 52, 31, 32], [54, 53, 34, 33], [55, 56, 35, 36], [58, 57, 38, 37], [59, 60, 39, 40]]

distMatrix = []
for i in range(0, 61):
    distMatrix.append(np.zeros(61))


#      Euclidean Distance
def get_distance(idx1, idx2):
    return pow((idx[idx1][0] - idx[idx2][0]) * 0.45, 2) + pow((idx[idx1][1] - idx[idx2][1]) * 0.45, 2)


#      calculate coord by coord distance
def record_distance_vector(Matrix, list):
    for i in range(len(list)):
        j = i + 1
        while j < len(list):
            distance = math.sqrt(get_distance(list[i], list[j]))
            Matrix[list[i]][list[j]] = distance
            Matrix[list[j]][list[i]] = distance
            Matrix[list[i]][0] += distance
            Matrix[list[j]][0] += distance
            j += 1

    while len(list) > 3:
        tempMax = 0
        target = 0
        for i in range(len(list)):
            if Matrix[minor_list[i]][0] * -1 > tempMax:
                tempMax = Matrix[list[i]][0]
                target = list[i]

        list.remove(target)
        for i in range(len(list)):
            Matrix[list[i]][0] -= Matrix[list[i]][target]


#      파일 열기
filePath = os.getcwd() + '/Dataset/'
fileList = os.listdir(filePath)

rmsList = []
maxList = []
minList = []
idxList = []
coordList = []
for file in fileList:

    fread = open(filePath + file, 'r', encoding='utf-8')
    rd = csv.reader(fread)

    time = ""
    minor_list = []
    Matrix = []
    Q = PriorityQueue()
    for line in rd:
        if line[0] == 'TIME':
            continue

        if line[0] != time:
            time = line[0]
            if Q.empty():
                continue

            minor_list.clear()
            while not Q.empty():
                value = Q.get()[1]
                if len(minor_list) <= 10:
                    minor_list.append(value)

            distance = 0
            Matrix.clear()
            for i in range(0, 61):
                Matrix.append(np.zeros(61))

            for i in range(len(minor_list)):
                j = i + 1
                while j < len(minor_list):
                    distance = math.sqrt(get_distance(minor_list[i], minor_list[j]))
                    Matrix[minor_list[i]][minor_list[j]] = distance
                    Matrix[minor_list[j]][minor_list[i]] = distance
                    Matrix[minor_list[i]][0] += (distance * -1)
                    Matrix[minor_list[j]][0] += (distance * -1)
                    j += 1

            while len(minor_list) > 5:
                tempMax = 0
                target = 0
                for i in range(len(minor_list)):
                    if Matrix[minor_list[i]][0] * -1 > tempMax:
                        tempMax = Matrix[minor_list[i]][0]
                        target = minor_list[i]
                minor_list.remove(target)

                for i in range(len(minor_list)):
                    Matrix[minor_list[i]][0] -= Matrix[minor_list[i]][target]

            coord_x = 0
            coord_y = 0
            for i in range(len(minor_list)):
                coord_x += idx[minor_list[i]][0]
                coord_y += idx[minor_list[i]][1]
                # print(minor_list[i], Matrix[minor_list[i]][0])

            coord_x /= len(minor_list)
            coord_y /= len(minor_list)
            coordList.append([coord_x, coord_y])

        if int(line[3]) < -57:
            continue
        Q.put((int(line[3]) * -1, int(line[2])))

    fread.close()
    x = []
    y = []
    for i in coordList:
        x.append(i[0])
        y.append(i[1])

    plt.figure(figsize=(5, 11))
    plt.scatter(y, x, color='r')
    plt.axis([0, 5, 0, 11])
    plt.grid(True, axis='x')
    plt.grid(True, axis='y')
    plt.title("Minor : " + file[7:9])
    # plt.savefig("Minor : " + file[7:9])
    plt.show()
    plt.close()
    coordList.clear()


#   가장 강한 RSSI를 기준으로 RMS 계산
'''
    if line[0] != time:
        time = line[0]
        if Q.empty() == False:
            target = Q.get()[1]
            dist = math.sqrt(get_distance(target, int(file[7:9])))

            if max < dist:
                max = dist

            if min > dist:
                min = dist

            minorList.append(target)
            Q = PriorityQueue()
            # print(target)

        if int(line[3]) < -57:
            continue
    Q.put((int(line[3]) * -1, int(line[2])))

sum = 0.0
for i in minorList:
    sum += get_distance(i, int(file[7:9]))
'''

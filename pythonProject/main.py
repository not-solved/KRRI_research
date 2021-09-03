import csv
import os
import math
from queue import PriorityQueue

idx = [[-1, -1],
       [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1],
       [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1],
       [1, 4], [1, 3], [2, 3], [2, 4], [3, 4], [3, 3], [4, 3], [4, 4], [5, 4], [5, 3],
       [6, 3], [6, 4], [7, 4], [7, 3], [8, 3], [8, 4], [9, 4], [9, 3], [10, 3], [10, 4],
       [1, 2], [1, 1], [2, 1], [2, 2], [3, 2], [3, 1], [4, 1], [4, 2], [5, 2], [5, 1],
       [6, 1], [6, 2], [7, 2], [7, 1], [8, 1], [8, 2], [9, 2], [9, 1], [10, 1], [10, 2]]


#      Euclidean Distance
def get_distance(idx1, idx2):
    return pow((idx[idx1][0] - idx[idx2][0]) * 0.45, 2) + pow((idx[idx1][1] - idx[idx2][1]) * 0.45, 2)


#      파일 열기
filePath = "C:/Users/lab_408/Downloads/pythonProject/데이터 분석"
fileList = os.listdir(filePath)

rmsList = []
maxList = []
minList = []
idxList = []
for file in fileList:
       if file == "bias_analysis.py" or file == 'normdist.py' or file == 'record_analysis.py':
              continue

       fread = open(file, 'r', encoding='utf-8')
       rd = csv.reader(fread)

       time = ""
       target = ""
       max = 0
       min = 10
       minorList = []
       Q = PriorityQueue()

       for line in rd:
              if line[0] == 'TIME':
                     continue

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
              Q.put((int(line[3]) * -1, int(line[2])))

       sum = 0.0
       for i in minorList:
              sum += get_distance(i, int(file[7:9]))

       maxList.append(max)
       minList.append(min)
       rmsList.append(math.sqrt(sum / 900))
       idxList.append(file[7:9])
       fread.close()

max = 0
min = 10
avg = 0
for r in range(len(rmsList)):
       if max < rmsList[r]:
              max = rmsList[r]
       if min > rmsList[r]:
              min = rmsList[r]
       avg += rmsList[r]
       print(idxList[r] + "\tRMS : " + str(round(rmsList[r], 5)) +
             '\t\tMax : ' + str(round(maxList[r], 5)) +
             '\t\tMin : ' + str(minList[r]))

print("\n\n==============================  Total  ==============================")
print("Max : " + str(max))
print("Min : " + str(min))
print("Avg : " + str(avg / 40))

'''
#      normdist.py

import csv
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

filePath = "C:/Users/lab_408/Downloads/pythonProject/데이터 분석"
fileList = os.listdir(filePath)

rssi_recordAvg = np.empty(40)
rssi_recordMax = np.empty(40)
rssi_recordMin = np.empty(40)

rssi21 = []
x = np.array([
    [0, 0, 0, 0], [1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4 ,4 ,4 ,4],
    [5, 5, 5, 5], [6, 6, 6, 6], [7, 7, 7, 7], [8, 8, 8, 8], [9, 9, 9, 9]
])
y = np.array([
    [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3],
    [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]
])


for file in fileList:
    if file == 'record_analysis.py' or file == 'bias_analysis.py' or file == 'normdist.py':
        continue

    fread = open(file, 'r', encoding='utf-8')
    rd = csv.reader(fread)

    rssi_idx = ['21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
                '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
                '41', '42', '43', '44', '45', '46', '47', '48', '49', '50',
                '51', '52', '53', '54', '55', '56', '57', '58', '59', '60']
    rssi_cnt = np.empty(40, dtype=np.int)
    rssi_avg = np.empty(40)
    rssi_max = np.empty(40)
    rssi_min = np.empty(40)
    rssi_cnt.fill(0)
    rssi_avg.fill(0)
    rssi_max.fill(-100)
    rssi_min.fill(0)

    for line in rd:
        #   속성명 제외
        if line[0] == 'TIME':
            continue

        #   최대, 최소, 수신횟수 계산
        for idx in range(len(rssi_idx)):
            if rssi_idx[idx] == line[2]:
                rssi_cnt[idx] += 1
                rssi_avg[idx] += int(line[3])
                rssi21.append(int(line[3]))
                if rssi_max[idx] < int(line[3]):
                    rssi_max[idx] = int(line[3])
                if rssi_min[idx] > int(line[3]):
                    rssi_min[idx] = int(line[3])

    #   평균 계산
    for idx in range(len(rssi_idx)):
        rssi_avg[idx] = round((rssi_avg[idx] / rssi_cnt[idx]), 2)

    test = np.array([
        [rssi_avg[38], rssi_avg[39], rssi_avg[18], rssi_avg[19]],
        [rssi_avg[37], rssi_avg[36], rssi_avg[17], rssi_avg[16]],
        [rssi_avg[34], rssi_avg[35], rssi_avg[14], rssi_avg[15]],
        [rssi_avg[33], rssi_avg[32], rssi_avg[13], rssi_avg[12]],
        [rssi_avg[30], rssi_avg[31], rssi_avg[10], rssi_avg[11]],
        [rssi_avg[29], rssi_avg[28], rssi_avg[9], rssi_avg[8]],
        [rssi_avg[26], rssi_avg[27], rssi_avg[6], rssi_avg[7]],
        [rssi_avg[25], rssi_avg[24], rssi_avg[5], rssi_avg[4]],
        [rssi_avg[22], rssi_avg[23], rssi_avg[2], rssi_avg[3]],
        [rssi_avg[21], rssi_avg[20], rssi_avg[1], rssi_avg[0]],
    ])
        #   RSSI 평균 heatmap
    fig = plt.figure(figsize=(6, 8))
    ax = plt.subplot(1, 1, 1, projection='3d')
    ax.plot_surface(x, y, test, rstride=1, cstride=1)
    plt.show()

    #   각 블록에 위치했을 때의 최대, 최소, 평균치 기록
    for i in range(len(rssi_idx)):
        if rssi_idx[i] == file[7:9]:
            rssi_recordAvg[i] = rssi_avg[i]
            rssi_recordMax[i] = rssi_max[i]
            rssi_recordMin[i] = rssi_min[i]

    fread.close()

    #   plt.bar(rssi_idx, rssi_diff)
    #   plt.show()


#   각 블록에서의 RSSI 평균, 최대, 최소, 최대 최소 차이를 heatmap 으로 표시하기 위해 2차원 배열 처리
rssi_showAvg = np.array([
    [rssi_recordAvg[38], rssi_recordAvg[39], rssi_recordAvg[18], rssi_recordAvg[19]],
    [rssi_recordAvg[37], rssi_recordAvg[36], rssi_recordAvg[17], rssi_recordAvg[16]],
    [rssi_recordAvg[34], rssi_recordAvg[35], rssi_recordAvg[14], rssi_recordAvg[15]],
    [rssi_recordAvg[33], rssi_recordAvg[32], rssi_recordAvg[13], rssi_recordAvg[12]],
    [rssi_recordAvg[30], rssi_recordAvg[31], rssi_recordAvg[10], rssi_recordAvg[11]],
    [rssi_recordAvg[29], rssi_recordAvg[28], rssi_recordAvg[9], rssi_recordAvg[8]],
    [rssi_recordAvg[26], rssi_recordAvg[27], rssi_recordAvg[6], rssi_recordAvg[7]],
    [rssi_recordAvg[25], rssi_recordAvg[24], rssi_recordAvg[5], rssi_recordAvg[4]],
    [rssi_recordAvg[22], rssi_recordAvg[23], rssi_recordAvg[2], rssi_recordAvg[3]],
    [rssi_recordAvg[21], rssi_recordAvg[20], rssi_recordAvg[1], rssi_recordAvg[0]],
])
rssi_showMax = np.array([
    [rssi_recordMax[38], rssi_recordMax[39], rssi_recordMax[18], rssi_recordMax[19]],
    [rssi_recordMax[37], rssi_recordMax[36], rssi_recordMax[17], rssi_recordMax[16]],
    [rssi_recordMax[34], rssi_recordMax[35], rssi_recordMax[14], rssi_recordMax[15]],
    [rssi_recordMax[33], rssi_recordMax[32], rssi_recordMax[13], rssi_recordMax[12]],
    [rssi_recordMax[30], rssi_recordMax[31], rssi_recordMax[10], rssi_recordMax[11]],
    [rssi_recordMax[29], rssi_recordMax[28], rssi_recordMax[9], rssi_recordMax[8]],
    [rssi_recordMax[26], rssi_recordMax[27], rssi_recordMax[6], rssi_recordMax[7]],
    [rssi_recordMax[25], rssi_recordMax[24], rssi_recordMax[5], rssi_recordMax[4]],
    [rssi_recordMax[22], rssi_recordMax[23], rssi_recordMax[2], rssi_recordMax[3]],
    [rssi_recordMax[21], rssi_recordMax[20], rssi_recordMax[1], rssi_recordMax[0]],
])
rssi_showMin = np.array([
    [rssi_recordMin[38], rssi_recordMin[39], rssi_recordMin[18], rssi_recordMin[19]],
    [rssi_recordMin[37], rssi_recordMin[36], rssi_recordMin[17], rssi_recordMin[16]],
    [rssi_recordMin[34], rssi_recordMin[35], rssi_recordMin[14], rssi_recordMin[15]],
    [rssi_recordMin[33], rssi_recordMin[32], rssi_recordMin[13], rssi_recordMin[12]],
    [rssi_recordMin[30], rssi_recordMin[31], rssi_recordMin[10], rssi_recordMin[11]],
    [rssi_recordMin[29], rssi_recordMin[28], rssi_recordMin[9], rssi_recordMin[8]],
    [rssi_recordMin[26], rssi_recordMin[27], rssi_recordMin[6], rssi_recordMin[7]],
    [rssi_recordMin[25], rssi_recordMin[24], rssi_recordMin[5], rssi_recordMin[4]],
    [rssi_recordMin[22], rssi_recordMin[23], rssi_recordMin[2], rssi_recordMin[3]],
    [rssi_recordMin[21], rssi_recordMin[20], rssi_recordMin[1], rssi_recordMin[0]],
])
rssi_showAvg += 60
rssi_showDiff = rssi_showMax - rssi_showMin

'''

'''
import csv
import os
import math
import numpy as np
from queue import PriorityQueue
import matplotlib.pyplot as plt

idx = [[-1, -1],
       [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1],
       [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1],
       [0, 3], [0, 2], [1, 2], [1, 3], [2, 3], [2, 2], [3, 2], [3, 3], [4, 3], [4, 2],
       [5, 2], [5, 3], [6, 3], [6, 2], [7, 2], [7, 3], [8, 3], [8, 2], [9, 2], [9, 3],
       [0, 1], [0, 0], [1, 0], [1, 1], [2, 1], [2, 0], [3, 0], [3, 1], [4, 1], [4, 0],
       [5, 0], [5, 1], [6, 1], [6, 0], [7, 0], [7, 1], [8, 1], [8, 0], [9, 0], [9, 1]]

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
        j = i+1
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
filePath = "C:/Users/lab_408/Downloads/pythonProject/데이터 분석"
fileList = os.listdir(filePath)

rmsList = []
maxList = []
minList = []
idxList = []
coordList = []
for file in fileList:
    if file == "codes" or file == 'normdist.py':
        continue

    fread = open(file, 'r', encoding='utf-8')
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

            while len(minor_list) > 8:
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

            coord_x /= 8
            coord_y /= 8
            coordList.append([coord_x, coord_y])

        Q.put((int(line[3]) * -1, int(line[2])))

    for i in coordList:
        print(i)

    fread.close()
    x = []
    y = []
    for i in coordList:
        x.append(i[0])
        y.append(i[1])

    plt.figure(figsize=(3, 8))
    plt.scatter(y, x, color='r')
    plt.axis([0, 3, 0, 9])
    plt.grid(True, axis='x')
    plt.grid(True, axis='y')
    plt.title("Minor : " + file[7:9])
    plt.show()
    coordList.clear()

'''
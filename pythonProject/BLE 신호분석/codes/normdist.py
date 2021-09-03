import csv
import os
import math
import numpy as np
from queue import PriorityQueue

idx = [[-1, -1],
       [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1],
       [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1],
       [1, 4], [1, 3], [2, 3], [2, 4], [3, 4], [3, 3], [4, 3], [4, 4], [5, 4], [5, 3],
       [6, 3], [6, 4], [7, 4], [7, 3], [8, 3], [8, 4], [9, 4], [9, 3], [10, 3], [10, 4],
       [1, 2], [1, 1], [2, 1], [2, 2], [3, 2], [3, 1], [4, 1], [4, 2], [5, 2], [5, 1],
       [6, 1], [6, 2], [7, 2], [7, 1], [8, 1], [8, 2], [9, 2], [9, 1], [10, 1], [10, 2]]


distMatrix = []
for i in range(0, 61):
    distMatrix.append(np.zeros(61))


#      Euclidean Distance
def get_distance(idx1, idx2):
    return pow((idx[idx1][0] - idx[idx2][0]) * 0.45, 2) + pow((idx[idx1][1] - idx[idx2][1]) * 0.45, 2)

def get_distance_by_coord(coord1, coord2):
    return pow((coord1[0] - coord2[0]) * 0.45, 2) + pow((coord1[1] - coord2[1]) * 0.45, 2)

#      파일 열기
filePath = "C:/Users/lab_408/Downloads/pythonProject/데이터 분석"
fileList = os.listdir(filePath)

rmsList = []
maxList = []
minList = []
idxList = []
coordList = []
for file in fileList:
    if len(file) < 20:
        continue

    fread = open(file, 'r', encoding='utf-8')
    rd = csv.reader(fread)


    time = ""
    target = ""
    max = 0
    min = 10
    minorList = []
    Matrix = []
    Q = PriorityQueue()

    for line in rd:
        if line[0] == 'TIME':
            continue

        #   가장 강한 RSSI를 기준으로 RMS 계산
        #   (여기에 코드 복사)

        #   여러 좌표를 바탕으로 위치 측정 후 RMS 계산
        if line[0] != time:
            time = line[0]
            if Q.empty():
                continue

            minorList.clear()
            while not Q.empty():
                value = Q.get()
                if len(minorList) <= 8:
                    minorList.append(value)

            distance = 0
            Matrix.clear()
            for i in range(0, 61):
                Matrix.append(np.zeros(61))

            for i in range(len(minorList)):
                j = i + 1
                while j < len(minorList):
                    distance = math.sqrt(get_distance(minorList[i][1], minorList[j][1]))
                    Matrix[minorList[i][1]][minorList[j][1]] = distance
                    Matrix[minorList[j][1]][minorList[i][1]] = distance
                    Matrix[minorList[i][1]][0] += (distance * -1)
                    Matrix[minorList[j][1]][0] += (distance * -1)
                    j += 1

            while len(minorList) > 3:
                tempMax = 0
                target = 0
                for i in range(len(minorList)):
                    if Matrix[minorList[i][1]][0] * -1 > tempMax:
                        tempMax = Matrix[minorList[i][1]][0] * -1
                        target = minorList[i]
                minorList.remove(target)

                for i in range(len(minorList)):
                    Matrix[minorList[i][1]][0] -= Matrix[minorList[i][1]][target[1]]


            coord_x = 0
            coord_y = 0

            #   RSSI를 무시하는 경우
            '''
            for i in range(len(minorList)):
                coord_x += idx[minorList[i][1]][0]
                coord_y += idx[minorList[i][1]][1]
                
            coord_x /= len(minorList)
            coord_y /= len(minorList)
            '''

            #   RSSI에 가중치를 반영하는 경우
            weightQueue = PriorityQueue()

            for i in minorList:
                weightQueue.put(i)

            weight = [5, 3, 2]
            weightIdx = 0
            totalWeight = 0
            while not weightQueue.empty():
                value = weightQueue.get()
                coord_x += idx[value[1]][0] * weight[weightIdx]
                coord_y += idx[value[1]][1] * weight[weightIdx]
                totalWeight += weight[weightIdx]
                weightIdx += 1

            coord_x /= totalWeight
            coord_y /= totalWeight
            coordList.append([coord_x, coord_y])

            distance = math.sqrt(get_distance_by_coord([coord_x, coord_y], idx[int(file[7:9])]))
            if max < distance:
                max = distance

            if min > distance:
                min = distance


        if int(line[3]) < -57:
            continue
        Q.put((int(line[3]) * -1, int(line[2])))

    sum = 0.0
    for i in coordList:
        sum += get_distance_by_coord(i, idx[int(file[7:9])])

    maxList.append(max)
    minList.append(min)
    rmsList.append(math.sqrt(sum / 900))
    idxList.append(file[7:9])
    coordList.clear()
    fread.close()

fwrite = open("RMS result.csv", 'w', encoding='utf-8')
wr = csv.writer(fwrite, lineterminator='\n')
wr.writerow(['Block No.', 'RMS', 'Max', 'Min', '\n'])



max = 0
min = 10
avg = 0
for r in range(len(rmsList)):
    if max < rmsList[r]:
        max = rmsList[r]
    if min > rmsList[r]:
        min = rmsList[r]
    avg += rmsList[r]
    print(idxList[r] + "\tRMS : ", '%.4f' % round(rmsList[r], 4),
          '\t\tMax : ', '%.4f' % round(maxList[r], 4),
          '\t\tMin : ', round(minList[r], 4))
    wr.writerow([r + 21, round(rmsList[r], 4), round(maxList[r], 4), round(minList[r], 4), '\n'])


print("\n\n==============================  Total  ==============================")
print("Max : ", round(max, 4))
print("Min : ", round(min, 4))
print("Avg : ", round(avg / 40, 4))
wr.writerow(["Total=====================================================", '\n'])
wr.writerow(["Max : ", round(max, 4), '\n'])
wr.writerow(["Min : ", round(min, 4), '\n'])
wr.writerow(["Avg : ", round(avg / 40, 4), '\n'])

fwrite.close()

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


'''
import numpy as np
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
filePath = "C:/Users/lab_408/Downloads/pythonProject/데이터 분석"
fileList = os.listdir(filePath)

rmsList = []
maxList = []
minList = []
idxList = []
coordList = []
for file in fileList:
    if file == "codes" or file == 'normdist.py' or file == "Minor ":
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

    plt.figure(figsize=(3, 8))
    plt.scatter(y, x, color='r')
    plt.axis([0, 3, 0, 9])
    plt.grid(True, axis='x')
    plt.grid(True, axis='y')
    plt.title("Minor : " + file[7:9])
    plt.show()
    coordList.clear()

'''

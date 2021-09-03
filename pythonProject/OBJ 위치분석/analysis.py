import csv
import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

fileList = ['task1.csv', 'task2.csv', 'task3.csv', 'task4.csv']
m35 = np.zeros(5)
m36 = np.zeros(5)
m37 = np.zeros(5)
m38 = np.zeros(5)
m39 = np.zeros(5)
m40 = np.zeros(5)
m56 = np.zeros(5)
m57 = np.zeros(5)
m60 = np.zeros(5)


#   로드셀 배열 초기화
def initialize_List():
    m35.fill(0)
    m36.fill(0)
    m37.fill(0)
    m38.fill(0)
    m39.fill(0)
    m40.fill(0)
    m56.fill(0)
    m57.fill(0)
    m60.fill(0)


for file in fileList:
    fread = open(file, 'r', encoding='utf-8')
    rd = csv.reader(fread)

    initialize_List()
    idx = 1
    for line in rd:
        #   첫 줄은 넘긴다
        if line[0] == 'board_id':
            continue

        #   다음 상태를 읽는다다
        if line[0] == "Break":
            Matrix = [
                [m60[2] / m60[4], m60[3] / m60[4], m39[2] / m39[4], m39[3] / m39[4], m40[2] / m40[4], m40[3] / m40[4]],
                [m60[1] / m60[4], m60[0] / m60[4], m39[1] / m39[4], m39[0] / m39[4], m40[1] / m40[4], m40[0] / m40[4]],
                [m57[2] / m57[4], m57[3] / m57[4], m38[2] / m38[4], m38[3] / m38[4], m37[2] / m37[4], m37[3] / m37[4]],
                [m57[1] / m57[4], m57[0] / m57[4], m38[1] / m38[4], m38[0] / m38[4], m37[1] / m37[4], m37[0] / m37[4]],
                [m56[2] / m56[4], m56[3] / m56[4], m35[2] / m35[4], m35[3] / m35[4], m36[2] / m36[4], m36[3] / m36[4]],
                [m56[1] / m56[4], m56[0] / m56[4], m35[1] / m35[4], m35[0] / m35[4], m36[1] / m36[4], m36[0] / m36[4]]
            ]
            plt.figure(figsize=(7, 6))
            sns.heatmap(Matrix, linewidth=1.5, cmap='Greys', annot=True, fmt=".0f")

            plt.title(file + '_' + str(idx) + '\n\n')
            plt.savefig(file + '_' + str(idx) + ".png")
            plt.close()

            initialize_List()
            idx += 1
            continue

        if line[4] == '35':
            m35 += [int(line[5]), int(line[6]), int(line[7]), int(line[8]), 1]
        elif line[4] == '36':
            m36 += [int(line[5]), int(line[6]), int(line[7]), int(line[8]), 1]
        elif line[4] == '37':
            m37 += [int(line[5]), int(line[6]), int(line[7]), int(line[8]), 1]
        elif line[4] == '38':
            m38 += [int(line[5]), int(line[6]), int(line[7]), int(line[8]), 1]
        elif line[4] == '39':
            m39 += [int(line[5]), int(line[6]), int(line[7]), int(line[8]), 1]
        elif line[4] == '40':
            m40 += [int(line[5]), int(line[6]), int(line[7]), int(line[8]), 1]
        elif line[4] == '56':
            m56 += [int(line[5]), int(line[6]), int(line[7]), int(line[8]), 1]
        elif line[4] == '57':
            m57 += [int(line[5]), int(line[6]), int(line[7]), int(line[8]), 1]
        elif line[4] == '60':
            m60 += [int(line[5]), int(line[6]), int(line[7]), int(line[8]), 1]

    fread.close()


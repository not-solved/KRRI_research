import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

filePath = os.getcwd() + '/Dataset/'
fileList = os.listdir(filePath)

rssi_recordAvg = np.empty(40)
rssi_recordMax = np.empty(40)
rssi_recordMin = np.empty(40)

for file in fileList:

    fread = open(filePath + file, 'r', encoding='utf-8')
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
                if rssi_max[idx] < int(line[3]):
                    rssi_max[idx] = int(line[3])
                if rssi_min[idx] > int(line[3]):
                    rssi_min[idx] = int(line[3])

    #   평균 계산
    for idx in range(len(rssi_idx)):
        rssi_avg[idx] = round((rssi_avg[idx] / rssi_cnt[idx]), 2)

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
rssi_showDiff = rssi_showMax - rssi_showMin

totalAvg = 0
for i in rssi_recordAvg:
    totalAvg += rssi_recordAvg;

print(totalAvg / 40)

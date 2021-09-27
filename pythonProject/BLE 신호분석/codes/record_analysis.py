import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

filePath = os.getcwd() + '/Dataset/'
fileList = os.listdir(filePath)

for file in fileList:

    fread = open(filePath + file, 'r', encoding='utf-8')
    rd = csv.reader(fread)
    # fwrite = open(file[:9] + '_analysis.csv', 'w', encoding='utf-8')
    # wr = csv.writer(fwrite, lineterminator='\n')

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

    #   평균치 계산
    for idx in range(len(rssi_idx)):
        rssi_avg[idx] = round((rssi_avg[idx] / rssi_cnt[idx]), 2)

    fread.close()
    #   fwrite 쓰기
    '''
    #   csv 파일 입력 포맷에 맞게 배열 구성
    data_record = [
        ['59', '60', '39', '40', '',
         '59', '60', '39', '40', '',
         '59', '60', '39', '40', '',
         '59', '60', '39', '40', '\n'
         ],
        [rssi_avg[38], rssi_avg[39], rssi_avg[18], rssi_avg[19], '',
         rssi_max[38], rssi_max[39], rssi_max[18], rssi_max[19], '',
         rssi_min[38], rssi_min[39], rssi_min[18], rssi_min[19], '',
         rssi_cnt[38], rssi_cnt[39], rssi_cnt[18], rssi_cnt[19], ''
         ],
        ['58', '57', '38', '37', '',
         '58', '57', '38', '37', '',
         '58', '57', '38', '37', '',
         '58', '57', '38', '37', '\n'
         ],
        [rssi_avg[37], rssi_avg[36], rssi_avg[17], rssi_avg[16], '',
         rssi_max[37], rssi_max[36], rssi_max[17], rssi_max[16], '',
         rssi_min[37], rssi_min[36], rssi_min[17], rssi_min[16], '',
         rssi_cnt[37], rssi_cnt[36], rssi_cnt[17], rssi_cnt[16], '',
         ],
        ['55', '56', '35', '36', '',
         '55', '56', '35', '36', '',
         '55', '56', '35', '36', '',
         '55', '56', '35', '36', '\n'
         ],
        [rssi_avg[34], rssi_avg[35], rssi_avg[14], rssi_avg[15], '',
         rssi_max[34], rssi_max[35], rssi_max[14], rssi_max[15], '',
         rssi_min[34], rssi_min[35], rssi_min[14], rssi_min[15], '',
         rssi_cnt[34], rssi_cnt[35], rssi_cnt[14], rssi_cnt[15], '',
         ],
        ['54', '53', '34', '33', '',
         '54', '53', '34', '33', '',
         '54', '53', '34', '33', '',
         '54', '53', '34', '33', '\n'
         ],
        [rssi_avg[33], rssi_avg[32], rssi_avg[13], rssi_avg[12], '',
         rssi_max[33], rssi_max[32], rssi_max[13], rssi_max[12], '',
         rssi_min[33], rssi_min[32], rssi_min[13], rssi_min[12], '',
         rssi_cnt[33], rssi_cnt[32], rssi_cnt[13], rssi_cnt[12], '',
         ],
        ['51', '52', '31', '32', '',
         '51', '52', '31', '32', '',
         '51', '52', '31', '32', '',
         '51', '52', '31', '32', '\n'
         ],
        [rssi_avg[30], rssi_avg[31], rssi_avg[10], rssi_avg[11], '',
         rssi_max[30], rssi_max[31], rssi_max[10], rssi_max[11], '',
         rssi_min[30], rssi_min[31], rssi_min[10], rssi_min[11], '',
         rssi_cnt[30], rssi_cnt[31], rssi_cnt[10], rssi_cnt[11], '',
         ],
        ['50', '49', '30', '29', '',
         '50', '49', '30', '29', '',
         '50', '49', '30', '29', '',
         '50', '49', '30', '29', '\n'
         ],
        [rssi_avg[29], rssi_avg[28], rssi_avg[9], rssi_avg[8], '',
         rssi_max[29], rssi_max[28], rssi_max[9], rssi_max[8], '',
         rssi_min[29], rssi_min[28], rssi_min[9], rssi_min[8], '',
         rssi_cnt[29], rssi_cnt[28], rssi_cnt[9], rssi_cnt[8], '',
         ],
        ['47', '48', '27', '28', '',
         '47', '48', '27', '28', '',
         '47', '48', '27', '28', '',
         '47', '48', '27', '28', '\n'
         ],
        [rssi_avg[26], rssi_avg[27], rssi_avg[6], rssi_avg[7], '',
         rssi_max[26], rssi_max[27], rssi_max[6], rssi_max[7], '',
         rssi_min[26], rssi_min[27], rssi_min[6], rssi_min[7], '',
         rssi_cnt[26], rssi_cnt[27], rssi_cnt[6], rssi_cnt[7], '',
         ],
        ['46', '45', '26', '25', '',
         '46', '45', '26', '25', '',
         '46', '45', '26', '25', '',
         '46', '45', '26', '25', '\n'
         ],
        [rssi_avg[25], rssi_avg[24], rssi_avg[5], rssi_avg[4], '',
         rssi_max[25], rssi_max[24], rssi_max[5], rssi_max[4], '',
         rssi_min[25], rssi_min[24], rssi_min[5], rssi_min[4], '',
         rssi_cnt[25], rssi_cnt[24], rssi_cnt[5], rssi_cnt[4], '',
         ],
        ['43', '44', '23', '24', '',
         '43', '44', '23', '24', '',
         '43', '44', '23', '24', '',
         '43', '44', '23', '24', '\n'
         ],
        [rssi_avg[22], rssi_avg[23], rssi_avg[2], rssi_avg[3], '',
         rssi_max[22], rssi_max[23], rssi_max[2], rssi_max[3], '',
         rssi_min[22], rssi_min[23], rssi_min[2], rssi_min[3], '',
         rssi_cnt[22], rssi_cnt[23], rssi_cnt[2], rssi_cnt[3], '',
         ],
        ['42', '41', '22', '21', '',
         '42', '41', '22', '21', '',
         '42', '41', '22', '21', '',
         '42', '41', '22', '21', '\n'
         ],
        [rssi_avg[21], rssi_avg[20], rssi_avg[1], rssi_avg[0], '',
         rssi_max[21], rssi_max[20], rssi_max[1], rssi_max[0], '',
         rssi_min[21], rssi_min[20], rssi_min[1], rssi_min[0], '',
         rssi_cnt[21], rssi_cnt[20], rssi_cnt[1], rssi_cnt[0], '',
         ],
    ]

    #   csv 파일에 쓰기
    wr.writerow(['Base', file[7:9]])
    wr.writerow([''])
    wr.writerow(['Average RSSI', '', '', '', '', 'Max RSSI', '', '', '', '', 'Min RSSI', '', '', '', '', 'Cnt'])
    for i in data_record:
        wr.writerow(i)

    #   파일 읽기, 쓰기 종료
    fread.close()
    fwrite.close()
    '''

    #   avg, max, min 수치 출력
    '''
    for idx in range(len(rssi_idx)):
        print(rssi_idx[idx] + "  (" + str(rssi_cnt[idx]) + ")\t=================================")
        print("Average : " + str(rssi_avg[idx]))
        print("Max : " + str(rssi_max[idx]))
        print("Min : " + str(rssi_min[idx]))
    '''

    #   seaborn 으로 시각화 하기 위해 데이터를 2차원 배열 형태로 정리
    result_avg = np.array([
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
    result_cnt = np.array([
        [rssi_cnt[38], rssi_cnt[39], rssi_cnt[18], rssi_cnt[19]],
        [rssi_cnt[37], rssi_cnt[36], rssi_cnt[17], rssi_cnt[16]],
        [rssi_cnt[34], rssi_cnt[35], rssi_cnt[14], rssi_cnt[15]],
        [rssi_cnt[33], rssi_cnt[32], rssi_cnt[13], rssi_cnt[12]],
        [rssi_cnt[30], rssi_cnt[31], rssi_cnt[10], rssi_cnt[11]],
        [rssi_cnt[29], rssi_cnt[28], rssi_cnt[9], rssi_cnt[8]],
        [rssi_cnt[26], rssi_cnt[27], rssi_cnt[6], rssi_cnt[7]],
        [rssi_cnt[25], rssi_cnt[24], rssi_cnt[5], rssi_cnt[4]],
        [rssi_cnt[22], rssi_cnt[23], rssi_cnt[2], rssi_cnt[3]],
        [rssi_cnt[21], rssi_cnt[20], rssi_cnt[1], rssi_cnt[0]],
    ])

    #   RSSI 신호 평균치 시각화
    fig = plt.figure(figsize=(6, 8))
    fig.set_facecolor('white')

    sns.heatmap(result_avg, linewidth=1.5, cmap='Greys', annot=True)
    plt.title('Minor : ' + file[7:9] + '\n\n')
    plt.savefig("Average_" + file[7:9] + ".png")
    plt.close()

    #   RSSI 신호 수신 횟수 시각화
    fig = plt.figure(figsize=(6, 8))
    fig.set_facecolor('white')

    sns.heatmap(result_cnt, linewidth=1.5, cmap='Greys', annot=True, fmt='d')
    plt.title('Minor : ' + file[7:9] + '\n\n')
    plt.savefig("Count_" + file[7:9] + ".png")
    plt.close()

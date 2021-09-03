import os
import csv
import numpy as np

path_dir = "C:/Users/lab_408/downloads/pythonProject/데이터 작업"
filelist = os.listdir(path_dir)

for i in filelist:
    if i == "Get_Average.py" or i == "File_readAndWrite.py":
        continue

    fread = open(i, 'r', encoding='utf-8')
    rdr = csv.reader(fread)

    fwrite = open(i[:21] + '_average.csv', 'w', encoding='utf-8')
    wr = csv.writer(fwrite, lineterminator='\n')

    print(i[:21])
    rssi_idx = ['21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
                '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
                '41', '42', '43', '44', '45', '46', '47', '48', '49', '50',
                '51', '52', '53', '54', '55', '56', '57', '58', '59', '60']
    rssi_cnt = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype='i')
    rssi_avg = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype='f')

    Max_RSSI = -100;
    Max_MINOR = ""

    for line in rdr:
        if line[3] == 'Rssi':
            wr.writerow(["minor", "RSSI avg"])
            continue

        for idx in range(len(rssi_idx)):
            if rssi_idx[idx] == line[2]:
                rssi_cnt[idx] += 1
                rssi_avg[idx] += int(line[3])

    for idx in range(len(rssi_idx)):
        rssi_avg[idx] = round(rssi_avg[idx]/rssi_cnt[idx], 2)
        if Max_RSSI < rssi_avg[idx] :
            Max_RSSI = rssi_avg[idx]
            Max_MINOR = rssi_idx[idx]
        print(rssi_idx[idx], rssi_avg[idx])

    wr.writerow(["Base", i[7:9]])
    wr.writerow(["MAX", Max_MINOR, "(" + str(Max_RSSI) + ")"])
    wr.writerow(['\n'])

    wr.writerow(['59', '60', '39', '40'])
    wr.writerow([rssi_avg[38], rssi_avg[39], rssi_avg[18], rssi_avg[19], '\n'])
    wr.writerow(['58', '57', '38', '37'])
    wr.writerow([rssi_avg[37], rssi_avg[36], rssi_avg[17], rssi_avg[16], '\n'])

    wr.writerow(['55', '56', '35', '36'])
    wr.writerow([rssi_avg[34], rssi_avg[35], rssi_avg[14], rssi_avg[15], '\n'])
    wr.writerow(['54', '53', '34', '33'])
    wr.writerow([rssi_avg[33], rssi_avg[32], rssi_avg[13], rssi_avg[12], '\n'])

    wr.writerow(['51', '52', '31', '32'])
    wr.writerow([rssi_avg[30], rssi_avg[31], rssi_avg[10], rssi_avg[11], '\n'])
    wr.writerow(['50', '49', '30', '29'])
    wr.writerow([rssi_avg[29], rssi_avg[28], rssi_avg[9], rssi_avg[8], '\n'])

    wr.writerow(['47', '48', '27', '28'])
    wr.writerow([rssi_avg[26], rssi_avg[27], rssi_avg[6], rssi_avg[7], '\n'])
    wr.writerow(['46', '45', '26', '25'])
    wr.writerow([rssi_avg[25], rssi_avg[24], rssi_avg[5], rssi_avg[4], '\n'])

    wr.writerow(['43', '44', '23', '24'])
    wr.writerow([rssi_avg[22], rssi_avg[23], rssi_avg[2], rssi_avg[3], '\n'])
    wr.writerow(['42', '41', '22', '21'])
    wr.writerow([rssi_avg[21], rssi_avg[20], rssi_avg[1], rssi_avg[0], '\n'])

    fread.close()
    fwrite.close()
import csv
import os
import math
import numpy as np
from queue import PriorityQueue

filePath = os.getcwd() + '/Dataset/'
fileList = os.listdir(filePath)

RSSI_MAP = []
COORD_IDX = [
    [1, 4], [1, 3], [2, 3], [2, 4], [3, 4], [3, 3], [4, 3], [4, 4], [5,  4], [5,  3],
    [6, 3], [6, 4], [7, 4], [7, 3], [8, 3], [8, 4], [9, 4], [9, 3], [10, 3], [10, 4],
    [1, 2], [1, 1], [2, 1], [2, 2], [3, 2], [3, 1], [4, 1], [4, 2], [5,  2], [5,  1],
    [6, 1], [6, 2], [7, 2], [7, 1], [8, 4], [8, 2], [9, 2], [9, 1], [10, 1], [10, 2]
]


#   RSSI MAP 초기화 함수
def initialize_rssi_map():
    RSSI_MAP.clear()
    for initialize_idx in range(0, 40):
        RSSI_MAP.append(np.zeros(40))


#   RSSI 값을 이용한 Euclidean Distance 거리 계산 후 최소의 D 반환
def get_distance_by_RSSI(test_set):

    minors = []
    for beacons in test_set:
        minors.append(beacons[2])

    pq = PriorityQueue()
    for i in minors:
        dist = 0
        for j in test_set:
            dist += math.pow(RSSI_MAP[i - 21][j[2] - 21] - j[3], 2)

        #   (거리값, 해당 기준 위치)
        #   거리 기준으로 정렬하여, 우선순위 큐 머리에는 최소 거리에 해당하는 값이 있다.
        pq.put([math.sqrt(dist), i])

    return pq.get()


#   에러에서 발생한 RMS 계산 함수
def get_RMS(error_set):
    #   에러가 없을 경우
    if len(error_set) == 0:
        return 0.0
    answer = 0
    for err in error_set:
        dist = pow((COORD_IDX[err[0] - 21][0] - COORD_IDX[err[1] - 21][0]) * 0.45, 2) + pow((COORD_IDX[err[0] - 21][1] - COORD_IDX[err[1] - 21][1]) * 0.45, 2)
        answer += dist

    return round(math.sqrt(answer / len(error_set)), 4)


#   K-Fold 검증 및 결과 출력
def k_fold_validation_result(test_list):

    #   K = n에 대한 결과 측정
    correct = 0
    total = 0
    group = []
    minor = 0
    base_time = "no record"
    error_group = []

    #   각각의 기준 블록(Base)에 대한 결과 측정
    each_minor_result = []
    temp_correct = 0
    temp_total = 0
    temp_result = []
    temp_error = []

    #   테스트 데이터를 이용하여 K-fold validation 진행
    #   test -> (time, base(기준 위치), minor(측정 위치), RSSI)
    for test in test_list:
        
        #   각 Base 별 정확도, RMS 계산
        if minor != test[1]:
            if minor != 0:
                #   accuracy, rms
                each_minor_result.append([round(temp_correct / temp_total, 4), get_RMS(temp_error)])
                temp_correct = 0
                temp_total = 0
                temp_result.clear()
                temp_error.clear()
            minor = test[1]
        
        #   시간 주기를 구분지어 핑거프린팅 방식의 거리측정 진행
        if base_time == "no record":
            base_time = test[0]
        elif base_time != test[0]:
            base_time = test[0]
            result = get_distance_by_RSSI(group)
            # print(test, result)
            group.clear()
            if minor == result[1]:
                correct += 1
                temp_correct += 1
            else:
                #   (base, result)
                error_group.append([minor, result[1]])
                temp_error.append([minor, result[1]])
            total += 1
            temp_total += 1
        #   각 시간 주기별 평가용 정보(group), 21 ~ 60번 각각의 블록 결과 처리용 정보(temp_result)
        group.append(test)
        temp_result.append(test)

    #   미처 정보를 담지 못할 경우 처리
    if minor == 60:
        each_minor_result.append([round(temp_correct / temp_total, 4), get_RMS(temp_error)])

    #   K = n 전체 (21 ~ 60번 블록 모든 정보)에 대한 정확도, RMS 평가
    accuracy = round(correct / total, 4)
    rms_result = get_RMS(error_group)
    return accuracy, rms_result, each_minor_result


acc_data = [0, 100, 0]
rms_data = [0, 100, 0]


#   K-fold 교차검증 (K = 10)
for loop in range(1, 11):

    #   매번 RSSI MAP을 초기화한다.
    initialize_rssi_map()
    test_data = []

    for file in fileList:
        #   데이터 파일이 아니면 넘긴다
        if len(file) != 25:
            continue

        RSSI_CNT = np.zeros(40)

        base = int(file[7:9])
        content = []
        diff_time_cnt = 0
        total_cnt = 1

        temp_file = open(filePath + file, 'r', encoding='utf-8')
        rd = csv.reader(temp_file)
        time = "no record"

        #   파일 내용을 읽어 시간주기 90개 단위로 10번 나눠 기록
        for line in rd:
            #   속성 줄은 건너뛴다
            if line[0] == 'TIME':
                continue
            #   마지막 줄은 무시한다
            elif line[0] == 'END':
                break

            #   같은 시간대로 구분
            if time != line[0]:
                if time == "no record":
                    time = line[0]
                else:
                    diff_time_cnt += 1
                    if diff_time_cnt % 90 == 0:
                        total_cnt += 1
                    content.clear()
                    time = line[0]

            #   K 번째 루프에 해당될 경우 테스트 데이터로 활용
            #   time, base(실제 위치), minor(측정 위치), RSSI
            if total_cnt == loop:
                test_data.append([line[0], int(line[1]), int(line[2]), int(line[3])])
            #   그 외의 경우는 RSSI MAP 구성에 활용
            else:
                RSSI_MAP[int(line[1]) - 21][int(line[2]) - 21] += int(line[3])
                RSSI_CNT[int(line[2]) - 21] += 1

        for idx in range(len(RSSI_CNT)):
            if RSSI_CNT[idx] == 0:  # Zero division 방지
                continue
            RSSI_MAP[base - 21][idx] = round(RSSI_MAP[base - 21][idx] / RSSI_CNT[idx], 4)

        temp_file.close()

    write_file = open("K_fold_validation_" + str(loop) + '.csv', 'w', encoding='utf-8', newline='')
    wr = csv.writer(write_file)


    #   n번째 K-fold 교차검증 결과 확인 및 블록 별 정확도 및 RMS 결과 확인
    acc, rms, currentResult = k_fold_validation_result(test_data)
    print("K - ", loop, "  \t\tAccuracy : ", acc, "\t\tRMS : ", rms)
    print("-------------------------------------------------------------")
    wr.writerow(["Acc_total", acc, "RMS_total", rms])
    wr.writerow(["Minor", "Accuracy", "RMS"])

    #   블록 별 정확도 및 RMS 결과 확인
    resultIdx = 21
    for tempResult in currentResult:
        print("\t\t", resultIdx, " -\tAccuracy : ", tempResult[0], "  \t\tRMS : ", tempResult[1])
        wr.writerow([resultIdx, tempResult[0], tempResult[1]])
        resultIdx += 1
    print("=============================================================\n")
    if acc_data[0] < acc:
        acc_data[0] = acc
    if acc_data[1] > acc:
        acc_data[1] = acc
    acc_data[2] += acc

    if rms_data[0] < rms:
        rms_data[0] = rms
    if rms_data[1] > rms:
        rms_data[1] = rms
    rms_data[2] += rms

    write_file.close()

#   최종 결과 확인
acc_data[2] = round(acc_data[2] / 10, 5)
rms_data[2] = round(rms_data[2] / 10, 5)
print("=============================================================")
print("Accuracy - \tMAX : ", acc_data[0], "  \tMIN : ", acc_data[1], "  \tAVG : ", acc_data[2])
print("RMS      - \tMAX : ", rms_data[0], "  \tMIN : ", rms_data[1], "  \tAVG : ", rms_data[2])

import csv
from queue import PriorityQueue


#   블록 위치별 평균 RSSI 값의 평균을 편차 계산의 기준으로 삼는다
#   Map : RSSI_MAP
def get_Avg(Map):
    result = 0
    for idx in range(1, 41):
        result += Map[idx - 1][idx]

    result /= 40
    print("Avg : ", result)
    return result


#   블록 위치 별 평균 RSSI 값의 중간값을 편차 계산의 기준으로 삼는다.
#   Map : RSSI_MAP
def get_Mid(Map):
    avg_container = PriorityQueue()
    #   RSSI 수치와 해당 위치를 함께 큐에 저장
    for idx in range(0, 40):
        avg_container.put([Map[idx][idx + 1], Map[idx][0]])

    total_size = avg_container.qsize()

    while avg_container.qsize() > (total_size / 2):
        avg_container.get()

    result = avg_container.get()[0]
    print("Mid : ", result)
    return result


read_file = open('RSSI_MAP.csv', 'r', encoding='utf-8')
rd = csv.reader(read_file)

write_file = open('bias_adjust.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(write_file)

rssi_map = []

#   rd : RSSI_MAP 파일에서 읽는 내용
for content in rd:
    #   속성 행은 그대로 입력
    if content[0] == 'Base Minor':
        wr.writerow(content)
        continue
    #   RSSI 수치들은 기준 RSSI 번호(첫 값)과 나머지 40개 (값들이 입력될 칸들)으로 받는다.
    else:
        rssi_container = [int(content[0]), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(1, 41):
            rssi_container[i] = float(content[i])
        rssi_map.append(rssi_container)

avg = get_Avg(rssi_map)     # -51.55265533749999
mid = get_Mid(rssi_map)     # -50.36956522

diff = avg
#   수치 조정 및 조정값 파일에 작성
for rssi in rssi_map:
    Bias = rssi[rssi[0] - 20] - diff
    for j in range(1, 41):
        rssi[j] = round(rssi[j] - Bias, 5)
    wr.writerow(rssi)

read_file.close()
write_file.close()

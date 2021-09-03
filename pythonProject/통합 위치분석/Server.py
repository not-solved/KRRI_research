#   저장된 파일의 포맷을 재변환 (한줄로 표현)
'''
import csv

# file_dir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/'
# file_list = os.listdir(file_dir)
file_list = ['Location_result_300.csv', 'Location_result_500.csv']

for file in file_list:
    if len(file) <= 20:
        continue

    file_read = open(file, 'r', encoding='utf-8')
    file_reader = csv.reader(file_read)

    file_write = open("Location_unify_" + file[16:19] + '.csv', 'w', encoding='utf-8', newline='')
    file_writer = csv.writer(file_write)

    time = ""
    container = []
    time_included = False
    for line in file_reader:
        if line[0] == 'reg_dt':
            container.append('reg_dt')
            for minor in range(21, 61):
                container.append(str(minor) + '_' + line[2])
                container.append(str(minor) + '_' + line[3])
                container.append(str(minor) + '_' + line[4])
                container.append(str(minor) + '_' + line[5])
                container.append(str(minor) + '_' + line[6])
            file_writer.writerow(container)
            container.clear()
            continue

        if time != line[0]:
            if time == "":
                time = line[0]
            else:
                time = line[0]
                file_writer.writerow(container)
                time_included = False
                container.clear()

        if not time_included:
            time_included = True
            container.append(line[0])
        for i in range(2, 7):
            container.append(line[i])

    file_read.close()
    file_write.close()
'''

#   MySQL 서버에서 데이터를 읽어 하나의 파일로 저장
'''
import pymysql
import datetime
import csv
from datetime import timedelta

baseTime_2 = datetime.datetime(2021, 8, 27, 10, 26, 36, 0)
baseTime_2_end = datetime.datetime(2021, 8, 27, 10, 28, 4, 0)

DB = pymysql.connect(
    user='krri',
    passwd='Mobility408',
    host='192.168.10.193',
    db='smartBlock',
    charset='utf8'
)


BLE_cursor = DB.cursor(pymysql.cursors.DictCursor)
LC_cursor = DB.cursor(pymysql.cursors.DictCursor)

SQL_1_SELECT = 'SELECT minor, rssi, reg_dt FROM sb_user_block_ble '
SQL_2_SELECT = 'SELECT minor, lc1, lc2, lc3, lc4, reg_dt FROM sb_block_lc '
Time_interval = 300

FileWrite = open('Location_result__' + str(Time_interval) + '.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(FileWrite)

Container = ['reg_dt']
for minor_number in range(21, 61):
    Container.append(str(minor_number) + '_rssi')
    Container.append(str(minor_number) + '_lc1')
    Container.append(str(minor_number) + '_lc2')
    Container.append(str(minor_number) + '_lc3')
    Container.append(str(minor_number) + '_lc4')
wr.writerow(Container)
Container.clear()

i = 0
while baseTime_2 <= baseTime_2_end:
    baseTime_2 += timedelta(milliseconds=Time_interval)

    #   reg_dt, (minor, rssi, lc1, lc2, lc3, lc4)
    content = [baseTime_2,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
               ]

    SQL_1_WHERE = 'WHERE reg_dt >= \'' + str(baseTime_2 - timedelta(milliseconds=Time_interval)) +\
                  '\' and reg_dt < \'' + str(baseTime_2) + '\''
    BLE_cursor.execute(SQL_1_SELECT + SQL_1_WHERE)
    ble_TEMP = BLE_cursor.fetchall()

    for temp in ble_TEMP:
        content[(temp['minor'] - 21) * 5 + 1] = temp['rssi']

    SQL_2_WHERE = 'WHERE reg_dt >= \'' + str(baseTime_2 - timedelta(milliseconds=Time_interval)) +\
                  '\' and reg_dt < \'' + str(baseTime_2) + '\''
    LC_cursor.execute(SQL_2_SELECT + SQL_2_WHERE)
    lc_TEMP = LC_cursor.fetchall()

    for temp in lc_TEMP:
        content[(temp['minor'] - 21) * 5 + 2] = temp['lc1']
        content[(temp['minor'] - 21) * 5 + 3] = temp['lc2']
        content[(temp['minor'] - 21) * 5 + 4] = temp['lc3']
        content[(temp['minor'] - 21) * 5 + 5] = temp['lc4']

    wr.writerow(content)
    content.clear()
    print("record complete. current iter : " + str(i))
    i += 1


FileWrite.close()
'''
import pymysql
import csv
import datetime
from datetime import timedelta

'''
file_list = ['BLE_record_temp.csv', 'LC_record_temp.csv']

file_write = open("Unify_location.csv", 'w', encoding='utf-8', newline='')
file_writer = csv.writer(file_write)

container = ['reg_dt']
for i in range(21, 61):
    container.append(str(i) + '_lc1')
    container.append(str(i) + '_lc2')
    container.append(str(i) + '_lc3')
    container.append(str(i) + '_lc4')

for i in range(21, 61):
    container.append(str(i) + '_rssi')
file_writer.writerow(container)
container.clear()

file_read = open(file_list[0], 'r', encoding='utf-8')
file_reader = csv.reader(file_read)


for line in file_reader:
    print(line)
'''
baseTime_2 = datetime.datetime(2021, 8, 27, 15, 25, 24, 0)
baseTime_2_end = datetime.datetime(2021, 8, 27, 15, 26, 37, 4)

DB = pymysql.connect(
    user='krri',
    passwd='Mobility408',
    host='192.168.10.193',
    db='smartBlock',
    charset='utf8'
)


LC_cursor = DB.cursor(pymysql.cursors.DictCursor)
SQL_SELECT = 'SELECT reg_dt, minor, lc1, lc2, lc3, lc4 from sb_block_lc '

file_write = open("LC_record_temp_1.csv", 'w', encoding='utf-8', newline='')
wr = csv.writer(file_write)

Container = ['reg_dt']
for minor_number in range(21, 61):
    Container.append(str(minor_number) + '_lc1')
    Container.append(str(minor_number) + '_lc2')
    Container.append(str(minor_number) + '_lc3')
    Container.append(str(minor_number) + '_lc4')
wr.writerow(Container)
Container.clear()

while baseTime_2 < baseTime_2_end:
    print(baseTime_2)
    baseTime_2 += timedelta(milliseconds=200)
    container = [baseTime_2,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                 ]
    SQL_WHERE = 'WHERE reg_dt >= \'' + str(baseTime_2 - timedelta(milliseconds=200)) + \
                  '\' and reg_dt < \'' + str(baseTime_2) + '\''
    LC_cursor.execute(SQL_SELECT + SQL_WHERE)
    lc_TEMP = LC_cursor.fetchall()

    for temp in lc_TEMP:
        container[(temp['minor'] - 21) * 4 + 1] = temp['lc1']
        container[(temp['minor'] - 21) * 4 + 2] = temp['lc2']
        container[(temp['minor'] - 21) * 4 + 3] = temp['lc3']
        container[(temp['minor'] - 21) * 4 + 4] = temp['lc4']

    wr.writerow(container)
    container.clear()

file_write.close()
import csv
import os

path_dir = "C:/Users/lab_408/downloads/pythonProject/데이터 작업"
file_list = os.listdir(path_dir)

for i in file_list:
    if i == 'File_readAndWrite.py' or i == 'Get_Average.py':
        continue

    print(i[:21])
    fread = open(i, 'r', encoding='utf-8')
    rdr = csv.reader(fread)

    fwrite = open(i[:21] + '_.csv', 'w', encoding='utf-8', newline='')
    wr = csv.writer(fwrite)

    for line in rdr:
        if line[3] == 'Rssi':
            wr.writerow(line)
            continue
        if int(line[2]) > 60:
            if line[2] == "61":
                line[2] = "49"
            elif line[2] == "62":
                line[2] = "50"
            elif line[2] == "63":
                line[2] = "51"
            elif line[2] == "64":
                line[2] = "52"

        wr.writerow(line)

    fread.close()
    fwrite.close()



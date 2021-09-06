import threading
import paho.mqtt.client as mqtt
from socket import *
import datetime
import csv


#   MQTT Client define

#   subscribe topic from smart block
subscribe = [
    'pubSBK006', 'pubSBK007', 'pubSBK008', 'pubSBK009', 'pubSBK010',
    'pubSBK011', 'pubSBK012', 'pubSBK013', 'pubSBK014', 'pubSBK015',
]

#   publish topic to smart block
publish = [
    'subSB006', 'subSB007', 'subSB008', 'subSB009', 'subSB010',
    'subSB011', 'subSB012', 'subSB013', 'subSB014', 'subSB015',
]

received = [0,
            #   LC (21-1 ~ 60-4)
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            #   RSSI (21 ~ 60)
            21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def MQTT_msg_parse(com, board, block1, block2, block3, block4):
    result = []
    # result.append(com)
    # result.append(board)
    for i in [block1, block2, block3, block4]:
        result.append(int(i[43:45]))
        result.append([int(i[16:19]), int(i[19:22]), int(i[22:25]), int(i[25:28])])
        received[(int(i[43:45])-21)*4 + 1] = int(i[16:19])
        received[(int(i[43:45])-21)*4 + 2] = int(i[19:22])
        received[(int(i[43:45])-21)*4 + 3] = int(i[22:25])
        received[(int(i[43:45])-21)*4 + 4] = int(i[25:28])

        # result.append(i[16:28])
    return result


def BLE_msg_parse(recvData):
    for i in range(161, 201):
        received[i] = 0

    idx = 0
    while idx + 7 <= len(recvData):
        back = idx
        while recvData[back] != ':':
            back += 1
        minor = int(recvData[idx:back])
        idx = back+1
        back = idx
        while recvData[back] != ',':
            back += 1
        rssi = int(recvData[idx:back])
        idx = back + 2
        received[minor + 140] = rssi * -1

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected OK")
    else:
        print("Connection error : ", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))


def on_publish(client, userdata, mid):
    print(mid)


def on_subscribe(client, userdata, mid, granted_qos):
    print("subscribed : " + str(mid) + ' ' + str(granted_qos))


def on_message(client, userdata, msg):
    MSG = msg.payload.decode('utf-8')
    MQTT_msg_parse(MSG[10:14], MSG[26:30], MSG[43:89], MSG[93:139], MSG[143:189], MSG[193:239])


class MQTT_reader(threading.Thread):
    client = mqtt.Client()

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        self.client.on_disconnect = on_disconnect
        self.client.on_publish = on_publish
        self.client.on_subscribe = on_subscribe
        self.client.on_message = on_message
        print("MQTT subscriber is ready")

    def run(self):
        self.client.connect('192.168.10.193', 1883)
        for s in subscribe:
            self.client.subscribe(s, 1)

        self.client.loop_forever()


mqttThread = MQTT_reader('mqtt')
mqttThread.start()


#   Socket server define
host = "192.168.10.100"
port = 3010

file_write = open("signal_record.csv", 'w', encoding='utf-8', newline='')
wr = csv.writer(file_write)

Container = ['reg_dt']
for minor_number in range(21, 61):
    Container.append(str(minor_number) + '_lc1')
    Container.append(str(minor_number) + '_lc2')
    Container.append(str(minor_number) + '_lc3')
    Container.append(str(minor_number) + '_lc4')

for minor_number in range(21, 61):
    Container.append(str(minor_number) + '_ble')

wr.writerow(Container)
Container.clear()



class BLE_reader(threading.Thread):
    serverSocket = ''
    connectionSocket = ''
    address = ''

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind((host, port))
        self.serverSocket.listen(1)
        print("Waiting for client")
        self.connectionSocket, self.address = self.serverSocket.accept()

    def run(self):
        while True:
            data = self.connectionSocket.recv(65535)
            # recvData = json.loads(data.decode())
            if len(data) < 1:
                break

            received[0] = datetime.datetime.now()
            BLE_msg_parse(data.decode())
            wr.writerow(received)
            print(received)

        file_write.close()
        self.serverSocket.close()


bleThread = BLE_reader('ble')
bleThread.run()

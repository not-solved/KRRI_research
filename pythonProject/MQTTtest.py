import paho.mqtt.client as mqtt


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
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def MQTT_msg_parse(com, board, block1, block2, block3, block4):
    result = []
    # result.append(com)
    # result.append(board)
    for i in [block1, block2, block3, block4]:
        result.append(int(i[43:45]))
        result.append([int(i[16:19]), int(i[19:22]), int(i[22:25]), int(i[25:28])])
        received[(int(i[43:45])-21)*5 + 1] = int(i[43:45])
        received[(int(i[43:45])-21)*5 + 2] = int(i[16:19])
        received[(int(i[43:45])-21)*5 + 3] = int(i[19:22])
        received[(int(i[43:45])-21)*5 + 4] = int(i[22:25])
        received[(int(i[43:45])-21)*5 + 5] = int(i[25:28])

        # result.append(i[16:28])
    return result


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
    # print(MQTT_msg_parse(MSG[10:14], MSG[26:30], MSG[43:89], MSG[93:139], MSG[143:189], MSG[193:239]))
    # print(received)


client = mqtt.Client()

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_message = on_message

client.connect('192.168.10.193', 1883)

for s in subscribe:
    client.subscribe(s, 1)

# client.loop_forever()

#   Socket server define
from socket import *
import json

host = "192.168.10.100"
port = 3010

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((host, port))
serverSocket.listen(1)

print("Waiting for client")
connectionSocket, addr = serverSocket.accept()
while True :
    data = connectionSocket.recv(65535)
    if data[0] == 172:
        continue
    # recvData = json.loads(data.decode())
    print("Received Data : ", data.decode())


serverSocket.close()

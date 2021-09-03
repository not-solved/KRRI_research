from socket import *

OPEN = bytes([0x02, 0x00, 0x2c, 0xff, 0x01, 0x00, 0x00, 0xD0, 0x03])
CLOSE = bytes([0x02, 0x00, 0x5e, 0xff, 0x01, 0x00, 0x00, 0xD2, 0x03])
HB = bytes([0x02, 0x00, 0x56, 0xff, 0x01, 0x02, 0x00, 0x1f, 0x96, 0x21, 0x03])

ALERT = bytes([0x02, 0x00, 0x18, 0xff, 0x01, 0x02, 0x00, 0x00, 0x00, 0xE6, 0x03])
ALERT_close = bytes([0x02, 0x00, 0x18, 0xff, 0x01, 0x02, 0x00, 0x01, 0x00, 0xE7, 0x03])
FIRE_ALERT = bytes([0x02, 0x00, 0x18, 0xff, 0x01, 0x02, 0x00, 0x00, 0x00, 0xE7, 0x03])
FIRE_ALERT_close = bytes([0x02, 0x00, 0x18, 0xff, 0x01, 0x02, 0x00, 0x01, 0x00, 0xE6, 0x03])

LOCK = bytes([0x02, 0x00, 0x2F, 0xFF, 0x01, 0x01, 0x00, 0x00, 0xD2, 0x03])
UNLOCK = bytes([0x02, 0x00, 0x2F, 0xFF, 0x01, 0x01, 0x00, 0x01, 0xD3, 0x03])

OPEN_NORMALLY = bytes([0x02, 0x00, 0x2D, 0xFF, 0x01, 0x00, 0x00, 0xD1, 0x03])


serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("192.168.10.100", 8001))
serverSocket.listen(0)
print("Waiting for client")

connectionSocket, addr = serverSocket.accept()
print("Address : " , addr)

while True :
    data = connectionSocket.recv(1024)

    # if_main
    if len(data) > 0 :
        listData = list(map(hex, data))
        print("data length : ", len(data))
        print("Received Data : ", listData)

        if listData[2] == "0x56":
            print("HeartBeat")
            connectionSocket.send(OPEN)
        elif listData[2] == "0x2E":
            print("Door Close")
            connectionSocket.send(HB)
        elif listData[2] == "0x2C":
            print("Door Open")
            connectionSocket.send(HB)

    # end if_main

serverSocket.close()
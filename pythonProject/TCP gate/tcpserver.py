from socket import *

host = "127.0.0.1"
port = 12345

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((host, port))
serverSocket.listen(1)

print("Waiting for client")
while True :
    connectionSocket, addr = serverSocket.accept()
    data = connectionSocket.recv(65535)
    listData = list(map(hex, data))
    print("Received Data : ", data)
    connectionSocket.send("I am a server".encode())

serverSocket.close()


'''
from socket import *

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("192.168.10.100", 8001))
serverSocket.listen(0)
print("Waiting for client")

connectionSocket, addr = serverSocket.accept()
print("Address : " , addr)

while True :
    data = connectionSocket.recv(1024)
    if len(data) > 0 :
        listData = list(map(hex, data))
        print("data length : ", len(data))
        print("Received Data : ", listData)
        connectionSocket.send(bytes([0x02, 0x00, 0x56, 0xff, 0x01, 0x02, 0x00, 0x1f, 0x96, 0x21, 0x03]))

serverSocket.close()

'''
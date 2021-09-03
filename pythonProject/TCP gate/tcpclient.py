from socket import *

ip = "127.0.0.1"
port = 12345

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((ip, port))
print("Connection established")

clientSocket.send(bytes([0x02, 0x00, 0x2e, 0xff, 0x01, 0x00, 0x00, 0xd2, 0x03]))
data = clientSocket.recv(1024)
print("Received data : ", data.decode("utf-8"))


clientSocket.send(bytes([0x02, 0x00, 0x2c, 0xff, 0x01, 0x00, 0x00, 0xD0, 0x03]))
data = clientSocket.recv(1024)
print("Received data : ", data.decode("utf-8"))


clientSocket.close()

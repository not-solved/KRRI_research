from threading import Thread
from socket import *
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import binascii

OPEN_OUT = bytes([0x02, 0x00, 0x2c, 0xff, 0x01, 0x00, 0x00, 0xd0, 0x03])
OPEN_IN = bytes([0x02, 0x00, 0x2c, 0xff, 0x02, 0x00, 0x00, 0xD3, 0x03])
HB = bytes([0x02, 0x00, 0x56, 0xff, 0x01, 0x02, 0x00, 0x1f, 0x96, 0x21, 0x03])

# 태그 시 열리도록 등록한 카드 S/N
CardList = ["bd3b71", "7d6974", ]

class ServerSocket(QObject):

    update_signal = pyqtSignal(tuple, bool)
    recv_signal = pyqtSignal(str)
    send_signal = pyqtSignal(str)
    hbSend_signal = pyqtSignal(str)
    hbRecv_signal = pyqtSignal(str)
    card_signal = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.bListen = False
        self.clients = []
        self.ip = []
        self.threads = []

        # self.update_signal.connect(self.parent.updateClient)
        self.recv_signal.connect(self.parent.updateRMsg)
        self.send_signal.connect(self.parent.updateSMsg)
        self.hbSend_signal.connect(self.parent.updateHBsend)
        self.hbRecv_signal.connect(self.parent.updateHBrecv)
        self.card_signal.connect(self.parent.updateCardMsg)

    def __del__(self):
        self.stop()

    def start(self, ip, port):
        self.server = socket(AF_INET, SOCK_STREAM)
        try :
            self.server.bind((ip, port))
        except Exception as e :
            print("Server socket binding failed")
            return False
        else:
            self.bListen = True
            self.t = Thread(target=self.listen, args=(self.server,))
            self.t.start()
            print("Server listening...")
        return True

    def stop(self):
        self.bListen = False
        if hasattr(self, 'server'):
            self.server.close()
            print("Server shutdown")

    def listen(self, server):
        while self.bListen:
            server.listen(5)
            try:
                client, addr = server.accept()
            except Exception as e:
                print('Accept() Error : ', e)
                break
            else:
                self.clients.append(client)
                self.ip.append(addr)
                self.update_signal.emit(addr, True)
                t = Thread(target=self.receive, args=(addr, client))
                self.threads.append(t)
                t.start()

        self.removeAllClients()
        self.server.close()

    def receive(self, addr, client):
        while True:
            try:
                data = client.recv(1024)
            except Exception as e:
                print('Data receive error : ', e)
                break
            else:
                if data:
                    listData = list(map(hex, data))
                    received = binascii.hexlify(data).decode()
                    print("Received : ", received)
                    if listData[2] == "0x56":
                        self.parent.updateHBrecv(received)
                        client.send(HB)
                        self.parent.updateHBsend(binascii.hexlify(HB).decode())
                    elif listData[2] == "0x53":
                        self.parent.updateCardMsg("Card Data Receive : 0x" + received)
                        if self.check_in_list(received) == "Out":
                            client.send(OPEN_OUT)
                        elif self.check_in_list(received) == "In":
                            client.send(OPEN_IN)
                    else :
                        self.parent.updateRMsg("Success\t(0x" +  received + ")")

        self.removeClient(addr, client)

    def send(self, msg):
        try:
            for c in self.clients:
                c.send(msg)
        except Exception as e:
            print("Send message error : ", e)

    def removeClient(self, addr, client):
        idx = -1
        for k, v in enumerate(self.clients) :
            if v == client:
                idx = k
                break
        client.close()
        self.ip.remove(addr)
        self.clients.remove(client)

        del(self.threads[idx])
        self.update_signal.emit(addr, False)
        self.resourceInfo()

    def removeAllClients(self):
        for c in self.clients:
            c.close()
        for addr in self.ip:
            self.update_signal.emit(addr, False)
        self.ip.clear()
        self.clients.clear()
        self.threads.clear()

    def check_in_list(self, result):
        ID = result[92:98]
        direction = result[47:48]
        print(ID)
        for c in CardList:
            if ID == c:
                if direction == "1":
                    return "Out"
                elif direction == "0":
                    return "In"
        return False

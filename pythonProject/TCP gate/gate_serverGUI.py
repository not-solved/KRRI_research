from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import socket
import sys
import gate_server
import Commands
import binascii

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
port = 8001


class CWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.s = gate_server.ServerSocket(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Gate Control Server')

        # 서버 설정 부분
        ipbox = QHBoxLayout()

        gb = QGroupBox('서버 설정')
        ipbox.addWidget(gb)

        ####################################################################################
        # 서버 IP, PORT 할당 및 가동버튼
        box = QHBoxLayout()

        label = QLabel('Server IP')
        self.ip = QLineEdit(socket.gethostbyname(socket.gethostname()))
        box.addWidget(label)
        box.addWidget(self.ip)
        label = QLabel('Server Port')
        self.port = QLineEdit(str(port))
        box.addWidget(label)
        box.addWidget(self.port)
        self.btn = QPushButton('서버 실행')
        self.btn.setCheckable(True)
        self.btn.toggled.connect(self.toggleButton)
        box.addWidget(self.btn)

        gb.setLayout(box)
        ####################################################################################

        # 클라이언트와 상호작용 하는 부분
        infobox = QHBoxLayout()

        # 메시지 출력 부분
        gb = QGroupBox('메시지')
        infobox.addWidget(gb)

        messageBox = QVBoxLayout()

        box = QHBoxLayout()

        smallbox = QVBoxLayout()
        label = QLabel('보낸 메시지')
        smallbox.addWidget(label)
        self.Smsg = QListWidget()
        smallbox.addWidget(self.Smsg)
        box.addLayout(smallbox)

        smallbox = QVBoxLayout()
        label = QLabel('받은 메시지')
        smallbox.addWidget(label)
        self.Rmsg = QListWidget()
        smallbox.addWidget(self.Rmsg)
        box.addLayout(smallbox)

        messageBox.addLayout(box)

        box = QHBoxLayout()

        smallbox = QVBoxLayout()
        label = QLabel('보낸 HeartBeat 메시지')
        smallbox.addWidget(label)
        self.HBsend = QListWidget()
        smallbox.addWidget(self.HBsend)
        box.addLayout(smallbox)

        smallbox = QVBoxLayout()
        label = QLabel('받은 HeartBeat 메시지')
        smallbox.addWidget(label)
        self.HBrecv = QListWidget()
        smallbox.addWidget(self.HBrecv)
        box.addLayout(smallbox)

        messageBox.addLayout(box)

        cardbox = QVBoxLayout()
        label = QLabel('수신된 카드 정보')
        cardbox.addWidget(label)
        self.cardMsg = QListWidget()
        cardbox.addWidget(self.cardMsg)
        messageBox.addLayout(cardbox)

        gb.setLayout(messageBox)

        ####################################################################################
        gb = QGroupBox('보낼 명령')
        infobox.addWidget(gb)

        box = QVBoxLayout()

        minorBox = QVBoxLayout()
        self.openbtn = QPushButton('OPEN')
        self.openbtn.clicked.connect(self.sendOPENcom)
        self.openbtn.setFixedSize(150, 20)
        minorBox.addWidget(self.openbtn)
        self.openbtn = QPushButton('OPEN normally')
        self.openbtn.clicked.connect(self.sendOPEN_Normally)
        self.openbtn.setFixedSize(150, 20)
        minorBox.addWidget(self.openbtn)
        self.closebtn = QPushButton('CLOSE')
        self.closebtn.clicked.connect(self.sendCLOSEcom)
        self.closebtn.setFixedSize(150, 20)
        minorBox.addWidget(self.closebtn)
        box.addLayout(minorBox)

        minorBox = QVBoxLayout()

        moreMinorBox = QHBoxLayout()
        self.lockInside = QPushButton('LOCK\ninside')
        self.lockInside.clicked.connect(self.sendLockInside)
        self.lockInside.setFixedSize(70, 40)
        moreMinorBox.addWidget(self.lockInside)
        self.unlockInside = QPushButton('UNLOCK\ninside')
        self.unlockInside.clicked.connect(self.sendUnlockInside)
        self.unlockInside.setFixedSize(70, 40)
        moreMinorBox.addWidget(self.unlockInside)
        minorBox.addLayout(moreMinorBox)

        moreMinorBox = QHBoxLayout()
        self.lockOutside = QPushButton('LOCK\noutside')
        self.lockOutside.clicked.connect(self.sendLockOutside)
        self.lockOutside.setFixedSize(70, 40)
        moreMinorBox.addWidget(self.lockOutside)
        self.unlockOutside = QPushButton('UNLOCK\noutside')
        self.unlockOutside.clicked.connect(self.sendUnlockOutside)
        self.unlockOutside.setFixedSize(70, 40)
        moreMinorBox.addWidget(self.unlockOutside)
        minorBox.addLayout(moreMinorBox)

        box.addLayout(minorBox)


        minorBox = QVBoxLayout()
        self.speekbtn = QPushButton('Voice Broadcast')
        self.speekbtn.clicked.connect(self.sendBROADCASTcom)
        self.speekbtn.setFixedSize(150, 20)
        minorBox.addWidget(self.speekbtn)
        self.parambtn = QPushButton('Set Parameter')
        self.parambtn.clicked.connect(self.sendPARAMETERcom)
        self.parambtn.setFixedSize(150, 20)
        minorBox.addWidget(self.parambtn)
        box.addLayout(minorBox)

        gb.setLayout(box)

        minorBox = QVBoxLayout()

        moreMinorBox = QHBoxLayout()
        self.alertbtn = QPushButton('ALERT')
        self.alertbtn.clicked.connect(self.sendALERTcom)
        self.alertbtn.setFixedSize(70, 40)
        moreMinorBox.addWidget(self.alertbtn)
        self.falertbtn = QPushButton('Fire ALERT')
        self.falertbtn.clicked.connect(self.sendFIREALERTcom)
        self.falertbtn.setFixedSize(70, 40)
        moreMinorBox.addWidget(self.falertbtn)
        minorBox.addLayout(moreMinorBox)

        moreMinorBox = QHBoxLayout()
        self.alertoffbtn = QPushButton('ALERT\nOFF')
        self.alertoffbtn.clicked.connect(self.sendALERTOFFcom)
        self.alertoffbtn.setFixedSize(70, 40)
        moreMinorBox.addWidget(self.alertoffbtn)
        self.falertoffbtn = QPushButton('Fire ALERT\nOFF')
        self.falertoffbtn.clicked.connect(self.sendFIREALERTOFFcom)
        self.falertoffbtn.setFixedSize(70, 40)
        moreMinorBox.addWidget(self.falertoffbtn)
        minorBox.addLayout(moreMinorBox)

        box.addLayout(minorBox)

        ####################################################################################
        # 전체 배치
        vbox = QVBoxLayout()
        vbox.addLayout(ipbox)
        vbox.addLayout(infobox)
        self.setLayout(vbox)

        self.resize(1000, 600)
        self.show()

    def toggleButton(self, state):
        if state:
            ip = self.ip.text()
            port = self.port.text()
            if self.s.start(ip, int(port)):
                self.clearMsg()
                self.btn.setText('서버 종료')
        else:
            self.s.stop()
            self.btn.setText('서버 실행')


    # 데이터 수신 시 어플리케이션 각 구역에 출력 처리
    def updateSMsg(self, msg):
        self.Smsg.addItem(QListWidgetItem(msg))
        self.Smsg.setCurrentRow(self.Smsg.count() - 1)

    def updateRMsg(self, msg):
        self.Rmsg.addItem(QListWidgetItem(msg))
        self.Rmsg.setCurrentRow(self.Rmsg.count() - 1)

    def updateHBsend(self, msg):
        self.HBsend.addItem(QListWidgetItem(msg))
        self.HBsend.setCurrentRow(self.HBsend.count() - 1)

    def updateHBrecv(self, msg):
        self.HBrecv.addItem(QListWidgetItem(msg))
        self.HBrecv.setCurrentRow(self.HBrecv.count() - 1)

    def updateCardMsg(self, msg):
        self.cardMsg.addItem(QListWidgetItem(msg))
        self.cardMsg.setCurrentRow(self.cardMsg.count() - 1)

    
    # 메시지 초기화
    def clearMsg(self):
        self.Smsg.clear()
        self.Rmsg.clear()
        self.HBrecv.clear()
        self.HBsend.clear()
        self.cardMsg.clear()

    # 연결 종료 이벤트
    def closeEvent(self, e):
        self.s.stop()


    # 버튼 클릭 명령
    def sendOPENcom(self):
        self.updateSMsg("OPEN\t(0x" + binascii.hexlify(Commands.OPEN).decode() + ")")
        print("Send : ", binascii.hexlify(Commands.OPEN).decode())
        self.s.send(Commands.OPEN)

    def sendOPEN_Normally(self):
        self.updateSMsg("OPEN normally\t(0x" + binascii.hexlify(Commands.OPEN_NORMALLY).decode() + ")")
        print("Send : ", binascii.hexlify(Commands.OPEN_NORMALLY).decode())
        self.s.send(Commands.OPEN_NORMALLY)

    def sendCLOSEcom(self):
        self.updateSMsg("Close\t(0x" + binascii.hexlify(Commands.CLOSE).decode() + ")")
        print("Send : ", binascii.hexlify(Commands.CLOSE).decode())
        self.s.send(Commands.CLOSE)


    def sendHEARTBEATcom(self):
        self.updateHBsend(binascii.hexlify(Commands.HEART_BEAT).decode())
        print("Send : ", binascii.hexlify(Commands.HEART_BEAT).decode())
        self.s.send(Commands.HEART_BEAT)

    def sendPARAMETERcom(self):
        self.updateSMsg("Set Param\t(0x" + binascii.hexlify(Commands.SET_PARAMETER).decode() + ")")
        print("Send : ", binascii.hexlify(Commands.SET_PARAMETER).decode())
        self.s.send(Commands.SET_PARAMETER)

    def sendBROADCASTcom(self):
        self.updateSMsg("Voice Broadcase\t(0x" + binascii.hexlify(Commands.VOICE_BOARD).decode() + ")")
        print("Send : ", binascii.hexlify(Commands.VOICE_BOARD).decode())
        self.s.send(Commands.VOICE_BOARD)


    def sendALERTcom(self):
        self.updateSMsg("Alarm set\t(0x" + binascii.hexlify(Commands.ALERT).decode() + ")")
        print("Send : ", binascii.hexlify(Commands.ALERT).decode())
        self.s.send(Commands.ALERT)

    def sendALERTOFFcom(self):
        self.updateSMsg("Alarm off\t(0x" + binascii.hexlify(Commands.ALERT_close).decode() + ")")
        print("Send : ", binascii.hexlify(Commands.ALERT_close).decode())
        self.s.send(Commands.ALERT_close)

    def sendFIREALERTcom(self):
        self.updateSMsg("Fire Alarm set\t(0x" + binascii.hexlify(Commands.FIRE_ALERT).decode() + ")")
        print("Send : ", binascii.hexlify(Commands.FIRE_ALERT).decode())
        self.s.send(Commands.FIRE_ALERT)

    def sendFIREALERTOFFcom(self):
        self.updateSMsg("Fire Alarm off\t(0x" + binascii.hexlify(Commands.FIRE_ALERT_close).decode() + ")")
        print("Send : ", binascii.hexlify(Commands.FIRE_ALERT_close).decode())
        self.s.send(Commands.FIRE_ALERT_close)


    def sendLockInside(self):
        self.updateSMsg("Lock inside\t(0x" + binascii.hexlify(Commands.LOCK_inside).decode() + ")")
        print("Send : ", binascii.hexlify(Commands.LOCK_inside).decode())
        self.s.send(Commands.LOCK_inside)

    def sendUnlockInside(self):
        self.updateSMsg("Unlock inside\t(0x" + binascii.hexlify(Commands.UNLOCK_inside).decode() + ")")
        print("Send : ", binascii.hexlify(Commands.UNLOCK_inside).decode())
        self.s.send(Commands.UNLOCK_inside)

    def sendLockOutside(self):
        self.updateSMsg("Lock oustide\t(0x" + binascii.hexlify(Commands.LOCK_outside).decode() + ")")
        print("Send : ", binascii.hexlify(Commands.LOCK_outside).decode())
        self.s.send(Commands.LOCK_outside)

    def sendUnlockOutside(self):
        self.updateSMsg("Unlock outside\t(0x" + binascii.hexlify(Commands.UNLOCK_outside).decode() + ")")
        print("Send : ", binascii.hexlify(Commands.UNLOCK_outside).decode())
        self.s.send(Commands.UNLOCK_outside)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()
    sys.exit(app.exec_())

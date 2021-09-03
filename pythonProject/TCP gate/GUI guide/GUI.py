import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication


class MyApp(QWidget):

    # 어플리케이션 초기화
    def __init__(self):
        super().__init__()
        self.initUI()

    # 어플리케이션 초기화 초기화
    def initUI(self):
        # 상단에 표기될 이름 지정
        self.setWindowTitle('My First Application')

        # 위치 및 크기 지정
        self.setGeometry(300, 300, 300, 200)
        self.move(300, 300)
        self.resize(800, 500)

        # 버튼 구현
        btn = QPushButton('Quit', self)
        btn.move(50, 50)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(QCoreApplication.instance().quit)  # 클릭 시 기능 구현 : 닫기

        # 어플리케이션 화면에 출력
        self.show()


#   메인 함수
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())





#   툴팁 나타내기
'''
from PyQt.QtWidgets import QToolTip
from PyQt.QtGui import QFont

def initUI(self):
    QToolTip.setFont(QFont('SanSerif', 10))                 #   툴팁 글자 설정 (이후 모든 툴팁에 적용)
    self.setToolTip('This is a <b>QWidget</b> widget')      #   특정 요소들 (어플리케이션, 버튼, 그림 등)에 툴팁 적용
'''

#   상태바 만들기
'''
from PyQt5.QtWidgets import QMainWindow

def initUI(self):
    self.statusBar().showMessage('Ready')
'''

#   메뉴바 만들기
from PyQt5.QtWidgets import QMainWindow, QAction, qApp
from PyQt5.QtGui import QIcon

def initUI(self):
    #   메뉴에서 사용할 종료하기 기능 추가
    exitAction = QAction(QIcon('exit.png'), 'Exit', self)
    exitAction.setShortcut('Ctrl+Q')            #   단축키 지정
    exitAction.setStatusTip('Exit application') #   상태바에 나타날 툴팁 메시지
    exitAction.triggered.connect(qApp.quit)     #   어플리케이션 종료 기능 부여

    self.statusBar()          # 상태바 띄우기

    #   메뉴 바 구축하기'
    menubar = self.menuBar()
    menubar.setNativeMenuBar(false)
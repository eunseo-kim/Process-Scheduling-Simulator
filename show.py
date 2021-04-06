from Main import *

import sys
from PyQt5.QtWidgets import *


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.Proc_List = []
        self.Run_Start = True
        self.initUI()

    def initUI(self):

        self.Alg_Select = QComboBox(self)
        self.Alg_Select.addItem('FCFS')
        self.Alg_Select.addItem('RR')
        self.Alg_Select.addItem('SPN')
        self.Alg_Select.addItem('SRTN')
        self.Alg_Select.addItem('HRRN')
        self.Alg_Select.addItem('YOA')
        self.Alg_Select.activated.connect(self.enableSlot)

        ProName = QLineEdit()
        AT = QSpinBox()
        AT.setRange(0, 65535)
        BT = QSpinBox()
        BT.setRange(0, 65535)

        #Proc_Table은 둘째줄에 사용하지만 addButton에서 사용하기 떄문에 미리 선언
        self.Proc_Table = QTableWidget(self)
        self.Proc_Table.setColumnCount(3)
        self.Proc_Table.setHorizontalHeaderLabels(['Process Name', 'Arrival Time', 'Burst Time'])

        # Proc_List에 프로세스 목록을 추가 / 리셋하는 버튼
        addButton = QPushButton('Add', self)
        addButton.clicked.connect(lambda: self.add(ProName.text(),AT.value(),BT.value()))
        resetButton = QPushButton('Reset', self)
        resetButton.clicked.connect(self.reset)

        self.CPU_Number = QComboBox(self)
        self.CPU_Number.addItem('1')
        self.CPU_Number.addItem('2')
        self.CPU_Number.addItem('4')

        # quantum을 넣는 스핀박스, 초기는 FCFS이기에 비활성화해둠
        self.TQ = QSpinBox()
        self.TQ.setRange(0, 65535)
        self.TQ.setDisabled(True)

        # Run 알고리즘은 크게 실행도중인 경우 / 아닌경우, 아닌경우에서 Alg_Select가 어떤 알고리즘을 골랐느냐에 따라 선정이 달라질거임.
        # Run과 Stop은 최하단에서 선언해서 실행하도록 해야할것..아마?
        Run_Alg = QPushButton('Run', self)
        resetButton.clicked.connect(self.Run_Algorithm)
        Stop_Alg = QPushButton('Stop', self)

        # 첫째줄, 그리드에 프로세스 이름, AT, BT, 추가버튼, 리셋버튼 추가
        grid_Line1 = QGridLayout()
        grid_Line1.addWidget(QLabel('Algorithm'), 0, 0)
        grid_Line1.addWidget(QLabel('Process Name'), 0, 1)
        grid_Line1.addWidget(QLabel('AT'), 0, 2)
        grid_Line1.addWidget(QLabel('BT'), 0, 3)
        grid_Line1.addWidget(self.Alg_Select,1,0)
        grid_Line1.addWidget(ProName, 1, 1)
        grid_Line1.addWidget(AT, 1, 2)
        grid_Line1.addWidget(BT, 1, 3)
        grid_Line1.addWidget(addButton, 1, 4)
        grid_Line1.addWidget(resetButton, 1, 5)

        #두번째 줄 그리드, 모양만 구현하고 실제 실행은 되는거 없음
        grid_Line2 = QGridLayout()
        grid_Line2.addWidget(QLabel('Process Number'),0,0)
        grid_Line2.addWidget(self.CPU_Number, 0, 1)
        grid_Line2.addWidget(QLabel('Time qunaturn'),1,0)
        grid_Line2.addWidget(self.TQ, 1, 1)
        grid_Line2.addWidget(Run_Alg,2,0)
        grid_Line2.addWidget(Stop_Alg,2,1)

        hbox_Line2 = QHBoxLayout()
        hbox_Line2.addWidget(self.Proc_Table)
        hbox_Line2.addLayout(grid_Line2)
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)
        vbox_main.addLayout(grid_Line1)
        vbox_main.addLayout(hbox_Line2)
        vbox_main.addStretch(3)

        self.setWindowTitle('Test')
        self.setGeometry(0, 0, 800, 600)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def enableSlot(self):
        if self.Alg_Select.currentText() == 'RR' or self.Alg_Select.currentText() == 'SRTN':
            self.TQ.setEnabled(True)
        else:
            self.TQ.setDisabled(True)
    def add(self, name, at, bt):
        # Proc_List에 프로세스 이름, AT, BT 저장
        self.Proc_List.append((name,at,bt))
        # 이후 Proc_Table에 프로세스를 띄우도록 함, 열크기 = Proc_List 크기
        self.Proc_Table.setRowCount(len(self.Proc_List))
        for i in range(len(self.Proc_List)):
            self.Proc_Table.setItem(i, 0, QTableWidgetItem(self.Proc_List[i][0]))
            self.Proc_Table.setItem(i, 1, QTableWidgetItem(str(self.Proc_List[i][1])))
            self.Proc_Table.setItem(i, 2, QTableWidgetItem(str(self.Proc_List[i][2])))

    def reset(self):
        # Proc_Table의 열을 0으로 만들고 Proc_List를 clear
        self.Proc_Table.setRowCount(0)
        self.Proc_List.clear()
    
    def Run_Algorithm(self):
        pass
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

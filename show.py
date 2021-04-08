from Main import *
import random
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import time

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.Proc_List = []
        self.Run_Start = False
        self.initUI()
        
    def initUI(self):
        # 알고리즘 종류를 선택핧 Alg_Select를 콤보박스로 구현
        # 실행, 혹은 정지 도중에 알고리즘을 바꿨을때 어찌처리할지도 생각해야할듯? Reset 함수 부르면 될거같긴 함, 아니면 실행중엔 Stop을 제외한 버튼들 비활성 걸어놓던가
        self.Alg_Select = QComboBox(self)
        self.Alg_Select.addItem('FCFS')
        self.Alg_Select.addItem('RR')
        self.Alg_Select.addItem('SPN')
        self.Alg_Select.addItem('SRTN')
        self.Alg_Select.addItem('HRRN')
        self.Alg_Select.addItem('YOA')
        self.Alg_Select.activated.connect(self.enableSlot)
        
        # 프로세스 이름을 사용자에게 받을 ProName, AT를 사용자에게 받을 AT, BT를 사용자에게 받을 BT
        # AT와 BT같이 사용자에게 숫자로만 받을거라면 스핀박스로 하는게 더 편하다고 함 
        self.ProName = QLineEdit()
        self.ProName.setMaxLength(10)
        self.AT = QSpinBox()
        self.AT.setRange(0, 65535)
        self.BT = QSpinBox()
        self.BT.setRange(0, 65535)


        #프로세스 목록을 표로 보여줄 Proc_Table선언
        self.Proc_Table = QTableWidget(self)
        self.Proc_Table.setColumnCount(3)
        self.Proc_Table.setHorizontalHeaderLabels(['Process Name', 'Arrival Time', 'Burst Time'])
        self.Proc_Table.verticalHeader().setVisible(False)
        header = self.Proc_Table.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)

        #CPU의 코어 개수 선택에 사용할 CPU_Number를 콤보박스로 선언
        self.CPU_Number = QComboBox(self)
        self.CPU_Number.addItem('1')
        self.CPU_Number.addItem('2')
        self.CPU_Number.addItem('4')
        self.CPU_Number.activated.connect(self.setCPUTable_slot)

        #Ready Queue 보여줄 테이블
        self.Ready_Table = QTableWidget(self)
        self.Ready_Table.setRowCount(1)
        self.Ready_Table.verticalHeader().setVisible(False)
        self.Ready_Table.setMaximumHeight(50)
        self.Ready_Table.verticalHeader().setDefaultSectionSize(40)
        self.Ready_Table.horizontalHeader().setVisible(False)

        # CPU 일 목록
        self.Gantt_Table = QTableWidget(self)
        self.Gantt_Table.setRowCount(1)
        self.Gantt_Table.setVerticalHeaderLabels(['CPU 1'])
        header = self.Gantt_Table.verticalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)

        self.realTimeLabel = QLabel('Real Time = 0 sec')
        # quantum을 넣는 스핀박스, 초기는 FCFS이기에 비활성화해둠
        self.TQ = QSpinBox()
        self.TQ.setRange(1, 65535)
        self.TQ.setDisabled(True)

        #Gantt Chart를 표로 보여줄 Rseult_Table선언
        self.Rseult_Table = QTableWidget(self)
        self.Rseult_Table.setColumnCount(6)
        self.Rseult_Table.setHorizontalHeaderLabels(['Process Name', 'Arrival Time', 'Burst Time', 'Waiting Time', 'Turnaround Time', 'Normalized TT'])
        self.Rseult_Table.verticalHeader().setVisible(False)
        header = self.Rseult_Table.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.Stretch)


        # Proc_List에 프로세스 목록을 추가 및 화면 내용을 리셋하는 버튼 (이때문에 거진 뒤로 가야할듯) 
        addButton = QPushButton('Add', self)
        addButton.clicked.connect(self.add)
        resetButton = QPushButton('Reset', self)
        resetButton.clicked.connect(self.reset)

        # Run 알고리즘은 크게 실행도중인 경우 / 아닌경우, 아닌경우에서 Alg_Select가 어떤 알고리즘을 골랐느냐에 따라 선정이 달라질거임.
        # Run과 Stop은 최하단에서 선언해서 실행하도록 해야할것..아마?
        # 첫실행시에 Stop은 비활성, Run 누르면 활성 이렇게 해야할듯?
        self.Run_Alg = QPushButton('Run', self)
        self.Run_Alg.clicked.connect(self.Run_Algorithm)
        self.Stop_Alg = QPushButton('Stop', self)
        self.Stop_Alg.setDisabled(True)

        # 첫째줄, 그리드에 프로세스 이름, AT, BT, 추가버튼, 리셋버튼 추가
        grid_Line1 = QGridLayout()
        grid_Line1.addWidget(QLabel('Algorithm'), 0, 0)
        grid_Line1.addWidget(QLabel('Process Name'), 0, 1)
        grid_Line1.addWidget(QLabel('AT'), 0, 2)
        grid_Line1.addWidget(QLabel('BT'), 0, 3)
        grid_Line1.addWidget(self.Alg_Select,1,0)
        grid_Line1.addWidget(self.ProName, 1, 1)
        grid_Line1.addWidget(self.AT, 1, 2)
        grid_Line1.addWidget(self.BT, 1, 3)
        grid_Line1.addWidget(addButton, 1, 4)
        grid_Line1.addWidget(resetButton, 1, 5)

        #두번째 줄 오른편의 그리드, CPU_Number, TQ, Run_Alg, Stop_Alg을 그리드 레이아웃에 추가
        grid_Line2 = QGridLayout()
        grid_Line2.addWidget(QLabel('Process Number'),0,0)
        grid_Line2.addWidget(self.CPU_Number, 0, 1)
        grid_Line2.addWidget(QLabel('RR Time Qunaturn'),1,0)
        grid_Line2.addWidget(self.TQ, 1, 1)
        grid_Line2.addWidget(self.Run_Alg,2,0)
        grid_Line2.addWidget(self.Stop_Alg,2,1)

        #두번째 줄을 통합해줄 hbox_Line2, Proc_Table과 grid_Line2를 레이아웃에 추가함.
        hbox_Line2 = QHBoxLayout()
        hbox_Line2.addWidget(self.Proc_Table)
        hbox_Line2.addLayout(grid_Line2)

        # 그냥 이름용 
        vbox_Line3 = QVBoxLayout()
        Ready_Name = QLabel('Ready Queue')
        Ready_Name.setMaximumHeight(13)
        vbox_Line3.addWidget(Ready_Name)
        vbox_Line3.addWidget(self.Ready_Table)

        hbox_Line4 = QHBoxLayout()
        hbox_Line4.addWidget(QLabel('Gantt Chart'))
        hbox_Line4.addWidget(self.realTimeLabel)

        #레이아웃 및 위젯을 통합할 vbox_main을 선언, 메인 레이아웃 지정 후 레이아웃 및 위젯 통합
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)
        vbox_main.addLayout(grid_Line1)
        vbox_main.addLayout(hbox_Line2)
        vbox_main.addLayout(vbox_Line3)
        vbox_main.addLayout(hbox_Line4)
        vbox_main.addWidget(self.Gantt_Table)
        vbox_main.addWidget(self.Rseult_Table)
        #vbox_main.addStretch(3)
        self.setWindowTitle('Test')
        #setGeometry가 크기랑 위치 지정하는건데 잘몰르겟음 필요한가, 센터로 화면 가운데 위치지정중임
        #self.setGeometry(0, 0, 800, 600)
        self.center()
        self.show()

    def center(self):
        # 프로그램이 화면 중앙을 알아서 찾아가는 함수
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def enableSlot(self):
        if self.Alg_Select.currentText() == 'RR':
            self.TQ.setEnabled(True)
        else:
            self.TQ.setDisabled(True)

    def setCPUTable_slot(self):
        NameHeader = []
        CPU_Select = int(self.CPU_Number.currentText())
        self.Gantt_Table.setRowCount(CPU_Select)

        for i in range(1,CPU_Select+1):
            NameHeader.append('CPU '+str(i))

        self.Gantt_Table.setVerticalHeaderLabels(NameHeader)
        header = self.Gantt_Table.verticalHeader() 
        for i in range(len(NameHeader)):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

    def add(self):
        # Proc_List에 프로세스 이름, AT, BT 저장, 색상은 랜덤지정
        self.Proc_List.append([self.ProName.text(),self.AT.value(),self.BT.value(),None,None,None,random.randint(0,255),random.randint(0,255),random.randint(0,255)])
        # 이후 Proc_Table에 프로세스를 띄우도록 함, 열크기 = Proc_List 크기
        self.Proc_Table.setRowCount(len(self.Proc_List))
        for i in range(len(self.Proc_List)):
            self.Proc_Table.setItem(i, 0, QTableWidgetItem(self.Proc_List[i][0]))
            self.Proc_Table.item(i,0).setBackground(QtGui.QColor(self.Proc_List[i][6], self.Proc_List[i][7], self.Proc_List[i][8]))
            if self.Proc_List[i][6] + self.Proc_List[i][7] +  self.Proc_List[i][8] < 350:
                self.Proc_Table.item(i,0).setForeground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
            self.Proc_Table.setItem(i, 1, QTableWidgetItem(str(self.Proc_List[i][1])))
            self.Proc_Table.setItem(i, 2, QTableWidgetItem(str(self.Proc_List[i][2])))
        self.ProName.clear()
        self.AT.setValue(0)
        self.BT.setValue(0)

    def reset(self):
        # Proc_Table과 Rseult_Table 열을 0으로 만들고 Proc_List를 clear
        self.Proc_Table.setRowCount(0)
        self.Ready_Table.reset()
        self.Gantt_Table.reset()
        self.Rseult_Table.setRowCount(0)
        self.Stop_Alg.setDisabled(True)
        self.Proc_List.clear()
        
    # 캡쳐하려고하면 대충 막 5초뒤에 뻗던데 왜그런진 모르겠음..
    def Run_Algorithm(self):
        self.Stop_Alg.setEnabled(True)
        schedule = Scheduler(self.Proc_List[0:3], int(self.CPU_Number.currentText()))
        cur_time = 0
        finish_processes_count = 0
        AT_idx = 0
        sorted_processes = sorted(schedule.processes, key= lambda x : x.AT)
        # 끝난 프로세스가 총 프로세스의 수와 같아질때까지 작동
        while(finish_processes_count < schedule.process_count):
            # 현재 시간갱신하는 알고리즘
            fortext = 'Real Time = '+str(cur_time)+' sec'
            self.realTimeLabel.setText(fortext)
            self.realTimeLabel.repaint()

            # 현재 시간에 도착할 프로세스 대기열 큐에 넣어주기
            for process_idx in range(AT_idx, schedule.process_count):
                process = sorted_processes[process_idx]
                if process.AT == cur_time:
                    print("processe arrived - cur_time:", cur_time, " p_id :", process.process_id)
                    schedule.ready_queue.append(process)
                elif process.AT > cur_time:
                    AT_idx = process_idx
                    break

            # cpu들을 돌면서
            for cpu in schedule.cpus:
                # cpu의 일이 끝났으면
                if cpu.is_finished(cur_time):
                    print("processe finished - cur_time:", cur_time, " p_id :", cpu.process.process_id)
                    cpu.process.calculate_finished_process(cur_time)
                    finish_processes_count += 1
                    # 일이 끝난 CPU는 쉬게 해준다.
                    cpu.set_idle()
                # cpu가 쉬고 있고
                if cpu.is_idle():
                    # 대기열에 프로세스가 하나 이상 존재한다면
                    if len(schedule.ready_queue) >= 1 :
                        # 대기열 내의 프로세스 중 BT가 가장 작은 프로세스를 선별하여 cpu에 set
                        process_num = 0
                        for i in range(1,len(schedule.ready_queue)):
                            if schedule.ready_queue[i].BT < schedule.ready_queue[process_num].BT:
                                process_num = i
                        input_process = schedule.ready_queue.pop(process_num)
                        cpu.set_process(input_process, cur_time, cur_time + input_process.BT)
            # Ready_Table 갱신하는 알고리즘
            # 테이블을 clear하고 새로 채우는 방식임
            # ready_queue에서 빠지면 Ready_Table에서도 빠지게 그런거 가능하면 그게 더 효율적이긴 할것임..
            self.Ready_Table.clear()
            self.Ready_Table.setColumnCount(len(schedule.ready_queue))
            if len(schedule.ready_queue) == 0:
                self.Ready_Table.repaint()
            else:
                for Queue_Num in range(len(schedule.ready_queue)):
                    self.Ready_Table.setItem(0, Queue_Num, QTableWidgetItem(schedule.ready_queue[Queue_Num].process_id))
                    for Set_Num in range(len(self.Proc_List)):
                        if self.Proc_List[Set_Num][0] == schedule.ready_queue[Queue_Num].process_id:
                            self.Ready_Table.item(0, Queue_Num).setBackground(QtGui.QColor(self.Proc_List[Set_Num][6], self.Proc_List[Set_Num][7], self.Proc_List[Set_Num][8]))
                            if self.Proc_List[Set_Num][6] + self.Proc_List[Set_Num][7] +  self.Proc_List[Set_Num][8] < 350:
                                self.Ready_Table.item(0, Queue_Num).setForeground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
                self.Ready_Table.repaint()
            # 현재시간 증가
            cur_time += 1
            time.sleep(1)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
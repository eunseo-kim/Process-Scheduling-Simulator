from Main import *
import random
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import time
from PyQt5.QtCore import Qt
import copy


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.change_font()
        self.Proc_List = []
        self.history = []
        self.Run_Start = False
        self.algo_list = ["FCFS", "RR", "SPN", "SRTN", "HRRN", "YOSA"]
        self.column_count = 3
        self.cur_algo = "FCFS"
        self.proc_Count = [0] * 4
        self.initUI()

    # 수정 : font
    def change_font(self):
        font = QtGui.QFont()
        # 폰트 없으시면 주석 처리하세요!
        # font.setFamily("카카오 Regular")
        font.setFamily("Consolas")
        font.setPointSize(10)
        # font.setBold(True)
        self.setFont(font)

    def initUI(self):
        self.resize(1400, 900)
        self.center()

        # 알고리즘 종류를 선택핧 Alg_Select를 콤보박스로 구현
        # 실행, 혹은 정지 도중에 알고리즘을 바꿨을때 어찌처리할지도 생각해야할듯? Reset 함수 부르면 될거같긴 함, 아니면 실행중엔 Stop을 제외한 버튼들 비활성 걸어놓던가
        self.Alg_Select = QComboBox(self)
        for algo in self.algo_list:
            self.Alg_Select.addItem(algo)
        self.Alg_Select.activated.connect(self.enableSlot)

        # 프로세스 이름을 사용자에게 받을 ProName, AT를 사용자에게 받을 AT, BT를 사용자에게 받을 BT
        # AT와 BT같이 사용자에게 숫자로만 받을거라면 스핀박스로 하는게 더 편하다고 함
        self.ProName = QLineEdit()
        self.ProName.setMaxLength(10)
        self.ATLabel = QLabel("AT")
        self.AT = QSpinBox()
        self.AT.setRange(0, 65535)
        self.BT = QSpinBox()
        self.BT.setRange(1, 65535)
        self.StudentList = QComboBox(self)
        self.StudentList.addItem("학생 1")
        self.StudentList.setDisabled(True)
        # 프로세스 목록을 표로 보여줄 Proc_Table선언
        self.Proc_Table = QTableWidget(self)
        self.Proc_Table.setColumnCount(3)
        self.Proc_Table.setHorizontalHeaderLabels(["Process Name", "Arrival Time", "Burst Time"])

        self.Proc_Table.verticalHeader().setVisible(False)
        header = self.Proc_Table.horizontalHeader()
        for column_idx in range(self.column_count):
            header.setSectionResizeMode(column_idx, QHeaderView.Stretch)

        # CPU의 코어 개수 선택에 사용할 cpu_count를 콤보박스로 선언
        self.cpu_count = QComboBox(self)
        for cpu_idx in range(1, 5):
            self.cpu_count.addItem(str(cpu_idx))
        self.cpu_count.activated.connect(self.setCPUTable_slot)
        self.CPULabel = QLabel("CPU")

        # Ready Queue 보여줄 테이블
        self.Ready_Table = QTableWidget(self)
        self.Ready_Table.setRowCount(1)
        self.Ready_Table.verticalHeader().setVisible(False)
        self.Ready_Table.setMaximumHeight(50)
        self.Ready_Table.verticalHeader().setDefaultSectionSize(40)
        self.Ready_Table.horizontalHeader().setVisible(False)

        # CPU 일 목록
        self.Gantt_Table = QTableWidget(self)
        self.Gantt_Table.setRowCount(1)
        self.Gantt_Table.setVerticalHeaderLabels(["CPU 1"])
        header = self.Gantt_Table.verticalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)

        self.realTimeLabel = QLabel("Real Time = 0 sec")
        # quantum을 넣는 스핀박스, 초기는 FCFS이기에 비활성화해둠
        self.TQ = QSpinBox()
        self.TQ.setRange(1, 65535)
        self.TQ.setDisabled(True)
        self.TQLabel = QLabel("Quantum")

        self.TP_Time = QSpinBox()
        self.TP_Time.setRange(1,24)
        self.TP_Time.setDisabled(True)

        # Gantt Chart를 표로 보여줄 Result_Table선언
        self.Result_Table = QTableWidget(self)
        self.Result_Table.setColumnCount(6)
        self.Result_Table.setHorizontalHeaderLabels(
            ["Process Name", "Arrival Time", "Burst Time", "Waiting Time", "Turnaround Time", "Normalized TT"]
        )
        self.Result_Table.verticalHeader().setVisible(False)
        header = self.Result_Table.horizontalHeader()
        for time_table_col in range(6):
            header.setSectionResizeMode(time_table_col, QHeaderView.Stretch)

        # Proc_List에 프로세스 목록을 추가 및 화면 내용을 리셋하는 버튼 (이때문에 거진 뒤로 가야할듯)
        self.addButton = QPushButton("Add", self)
        # addButton.clicked.connect(self.add)
        # 수정 : 디버깅용 test를 add 버튼에 일시적으로 연결 (test 누르면 자동으로 값 입력됨)
        self.addButton.clicked.connect(self.add)

        resetButton = QPushButton("Reset", self)
        resetButton.clicked.connect(self.reset)

        # Run 알고리즘은 크게 실행도중인 경우 / 아닌경우, 아닌경우에서 Alg_Select가 어떤 알고리즘을 골랐느냐에 따라 선정이 달라질거임.
        # Run과 Stop은 최하단에서 선언해서 실행하도록 해야할것..아마?
        # 첫실행시에 Stop은 비활성, Run 누르면 활성 이렇게 해야할듯?
        self.Run_Alg = QPushButton("Run", self)
        self.Run_Alg.clicked.connect(self.Run_Algorithm)
        self.Run_Alg.setDisabled(True)

        self.history_slider = QSlider(Qt.Horizontal, self)
        self.history_slider.setDisabled(True)
        self.history_slider.valueChanged.connect(self.slider_Control)
        # 첫째줄, 그리드에 프로세스 이름, AT, BT, 추가버튼, 리셋버튼 추가
        grid_Line1 = QGridLayout()
        grid_Line1.addWidget(QLabel("Algorithm"), 0, 0)
        grid_Line1.addWidget(QLabel("Process Name"), 0, 1)
        grid_Line1.addWidget(self.ATLabel, 0, 2)
        grid_Line1.addWidget(QLabel("BT"), 0, 3)
        grid_Line1.addWidget(self.Alg_Select, 1, 0)
        grid_Line1.addWidget(self.ProName, 1, 1)
        grid_Line1.addWidget(self.AT, 1, 2)
        grid_Line1.addWidget(self.BT, 1, 3)
        grid_Line1.addWidget(QLabel("대상 학생"),0,4)
        grid_Line1.addWidget(self.StudentList,1,4)
        grid_Line1.addWidget(self.addButton, 1, 5)
        grid_Line1.addWidget(resetButton, 1, 6)

        # 두번째 줄 오른편의 그리드, cpu_count, TQ, Run_Alg, Stop_Alg을 그리드 레이아웃에 추가
        grid_Line2 = QGridLayout()
        grid_Line2.addWidget(self.CPULabel, 0, 0)
        grid_Line2.addWidget(self.cpu_count, 0, 1)
        grid_Line2.addWidget(self.TQLabel, 1, 0)
        grid_Line2.addWidget(self.TQ, 1, 1)
        grid_Line2.addWidget(QLabel("팀프 시간"),2,0)
        grid_Line2.addWidget(self.TP_Time,2,1)
        grid_Line2.addWidget(self.Run_Alg, 3, 0)

        # 두번째 줄을 통합해줄 hbox_Line2, Proc_Table과 grid_Line2를 레이아웃에 추가함.
        hbox_Line2 = QHBoxLayout()
        hbox_Line2.addWidget(self.Proc_Table)
        hbox_Line2.addLayout(grid_Line2)

        # 그냥 이름용
        vbox_Line3 = QVBoxLayout()
        Ready_Name = QLabel("Ready Queue")
        Ready_Name.setMaximumHeight(25)  # 수정 : ready queue 글자가 잘려서 25로 늘렸음
        vbox_Line3.addWidget(Ready_Name)
        vbox_Line3.addWidget(self.Ready_Table)

        hbox_Line4 = QHBoxLayout()
        hbox_Line4.addWidget(QLabel("Gantt Chart"))
        hbox_Line4.addWidget(self.realTimeLabel)

        # 레이아웃 및 위젯을 통합할 vbox_main을 선언, 메인 레이아웃 지정 후 레이아웃 및 위젯 통합
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)
        vbox_main.addLayout(grid_Line1)
        vbox_main.addLayout(hbox_Line2)
        vbox_main.addWidget(self.history_slider)
        vbox_main.addLayout(vbox_Line3)
        vbox_main.addLayout(hbox_Line4)
        vbox_main.addWidget(self.Gantt_Table)
        vbox_main.addWidget(self.Result_Table)
        # vbox_main.addStretch(3)
        self.setWindowTitle("Process Scheduling Simulator")
        # setGeometry가 크기랑 위치 지정하는건데 잘몰르겟음 필요한가, 센터로 화면 가운데 위치지정중임
        # self.setGeometry(0, 0, 800, 600)
        self.center()
        self.show()

    def center(self):
        # 프로그램이 화면 중앙을 알아서 찾아가는 함수
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def enableSlot(self):
        if self.Alg_Select.currentText() == "YOSA":
            self.reset()
            # 화면을 YOSA용 세팅으로 변경
            self.YOSASetting()
        else:
            # 이전 세팅이 YOSA 였다면
            if self.cur_algo == "YOSA":
                self.reset()
                # 화면을 기본 세팅으로 바꿈
                self.defaultSetting()
            if self.Alg_Select.currentText() == "RR":
                self.TQ.setEnabled(True)
            else:
                self.TQ.setDisabled(True)
        self.cur_algo = self.Alg_Select.currentText() 

    def setCPUTable_slot(self):
        NameHeader = []
        CPU_Select = int(self.cpu_count.currentText())
        self.Gantt_Table.setRowCount(CPU_Select)
        if self.Alg_Select.currentText() == "YOSA":
            for i in range(1, CPU_Select + 1):
                NameHeader.append("학생 " + str(i))
            # CPU에 개수에 따라 변동되는 내역들은 전부 여기에 있다고 생각하면 편함
            self.Result_Table.setRowCount(CPU_Select)
            self.Result_Table.verticalHeader().setVisible(True)
            self.Result_Table.setVerticalHeaderLabels(NameHeader)
            header = self.Result_Table.verticalHeader()
            for i in range(len(NameHeader)):
                header.setSectionResizeMode(i, QHeaderView.Stretch)
            # 팀프의 최대 시간은 학생의 수 * 24
            self.TP_Time.setRange(1,CPU_Select*24)
            self.StudentList.clear()
            for i in range(1, CPU_Select + 1):
                self.StudentList.addItem("학생 " + str(i))
        else:
            for i in range(1, CPU_Select + 1):
                NameHeader.append("CPU " + str(i))
        # 간트차트 정렬 하는거
        self.Gantt_Table.setVerticalHeaderLabels(NameHeader)
        header = self.Gantt_Table.verticalHeader()
        for i in range(len(NameHeader)):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

    # 수정 : 디버깅용(자동 입력 해줌 - 프로세스 개수, AT, BT까지 자동으로 입력)
    def test(self):
        self.Run_Alg.setEnabled(True)
        # Proc_List에 프로세스를 저장.======================
        for process_id in range(random.randrange(1, 16)):
            self.Proc_List.append(
                Process("p" + str(process_id), random.randrange(0, 10), random.randrange(1, 8), process_id)
            )
        # ===============================================
        # 테스트 값 내가 넣어줄때-----------
        # self.Proc_List = [
        #     Process("p0", 8, 7, 0),
        #     Process("p1", 3, 4, 1),
        #     Process("p2", 4, 7, 2),
        #     Process("p3", 9, 5, 3),
        #     Process("p4", 1, 6, 4),
        #     Process("p5", 0, 6, 5),
        #     Process("p6", 9, 6, 6),
        #     Process("p7", 0, 7, 7),
        #     Process("p8", 1, 7, 8),
        # ]
        # ----------------------------
        print("[self.Proc_List]")
        print("[", end="")
        for idx, process in enumerate(self.Proc_List):
            print("Process('{0}', {1}, {2}, {3}),".format(process.process_id, process.AT, process.BT, idx), end="")
        print("]")
        # 기본
        # self.Proc_List.append(Process("p1", 0, 3))
        # self.Proc_List.append(Process("p2", 1, 7))
        # self.Proc_List.append(Process("p3", 3, 2))
        # self.Proc_List.append(Process("p4", 5, 5))
        # self.Proc_List.append(Process("p5", 6, 3))
        # 이후 Proc_Table에 프로세스를 띄우도록 함, 열크기 = Proc_List 크기
        self.Proc_Table.setRowCount(len(self.Proc_List))
        for i in range(len(self.Proc_List)):
            self.Proc_Table.setItem(i, 0, QTableWidgetItem(self.Proc_List[i].process_id))
            self.Proc_Table.item(i, 0).setBackground(
                QtGui.QColor(self.Proc_List[i].Color[0], self.Proc_List[i].Color[1], self.Proc_List[i].Color[2])
            )
            # if self.Proc_List[i].Color[0] + self.Proc_List[i].Color[1] + self.Proc_List[i].Color[2] < 350:
            #     self.Proc_Table.item(i, 0).setForeground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
            self.Proc_Table.setItem(i, 1, QTableWidgetItem(str(self.Proc_List[i].AT)))
            self.Proc_Table.setItem(i, 2, QTableWidgetItem(str(self.Proc_List[i].BT)))
        # 초기화 부분
        self.ProName.clear()
        self.AT.setValue(0)
        self.BT.setValue(0)

    def add(self):
        self.Run_Alg.setEnabled(True)
        # Proc_List에 프로세스를 저장.
        if self.cur_algo != "YOSA":
            self.Proc_List.append(Process(self.ProName.text(), self.AT.value(), self.BT.value()))
        # YOSA인 경우 해당되는 CPU의 정보도 같이 넣어줌
        else:
            # select에 선택한 학생 번호를 넣어주고, 이를 Proc_List에 넣을떄 같이 넣어줌
            select = int(self.StudentList.currentText()[-1])
            self.Proc_List.append(Process(self.ProName.text(), self.AT.value(), self.BT.value(), random.randrange(1, 15), select))
            self.proc_Count[select -  1] += 1
            # 만약 학생 3이 해야하는 프로세스가 등록이 되었을 때, 이후 학생 수를 1이나 2로 선정하고 run을 돌리면 문제가 될 것.
            # 이를 보완하기 위해 학생 3이 해야하는 프로세스가 등록이 되면 학생수 1이나 2를 비활성화 하함
            while(int(self.cpu_count.itemText(0)) < select):
                  self.cpu_count.removeItem(0)
            # 만약 해당 학생의 프로세스 개수가 4가 되면 StudentList의 해당 학생을 빼서 더이상 넣지 못하게 함
            # 그리고 그런 상황에서 cpu_count 건들면 괜히 이상해질거같으니 cpu_count 비활성화 
            if self.proc_Count[select -  1] == 4:
                find = "학생 " + str(select)
                deleteIndex = self.StudentList.findText(find)
                self.StudentList.removeItem(deleteIndex)
                self.cpu_count.setDisabled(True)
            # 위에 하면서 StudentList 내용 지우다가 내용 싹다 없어지면 addbutton 비활성화
            if self.StudentList.count() == 0:
                self.addButton.setDisabled(True)
        # 이후 Proc_Table에 프로세스를 띄우도록 함, 열크기 = Proc_List 크기
        self.Proc_Table.setRowCount(len(self.Proc_List))
        for i in range(len(self.Proc_List)):
            self.Proc_Table.setItem(i, 0, QTableWidgetItem(self.Proc_List[i].process_id))
            self.Proc_Table.item(i, 0).setBackground(
                QtGui.QColor(self.Proc_List[i].Color[0], self.Proc_List[i].Color[1], self.Proc_List[i].Color[2])
            )
            self.Proc_Table.setItem(i, 1, QTableWidgetItem(str(self.Proc_List[i].AT)))
            self.Proc_Table.setItem(i, 2, QTableWidgetItem(str(self.Proc_List[i].BT)))
            if self.cur_algo == "YOSA":
                # YOSA인 경우엔 select_CPU값도 넣어줌
                self.Proc_Table.setItem(i, 3, QTableWidgetItem("학생 " + str(self.Proc_List[i].select_CPU)))
        # 초기화 부분
        self.ProName.clear()
        self.AT.setValue(0)
        self.BT.setValue(1)

    def reset(self):
        # Proc_Table과 Result_Table 열을 0으로 만들고 Proc_List를 clear
        self.Proc_Table.setRowCount(0)

        # 수정 : Ready_Table - reset 안되는 문제 해결
        self.Ready_Table.clear()
        self.Ready_Table.setColumnCount(0)

        self.Gantt_Table.setColumnCount(0)
        self.Result_Table.setRowCount(0)
        self.Run_Alg.setDisabled(True)
        self.Proc_List.clear()
        self.history.clear()
        self.history_slider.setDisabled(True)
        self.addButton.setEnabled(True)
        # YOSA에서 학생 목록 지워버린것도 고려해야해서 setCPUTable_slot 넣었음
        self.setCPUTable_slot()
        self.cpu_count.setEnabled(True)
        # cpu_count 건드리는 일이 있다면, 이것도 같이 써두는 것이 나을 것이라 생각함.
        self.cpu_count.clear()
        for cpu_idx in range(1, 5):
            self.cpu_count.addItem(str(cpu_idx))
        for i in range(len(self.proc_Count)):
            self.proc_Count[i] = 0

    # 알고리즘 실행
    def Run_Algorithm(self):
        # 아직 알고리즘 구분 안넣고 RR을 시험삼아 돌림, 그래서 Quantum설정 하려면 RR선택하고 돌려볼것

        # 수정 : 알고리즘 선택하는 부분
        # 한번 설정한 프로세스 목록을 계속해서 돌릴 상황을 가정해야하기 떄문에 깊은 복사로 PList에 가져와서 실행
        PList = copy.deepcopy(self.Proc_List)
        if self.Alg_Select.currentText() == "FCFS":
            scheduler = FCFS(PList, int(self.cpu_count.currentText()))
        elif self.Alg_Select.currentText() == "RR":
            scheduler = RR(PList, int(self.cpu_count.currentText()), self.TQ.value())
        elif self.Alg_Select.currentText() == "SPN":
            scheduler = SPN(PList, int(self.cpu_count.currentText()))
        elif self.Alg_Select.currentText() == "SRTN":
            scheduler = SRTN(PList, int(self.cpu_count.currentText()))
        elif self.Alg_Select.currentText() == "HRRN":
            scheduler = HRRN(PList, int(self.cpu_count.currentText()))
        # elif self.Alg_Select.currentText() == "YOSA":
        #     scheduler = YOSA(PList, int(self.cpu_count.currentText()))

        scheduler.run()
        # 실행 이후 히스토리를 self.history에 저장
        self.history = scheduler.history
        # len(self.history) = 경과 시간, 경과 시간을 탐색할 수 있게 슬라이더를 활성화하고 슬라이더의 범위 지정, 초기는 0초
        self.history_slider.setEnabled(True)
        self.history_slider.setRange(0, len(self.history) - 1)
        self.history_slider.setValue(0)
        # 이후 함수들은 0초를 기준으로 화면에 띄우는것, slider_Control과 거이 동일하기 때문에 거기에 주석을 달겠습니다.
        self.Ready_Table.setColumnCount(len(self.history[0][0]))
        self.Gantt_Table.setColumnCount(0)
        self.Result_Table.setRowCount(len(self.history[0][2]))

        ready_queue_count = len(self.history[0][0])
        cpu_count = len(self.history[0][1])
        process_count = len(self.history[0][2])

        for queue_process_idx in range(ready_queue_count):
            self.Ready_Table.setItem(
                0, queue_process_idx, QTableWidgetItem(self.history[0][0][queue_process_idx].process_id)
            )
            self.Ready_Table.item(0, queue_process_idx).setBackground(
                QtGui.QColor(
                    self.history[0][0][queue_process_idx].Color[0],
                    self.history[0][0][queue_process_idx].Color[1],
                    self.history[0][0][queue_process_idx].Color[2],
                )
            )
            # DEBUG
            # print("queue:", self.history[0][0][queue_process_idx].process_id)

        # 처음에는 간트 차트 출력 X
        # for cpu in range(cpu_count):
        #     if self.history[1][1][cpu]:
        #         print("CHECK:", self.history[1][1][cpu].process_id)
        #         self.Gantt_Table.setItem(cpu, 0, QTableWidgetItem(self.history[1][1][cpu].process_id))
        #         self.Gantt_Table.item(cpu, 0).setBackground(
        #             QtGui.QColor(
        #                 self.history[1][1][cpu].Color[0],
        #                 self.history[1][1][cpu].Color[1],
        #                 self.history[1][1][cpu].Color[2],
        #             )
        #         )
        # print("gantt:", self.history[0][1][cpu].process_id)

        for process in range(process_count):
            self.Result_Table.setItem(process, 0, QTableWidgetItem(self.history[0][2][process].process_id))
            self.Result_Table.setItem(process, 1, QTableWidgetItem(str(self.history[0][2][process].AT)))
            self.Result_Table.setItem(process, 2, QTableWidgetItem(str(self.history[0][2][process].BT)))
            self.Result_Table.setItem(process, 3, QTableWidgetItem(str(self.history[0][2][process].WT)))
            self.Result_Table.setItem(process, 4, QTableWidgetItem(str(self.history[0][2][process].TT)))
            self.Result_Table.setItem(process, 5, QTableWidgetItem(str(self.history[0][2][process].NTT)))
            self.Result_Table.item(process, 0).setBackground(
                QtGui.QColor(
                    self.history[0][2][process].Color[0],
                    self.history[0][2][process].Color[1],
                    self.history[0][2][process].Color[2],
                )
            )
            # print("result:", self.history[0][2][process].process_id)

        self.Ready_Table.repaint()
        self.Gantt_Table.repaint()
        self.Result_Table.repaint()

    def slider_Control(self):
        # 초 = 슬라이더의 값
        second = self.history_slider.value()
        ready_queue_count = len(self.history[second][0])
        cpu_count = len(self.history[0][1])
        process_count = len(self.history[0][2])

        # 표의 너비 지정
        self.Ready_Table.setColumnCount(len(self.history[second][0]))
        self.Gantt_Table.setColumnCount(second)
        self.Result_Table.setRowCount(len(self.history[second][2]))
        # 레디 큐에 저장된 프로세스를 Ready_Table에 넣는 과정
        for queue_process_idx in range(ready_queue_count):
            self.Ready_Table.setItem(
                0, queue_process_idx, QTableWidgetItem(self.history[second][0][queue_process_idx].process_id)
            )
            self.Ready_Table.item(0, queue_process_idx).setBackground(
                QtGui.QColor(
                    self.history[second][0][queue_process_idx].Color[0],
                    self.history[second][0][queue_process_idx].Color[1],
                    self.history[second][0][queue_process_idx].Color[2],
                )
            )
            # print("queue:", self.history[second][0][queue_process_idx].process_id)

        # ==================================================================
        # history CPU를 매초마다 탐색해서 CPU내에 들어간 프로세스를 넣는 과정
        max_len_cpu = 0
        for seconds in range(second):
            for cpu in range(cpu_count):
                # CPU가 쉬는 도중에는 할당될 프로세스가 없을 가능성 존재
                if self.history[seconds + 1][1][cpu]:
                    max_len_cpu = cpu
                    self.Gantt_Table.setItem(
                        cpu, seconds, QTableWidgetItem(self.history[seconds + 1][1][cpu].process_id)
                    )
                    # 이거 if 안넣으면 NoneType떠서 넣긴했는데 이유 솔직히 모르겠음.. 저도 모르겠네요...
                    self.Gantt_Table.item(cpu, seconds).setBackground(
                        QtGui.QColor(
                            self.history[seconds + 1][1][cpu].Color[0],
                            self.history[seconds + 1][1][cpu].Color[1],
                            self.history[seconds + 1][1][cpu].Color[2],
                        )
                    )

        self.Gantt_Table.scrollToItem(self.Gantt_Table.item(max_len_cpu, second - 1))
        # 결과 테이블에 프로세스의 현황을 넣는 과정, 근데 계산 끝난 결과로만 출력이 되는데 왜 그러는지 잘 모르겠음.
        # 굳이 매초마다 갱신할 필요가 없으면 슬라이더 옮길때마다 매번 갱신할 필요가 없어서 이부분은 지워도 괜찮음.

        self.Ready_Table.repaint()
        self.Gantt_Table.repaint()
       
        # 경과시간 표시하는 라벨 수정하는거
        if Alg_Select.currentText() == "YOSA":
            fortext = "Real Time = " + str(second) + " hour"
            self.realTimeLabel.setText(fortext)
        else:
            fortext = "Real Time = " + str(second) + " sec"
            self.realTimeLabel.setText(fortext)
        self.realTimeLabel.repaint()

    def defaultSetting(self):
        # AT BT 범위 바꾼거 수정
        self.AT.setRange(0, 65535)
        self.ATLabel.setText("AT")
        self.BT.setRange(1, 65535)
        self.CPULabel.setText("CPU")
        self.TQ.setRange(1, 65535)
        self.TQLabel.setText("Quantum")
        # Proc_Table 기본 세팅
        self.Proc_Table.setColumnCount(3)
        self.Proc_Table.setHorizontalHeaderLabels(["Process Name", "Arrival Time", "Burst Time"])
        header = self.Proc_Table.horizontalHeader()
        for column_idx in range(self.column_count):
            header.setSectionResizeMode(column_idx, QHeaderView.Stretch)
        # Gantt Table 기본 세팅
        self.setCPUTable_slot()
        # Result_Table 기본 세팅
        self.Result_Table.setColumnCount(6)
        self.Result_Table.setHorizontalHeaderLabels(
            ["Process Name", "Arrival Time", "Burst Time", "Waiting Time", "Turnaround Time", "Normalized TT"]
        )
        self.Result_Table.verticalHeader().setVisible(False)
        header = self.Result_Table.horizontalHeader()
        for time_table_col in range(6):
            header.setSectionResizeMode(time_table_col, QHeaderView.Stretch)
        self.realTimeLabel.setText("Real Time = 0 sec")
        self.StudentList.setDisabled(True)
        self.TP_Time.setDisabled(True)

    def YOSASetting(self):
        # AT BT 범위 바꾼거 수정
        self.AT.setRange(1, 4)
        self.ATLabel.setText("학점")
        self.BT.setRange(1, 24)
        self.CPULabel.setText("학생 수")
        self.TQ.setRange(1, 4)
        self.TQLabel.setText("팀프 학점")
        # Proc_Table 기본 세팅
        self.Proc_Table.setColumnCount(4)
        self.Proc_Table.setHorizontalHeaderLabels(["과목 이름", "학점", "소요 시간", "대상 인원"])
        header = self.Proc_Table.horizontalHeader()
        for column_idx in range(4):
            header.setSectionResizeMode(column_idx, QHeaderView.Stretch)
        # Gantt Table 기본 세팅
        # 이건 setCPU 여기서 바꿔야할듯
        self.setCPUTable_slot()
        # Result_Table 기본 세팅
        self.Result_Table.setColumnCount(7)
        self.Result_Table.setHorizontalHeaderLabels(
            ["개인 공부 투자시간", "팀프 투자 시간", "과목 1 학점", "과목 2 학점", "과목 3 학점", "과목 4 학점", "평균 학점"]
        )
        # Result의 Vertical과 StudentList부분은 setCPUTAble_slot으로 넘김
        
        header = self.Result_Table.horizontalHeader()
        for time_table_col in range(7):
            header.setSectionResizeMode(time_table_col, QHeaderView.Stretch)
        self.realTimeLabel.setText("Real Time = 0 hour")
        self.StudentList.setEnabled(True)
        self.TQ.setEnabled(True)
        self.TP_Time.setEnabled(True)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

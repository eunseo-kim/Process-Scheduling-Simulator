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
        self.proc_list = []
        self.history = []
        self.algo_list = ["FCFS", "RR", "SPN", "SRTN", "HRRN", "YOSA"]
        self.column_count = 3
        self.cur_algo = "FCFS"
        self.process_count = 0
        self.subject_count = [0, 0, 0, 0]
        self.initUI()

    # 수정 : font
    def change_font(self):
        font = QtGui.QFont()
        # 폰트 없으시면 주석 처리하세요!
        font.setFamily("카카오 Regular")
        # font.setFamily("Consolas")
        font.setPointSize(10)
        # font.setBold(True)
        self.setFont(font)

    def initUI(self):
        self.resize(1400, 900)
        self.center()

        # 알고리즘 종류를 선택핧 Alg_Select를 콤보박스로 구현
        self.alg_select = QComboBox(self)
        for algo in self.algo_list:
            self.alg_select.addItem(algo)
        self.alg_select.activated.connect(self.enableSlot)

        # 프로세스 이름을 사용자에게 받을 ProName, AT를 사용자에게 받을 AT, BT를 사용자에게 받을 BT
        # AT와 BT같이 사용자에게 숫자로만 받을거라면 스핀박스로 하는게 더 편하다고 함
        self.process_name = QLineEdit()
        self.process_name.setMaxLength(10)
        self.AT_label = QLabel("AT")
        self.AT = QSpinBox()
        self.AT.setRange(0, 65535)
        self.BT = QSpinBox()
        self.BT.setRange(1, 65535)
        self.student_list = QComboBox(self)
        self.student_list.addItem("학생 1")
        self.student_list.setDisabled(True)
        # 프로세스 목록을 표로 보여줄 Proc_Table선언
        self.proc_table = QTableWidget(self)
        self.proc_table.setColumnCount(3)
        self.proc_table.setHorizontalHeaderLabels(["Process Name", "Arrival Time", "Burst Time"])

        self.proc_table.verticalHeader().setVisible(False)
        header = self.proc_table.horizontalHeader()
        for column_idx in range(self.column_count):
            header.setSectionResizeMode(column_idx, QHeaderView.Stretch)

        # CPU의 코어 개수 선택에 사용할 cpu_count를 콤보박스로 선언
        self.cpu_count = QComboBox(self)
        for cpu_idx in range(1, 5):
            self.cpu_count.addItem(str(cpu_idx))
        self.cpu_count.activated.connect(self.set_CPU_slot)
        self.CPU_label = QLabel("CPU")

        # Ready Queue 보여줄 테이블
        self.ready_table = QTableWidget(self)
        self.ready_table.setRowCount(1)
        self.ready_table.verticalHeader().setVisible(False)
        self.ready_table.setMaximumHeight(50)
        self.ready_table.verticalHeader().setDefaultSectionSize(50)
        self.ready_table.horizontalHeader().setVisible(False)

        # CPU 일 목록
        self.gantt_table = QTableWidget(self)
        self.gantt_table.setRowCount(1)
        self.gantt_table.setVerticalHeaderLabels(["CPU 1"])
        header = self.gantt_table.verticalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)

        self.real_time_label = QLabel("Real Time = 0 sec")
        # quantum을 넣는 스핀박스, 초기는 FCFS이기에 비활성화해둠
        self.TQ = QSpinBox()
        self.TQ.setRange(1, 65535)
        self.TQ.setDisabled(True)
        self.TQ_label = QLabel("Quantum")



        # Gantt Chart를 표로 보여줄 Result_Table선언
        self.result_table = QTableWidget(self)
        self.result_table.setColumnCount(6)
        self.result_table.setHorizontalHeaderLabels(
            ["Process Name", "Arrival Time", "Burst Time", "Waiting Time", "Turnaround Time", "Normalized TT"]
        )
        self.result_table.verticalHeader().setVisible(False)
        header = self.result_table.horizontalHeader()
        for time_table_col in range(6):
            header.setSectionResizeMode(time_table_col, QHeaderView.Stretch)

        # Proc_List에 프로세스 목록을 추가 및 화면 내용을 리셋하는 버튼 (이때문에 거진 뒤로 가야할듯)
        self.add_button = QPushButton("Add", self)
        self.add_button.clicked.connect(self.add)
        # 수정 : 디버깅용 test를 add 버튼에 일시적으로 연결 (test 누르면 자동으로 값 입력됨)
        # self.add_button.clicked.connect(self.test)

        reset_button = QPushButton("Reset", self)
        reset_button.clicked.connect(self.reset)
        
        # 알고리즘 실행 버튼
        self.run_alg = QPushButton("Run", self)
        self.run_alg.clicked.connect(self.run_algorithm)
        self.run_alg.setDisabled(True)

        # 각 히스토리 시간마다 보여주기 위한 슬라이드
        self.history_slider = QSlider(Qt.Horizontal, self)
        self.history_slider.setDisabled(True)
        self.history_slider.valueChanged.connect(self.slider_Control)
        # 첫째줄, 그리드에 프로세스 이름, AT, BT, 추가버튼, 리셋버튼 추가
        grid_Line1 = QGridLayout()
        grid_Line1.addWidget(QLabel("Algorithm"), 0, 0)
        grid_Line1.addWidget(QLabel("Process Name"), 0, 1)
        grid_Line1.addWidget(self.AT_label, 0, 2)
        grid_Line1.addWidget(QLabel("BT"), 0, 3)
        grid_Line1.addWidget(self.alg_select, 1, 0)
        grid_Line1.addWidget(self.process_name, 1, 1)
        grid_Line1.addWidget(self.AT, 1, 2)
        grid_Line1.addWidget(self.BT, 1, 3)
        grid_Line1.addWidget(QLabel("대상 학생"), 0, 4)
        grid_Line1.addWidget(self.student_list, 1, 4)
        grid_Line1.addWidget(self.add_button, 1, 5)
        grid_Line1.addWidget(reset_button, 1, 6)

        # 두번째 줄 오른편의 그리드, cpu_count, TQ, Run_Alg, Stop_Alg을 그리드 레이아웃에 추가
        grid_Line2 = QGridLayout()
        grid_Line2.addWidget(self.CPU_label, 0, 0)
        grid_Line2.addWidget(self.cpu_count, 0, 1)
        grid_Line2.addWidget(self.TQ_label, 1, 0)
        grid_Line2.addWidget(self.TQ, 1, 1)
        grid_Line2.addWidget(self.run_alg, 2, 0)

        # 두번째 줄을 통합해줄 hbox_Line2, Proc_Table과 grid_Line2를 레이아웃에 추가함.
        hbox_Line2 = QHBoxLayout()
        hbox_Line2.addWidget(self.proc_table)
        hbox_Line2.addLayout(grid_Line2)

        # 그냥 이름용
        vbox_Line3 = QVBoxLayout()
        ready_name = QLabel("Ready Queue")
        ready_name.setMaximumHeight(25)  # 수정 : ready queue 글자가 잘려서 25로 늘렸음
        vbox_Line3.addWidget(ready_name)
        vbox_Line3.addWidget(self.ready_table)

        hbox_Line4 = QHBoxLayout()
        hbox_Line4.addWidget(QLabel("Gantt Chart"))
        hbox_Line4.addWidget(self.real_time_label)

        # 레이아웃 및 위젯을 통합할 vbox_main을 선언, 메인 레이아웃 지정 후 레이아웃 및 위젯 통합
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)
        vbox_main.addLayout(grid_Line1)
        vbox_main.addLayout(hbox_Line2)
        vbox_main.addWidget(self.history_slider)
        vbox_main.addLayout(vbox_Line3)
        vbox_main.addLayout(hbox_Line4)
        vbox_main.addWidget(self.gantt_table)
        vbox_main.addWidget(self.result_table)
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
        if self.alg_select.currentText() != "YOSA":
            # 이전 세팅이 YOSA 였다면
            if self.cur_algo == "YOSA":
                self.reset()
                # 화면을 기본 세팅으로 바꿈
                self.default_setting()
            if self.alg_select.currentText() == "RR":
                self.TQ.setEnabled(True)
            else:
                self.TQ.setDisabled(True)
        else:
            self.reset()
            # 화면을 YOSA용 세팅으로 변경
            self.YOSA_setting()
        self.cur_algo = self.alg_select.currentText()

    def set_CPU_slot(self):
        name_header = []
        CPU_select = int(self.cpu_count.currentText())
        self.gantt_table.setRowCount(CPU_select)
        if self.alg_select.currentText() != "YOSA":
            for i in range(1, CPU_select + 1):
                name_header.append("CPU " + str(i))
        else:
            for i in range(1, CPU_select + 1):
                name_header.append("학생 " + str(i))
            # CPU에 개수에 따라 변동되는 내역들은 전부 여기에 있다고 생각하면 편함
            self.result_table.setRowCount(CPU_select)
            self.result_table.verticalHeader().setVisible(True)
            self.result_table.setVerticalHeaderLabels(name_header)
            # 팀원 전체 학점 평균의 셀 병합
            if CPU_select > 1:
                self.result_table.setSpan(0, 10, CPU_select, 1)
                self.result_table.setSpan(0, 12, CPU_select, 1)
            header = self.result_table.verticalHeader()
            for i in range(len(name_header)):
                header.setSectionResizeMode(i, QHeaderView.Stretch)
            self.student_list.clear()
            for i in range(1, CPU_select + 1):
                self.student_list.addItem("학생 " + str(i))
        # 간트차트 정렬 하는거
        self.gantt_table.setVerticalHeaderLabels(name_header)
        header = self.gantt_table.verticalHeader()
        for i in range(len(name_header)):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        # 프로그램 좀 굴리다 깨달은건데 run 돌리고 CPU 만지고 슬라이더 돌리면 오류생길수있음
        self.history_slider.setDisabled(True)

    # 수정 : 디버깅용(자동 입력 해줌 - 프로세스 개수, AT, BT까지 자동으로 입력)
    def test(self):
        self.run_alg.setEnabled(True)
        # Proc_List에 프로세스를 저장.======================
        for process_id in range(random.randrange(1, 16)):
            self.proc_list.append(
                Process("p" + str(process_id), random.randrange(0, 10), random.randrange(1, 8), process_id)
            )
        # ===============================================
        # 테스트 값 내가 넣어줄때-----------
        self.proc_list = [
            Process("p0", 1, 4, 0),
            Process("p1", 2, 3, 1),
            Process("p2", 2, 3, 2),
            Process("p3", 2, 3, 3),
            Process("p4", 2, 3, 4),
            Process("p5", 0, 2, 5),
            Process("p6", 0, 2, 6),
            Process("p7", 0, 2, 7),
            Process("p8", 1, 4, 8),
            Process("p9", 1, 4, 9),
        ]
        # ----------------------------
        self.proc_list = [
            Subject("알고리즘", 4, 8, 0, 0),
            Subject("웹프", 3, 7, 1, 0),
            Subject("직능훈", 2, 4, 2, 0),
            # Subject("알고리즘", 4, 5, 3, 1),
            Subject("C++", 4, 4, 4, 1),
            # Subject("웹프", 3, 3, 5, 1),
            # Subject("알고리즘", 4, 4, 6, 2),
            # Subject("데베설", 3, 5, 7, 2),
            # Subject("운영체제", 2, 6, 8, 2),
        ]

        #-------------------------------
        print("[self.proc_list]")
        print("[", end="")
        for idx, process in enumerate(self.proc_list):
            print("Process('{0}', {1}, {2}, {3}),".format(process.process_id, process.AT, process.BT, idx), end="")
        print("]")
        # 기본
        # self.proc_list.append(Process("p1", 0, 3))
        # self.proc_list.append(Process("p2", 1, 7))
        # self.proc_list.append(Process("p3", 3, 2))
        # self.proc_list.append(Process("p4", 5, 5))
        # self.proc_list.append(Process("p5", 6, 3))
        # 이후 Proc_Table에 프로세스를 띄우도록 함, 열크기 = Proc_List 크기
        self.proc_table.setRowCount(len(self.proc_list))
        for i in range(len(self.proc_list)):
            self.proc_table.setItem(i, 0, QTableWidgetItem(self.proc_list[i].process_id))
            self.proc_table.item(i, 0).setBackground(
                QtGui.QColor(self.proc_list[i].Color[0], self.proc_list[i].Color[1], self.proc_list[i].Color[2])
            )
            # if self.proc_list[i].Color[0] + self.proc_list[i].Color[1] + self.proc_list[i].Color[2] < 350:
            #     self.proc_table.item(i, 0).setForeground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
            self.proc_table.setItem(i, 1, QTableWidgetItem(str(self.proc_list[i].AT)))
            self.proc_table.setItem(i, 2, QTableWidgetItem(str(self.proc_list[i].BT)))
        # 초기화 부분
        self.process_name.clear()
        self.AT.setValue(0)
        self.BT.setValue(0)

    def add(self):
        self.run_alg.setEnabled(True)
        # Proc_List에 프로세스를 저장.
        if self.cur_algo != "YOSA":
            # 색상을 현재 프로세스 개수를 기준으로 매겨주고, 만약 프로세스가 15개가 넘어가면 추가를 막음.
            self.proc_list.append(
                Process(self.process_name.text(), self.AT.value(), self.BT.value(), self.process_count)
            )
            self.process_count += 1
            if self.process_count == 15:
                self.add_button.setDisabled(True)
        # YOSA인 경우 해당되는 CPU의 정보도 같이 넣어줌
        else:
            # select에 선택한 학생 번호를 넣어주고, 이를 Proc_List에 넣을떄 같이 넣어줌
            select = int(self.student_list.currentText()[-1])
            self.proc_list.append(
                Subject(self.process_name.text(), self.AT.value(), self.BT.value(), random.randrange(1, 15), select - 1)
            )
            self.subject_count[select - 1] += 1
            # 만약 학생 3이 해야하는 프로세스가 등록이 되었을 때, 이후 학생 수를 1이나 2로 선정하고 run을 돌리면 문제가 될 것.
            # 이를 보완하기 위해 학생 3이 해야하는 프로세스가 등록이 되면 학생수 1이랑 2를 비활성화 하함
            while int(self.cpu_count.itemText(0)) < select:
                self.cpu_count.removeItem(0)
            # 만약 해당 학생의 프로세스 개수가 4가 되면 StudentList의 해당 학생을 빼서 더이상 넣지 못하게 함
            # 그리고 그런 상황에서 cpu_count 건들면 괜히 이상해질거같으니 cpu_count 비활성화
            if self.subject_count[select - 1] == 4:
                find = "학생 " + str(select)
                deleteIndex = self.student_list.findText(find)
                self.student_list.removeItem(deleteIndex)
                self.cpu_count.setDisabled(True)
            # 위에 하면서 StudentList 내용 지우다가 내용 싹다 없어지면 addbutton 비활성화
            if self.student_list.count() == 0:
                self.add_button.setDisabled(True)
        # 이후 Proc_Table에 프로세스를 띄우도록 함, 열크기 = Proc_List 크기
        self.proc_table.setRowCount(len(self.proc_list))
        for proc_idx, process in enumerate(self.proc_list):
            self.proc_table.setItem(proc_idx, 0, QTableWidgetItem(process.process_id))
            self.proc_table.item(proc_idx, 0).setBackground(
                QtGui.QColor(process.Color[0], process.Color[1], process.Color[2])
            )
            self.proc_table.setItem(proc_idx, 2, QTableWidgetItem(str(process.BT)))
            if self.cur_algo != "YOSA":
                # YOSA가 아닌경우엔 AT를 
                self.proc_table.setItem(proc_idx, 1, QTableWidgetItem(str(process.AT)))
            else:
                # YOSA인 경우엔 student_id값과 학점을 넣어줌, 위에서 YOSA 구분때 넣을까 했는데 그러면 코드 줄 늘어나서 안했음
                self.proc_table.setItem(proc_idx, 1, QTableWidgetItem(str(process.credit)))
                self.proc_table.setItem(proc_idx, 3, QTableWidgetItem("학생 " + str(process.student_id + 1)))

        # 초기화 부분
        self.process_name.clear()
        self.AT.setValue(0)
        self.BT.setValue(1)

    def reset(self):
        # Proc_Table과 Result_Table 열을 0으로 만들고 Proc_List를 clear
        self.proc_table.setRowCount(0)

        # 수정 : Ready_Table - reset 안되는 문제 해결
        self.ready_table.clear()
        self.ready_table.setColumnCount(0)

        self.gantt_table.setColumnCount(0)
        self.result_table.setRowCount(0)
        self.run_alg.setDisabled(True)
        self.proc_list.clear()
        self.history.clear()
        self.history_slider.setDisabled(True)
        self.add_button.setEnabled(True)
        # YOSA에서 학생 목록 지워버린것도 고려해야해서 set_CPU_slot 넣었음
        self.set_CPU_slot()
        self.cpu_count.setEnabled(True)
        # cpu_count 건드릴 일 있으니 cpu_count 갱신해줘야함.
        self.cpu_count.clear()
        for cpu_idx in range(1, 5):
            self.cpu_count.addItem(str(cpu_idx))
        self.subject_count = [0, 0, 0, 0]
        self.process_count = 0

    # 알고리즘 실행
    def run_algorithm(self):
        # 아직 알고리즘 구분 안넣고 RR을 시험삼아 돌림, 그래서 Quantum설정 하려면 RR선택하고 돌려볼것

        # 수정 : 알고리즘 선택하는 부분
        # 한번 설정한 프로세스 목록을 계속해서 돌릴 상황을 가정해야하기 떄문에 깊은 복사로 PList에 가져와서 실행
        PList = copy.deepcopy(self.proc_list)
        if self.cur_algo == "FCFS":
            scheduler = FCFS(PList, int(self.cpu_count.currentText()))
        elif self.cur_algo == "RR":
            scheduler = RR(PList, int(self.cpu_count.currentText()), self.TQ.value())
        elif self.cur_algo == "SPN":
            scheduler = SPN(PList, int(self.cpu_count.currentText()))
        elif self.cur_algo == "SRTN":
            scheduler = SRTN(PList, int(self.cpu_count.currentText()))
        elif self.cur_algo == "HRRN":
            scheduler = HRRN(PList, int(self.cpu_count.currentText()))
        elif self.cur_algo == "YOSA":
            scheduler = YOSA(PList, int(self.cpu_count.currentText()), self.TQ.value())

        scheduler.run()
        self.history_slider.setEnabled(True)
        # 실행 이후 히스토리를 self.history에 저장
        # 이후 함수들은 0초를 기준으로 화면에 띄우는것, slider_Control과 거이 동일하기 때문에 거기에 주석을 달겠습니다.
        # history가 어케될지는 모르겠는데, 이쪽이 어떻게 되냐에 따라서 여기 밑부터 YOSA인경우, 아닌경우 나눠서 해야할수도 있음

        # 처음에는 간트 차트 출력 X
        # for cpu in range(cpu_count):
        #     if self.history[1][1][cpu]:
        #         print("CHECK:", self.history[1][1][cpu].process_id)
        #         self.gantt_table.setItem(cpu, 0, QTableWidgetItem(self.history[1][1][cpu].process_id))
        #         self.gantt_table.item(cpu, 0).setBackground(
        #             QtGui.QColor(
        #                 self.history[1][1][cpu].Color[0],
        #                 self.history[1][1][cpu].Color[1],
        #                 self.history[1][1][cpu].Color[2],
        #             )
        #         )
        # print("gantt:", self.history[0][1][cpu].process_id)
        if self.cur_algo != "YOSA":
            self.history = scheduler.history
            # len(self.history) = 경과 시간, 경과 시간을 탐색할 수 있게 슬라이더를 활성화하고 슬라이더의 범위 지정, 초기는 0초
            self.history_slider.setRange(0, len(self.history) - 1)
            self.history_slider.setValue(0)
            self.ready_table.setColumnCount(len(self.history[0][0]))
            self.gantt_table.setColumnCount(0)
            self.result_table.setRowCount(len(self.history[0][2]))

            for Q_proc_idx, Q_process in enumerate(self.history[0][0]):
                self.ready_table.setItem(
                    0, Q_proc_idx, QTableWidgetItem(Q_process.process_id)
                )
                self.ready_table.item(0, Q_proc_idx).setBackground(
                    QtGui.QColor(
                        Q_process.Color[0],
                        Q_process.Color[1],
                        Q_process.Color[2],
                    )
                )
            # DEBUG
            # print("queue:", self.history[0][0][queue_process_idx].process_id)
            for proc_idx, process in enumerate(self.history[0][2]):
                self.result_table.setItem(proc_idx, 0, QTableWidgetItem(process.process_id))
                self.result_table.setItem(proc_idx, 1, QTableWidgetItem(str(process.AT)))
                self.result_table.setItem(proc_idx, 2, QTableWidgetItem(str(process.BT)))
                self.result_table.setItem(proc_idx, 3, QTableWidgetItem(str(process.WT)))
                self.result_table.setItem(proc_idx, 4, QTableWidgetItem(str(process.TT)))
                self.result_table.setItem(proc_idx, 5, QTableWidgetItem(str(process.NTT)))
                self.result_table.item(proc_idx, 0).setBackground(
                    QtGui.QColor(
                        process.Color[0],
                        process.Color[1],
                        process.Color[2],
                    )
                )
            
        else:
            self.history = scheduler.each_student_history_list
            self.history_slider.setRange(0, 24)
            self.history_slider.setValue(0)
            print(scheduler.students[0].best_solo_total_study_time)
            # self.history[0][2]부분이 YOSA의 student 목록을 반환할 것이라 가정하고 코드를 작성.
            # self.history[0][2]부분이 student가 아닌 경우는 이에 맞춰서 코드를 수정할 필요가 있음.

            for student_idx, student in enumerate(scheduler.students):
                # 공부시간
                self.result_table.setItem(
                    student_idx, 0, QTableWidgetItem(str(student.best_solo_total_study_time))
                )
                # 각 과목 당 공부 시간
                for subject in range(len(student.best_solo_subjects_grade)):
                    self.result_table.setItem(
                        student_idx,
                        1 + subject * 2,
                        QTableWidgetItem(str(student.best_solo_subject_study_case[subject])),
                    )
                    self.result_table.setItem(
                        student_idx, 2 + subject * 2, QTableWidgetItem(str(student.best_solo_subjects_grade[subject]))
                    )
                self.result_table.setItem(
                    student_idx, 9, QTableWidgetItem(str(student.best_each_team_play_time))
                )
                self.result_table.setItem(student_idx, 11, QTableWidgetItem(str(student.best_avg_grade)))

            # 팀플 학점과 전체 평균은 병합했기에 한번만 입력하면 될 것이라 생각
            self.result_table.setItem(0, 10, QTableWidgetItem(str(scheduler.students[0].best_team_play_grade)))
            self.result_table.setItem(0, 12, QTableWidgetItem(str(scheduler.team_avg_grade)))

    def slider_Control(self):
        # 원래 repaint 있던 부분들은 1초마다 자동갱신때 쓰던거라 필요없어서 지움
        # 초 = 슬라이더의 값
        second = self.history_slider.value()
        # 표의 너비 지정
        if self.cur_algo != "YOSA":
            cpu_count = len(self.history[0][1])
            self.ready_table.setColumnCount(len(self.history[second][0]))
            self.gantt_table.setColumnCount(second)
            for Q_proc_idx, Q_process in enumerate(self.history[second][0]):
                self.ready_table.setItem(
                    0, Q_proc_idx, QTableWidgetItem(Q_process.process_id)
                )
                self.ready_table.item(0, Q_proc_idx).setBackground(
                    QtGui.QColor(
                        Q_process.Color[0],
                        Q_process.Color[1],
                        Q_process.Color[2],
                    )
                )
            max_len_cpu = 0
            for seconds in range(second):
                for cpu in range(cpu_count):
                # CPU가 쉬는 도중에는 할당될 프로세스가 없을 가능성 존재
                    if self.history[seconds + 1][1][cpu]:
                        max_len_cpu = cpu
                        self.gantt_table.setItem(
                            cpu, seconds, QTableWidgetItem(self.history[seconds + 1][1][cpu].process_id)
                        )
                        self.gantt_table.item(cpu, seconds).setBackground(
                            QtGui.QColor(
                                self.history[seconds + 1][1][cpu].Color[0],
                                self.history[seconds + 1][1][cpu].Color[1],
                                self.history[seconds + 1][1][cpu].Color[2],
                            )
                        )

            self.gantt_table.scrollToItem(self.gantt_table.item(max_len_cpu, second - 1))
            fortext = "Real Time = " + str(second) + " sec"
            self.real_time_label.setText(fortext)
            # 매초마다 Result_Table값이 바뀌지 않기 떄문에 Result_Table 갱신 내역은 지웠음
        else:
            max_len_student = 0
            student_count = len(self.history)
            self.gantt_table.setColumnCount(second)
            for seconds in range(second):
                for student in range(student_count):
                # CPU가 쉬는 도중에는 할당될 프로세스가 없을 가능성 존재
                # 강제로 24시간을 잡기 떄문에 SPN / RR을 돌리고 반환하는 시간이 24시간보다 적을 가능성이 존재
                    if seconds + 1 < len(self.history[student]):
                        if self.history[student][seconds + 1][1][0]:
                            max_len_student = student
                            self.gantt_table.setItem(
                                student, seconds, QTableWidgetItem(self.history[student][seconds + 1][1][0].process_id)
                            )
                            self.gantt_table.item(student, seconds).setBackground(
                                QtGui.QColor(
                                self.history[student][seconds + 1][1][0].Color[0],
                                self.history[student][seconds + 1][1][0].Color[1],
                                self.history[student][seconds + 1][1][0].Color[2],
                            )
                        )
            self.gantt_table.scrollToItem(self.gantt_table.item(max_len_student, second - 1))
            fortext = "Real Time = " + str(second) + " hour"
            self.real_time_label.setText(fortext)


    def default_setting(self):
        # AT BT 범위 바꾼거 수정
        self.AT.setRange(0, 65535)
        self.AT_label.setText("AT")
        self.BT.setRange(1, 65535)
        self.CPU_label.setText("CPU")
        self.TQ.setRange(1, 65535)
        self.TQ_label.setText("Quantum")
        # Proc_Table 기본 세팅
        self.proc_table.setColumnCount(3)
        self.proc_table.setHorizontalHeaderLabels(["Process Name", "Arrival Time", "Burst Time"])
        header = self.proc_table.horizontalHeader()
        for column_idx in range(self.column_count):
            header.setSectionResizeMode(column_idx, QHeaderView.Stretch)
        # Gantt Table 기본 세팅
        self.set_CPU_slot()
        # Result_Table 기본 세팅
        self.result_table.setColumnCount(6)
        self.result_table.setHorizontalHeaderLabels(
            ["Process Name", "Arrival Time", "Burst Time", "Waiting Time", "Turnaround Time", "Normalized TT"]
        )
        self.result_table.verticalHeader().setVisible(False)
        header = self.result_table.horizontalHeader()
        self.result_table.horizontalHeader().setFixedHeight(25)
        for time_table_col in range(6):
            header.setSectionResizeMode(time_table_col, QHeaderView.Stretch)
        self.real_time_label.setText("Real Time = 0 sec")
        self.student_list.setDisabled(True)

    def YOSA_setting(self):
        # AT BT 범위 바꾼거 수정
        self.AT.setRange(1, 4)
        self.AT_label.setText("학점")
        self.BT.setRange(1, 24)
        self.CPU_label.setText("학생 수")
        self.TQ.setRange(1, 96)
        self.TQ_label.setText("팀프 시간")
        # Proc_Table 기본 세팅
        self.proc_table.setColumnCount(4)
        self.proc_table.setHorizontalHeaderLabels(["과목 이름", "학점", "소요 시간", "대상 인원"])
        header = self.proc_table.horizontalHeader()
        for column_idx in range(4):
            header.setSectionResizeMode(column_idx, QHeaderView.Stretch)
        # Gantt Table 기본 세팅
        # 이건 setCPU 여기서 바꿔야할듯
        self.set_CPU_slot()
        # Result_Table 기본 세팅
        self.result_table.setColumnCount(13)
        self.result_table.setHorizontalHeaderLabels(
            [
                "개인 공부\n투자 시간",
                "과목 1\n공부 시간",
                "과목 1\n학점",
                "과목 2\n공부 시간",
                "과목 2\n학점",
                "과목 3\n공부 시간",
                "과목 3\n학점",
                "과목 4\n공부 시간",
                "과목 4\n학점",
                "팀플\n투자 시간",
                "팀플 학점",
                "평균 학점",
                "팀 전체\n평균 학점",
            ]
        )
        self.result_table.horizontalHeader().setFixedHeight(45)
        # Result의 Vertical과 StudentList부분은 set_CPU_slot으로 넘김
        header = self.result_table.horizontalHeader()
        for time_table_col in range(13):
            header.setSectionResizeMode(time_table_col, QHeaderView.Stretch)
        self.real_time_label.setText("Real Time = 0 hour")

        self.student_list.setEnabled(True)
        self.TQ.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

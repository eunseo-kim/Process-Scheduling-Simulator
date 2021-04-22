from CPU import *
from collections import defaultdict


class Student(CPU):
    def __init__(self, student_name):  # student_name는 학생 이름, class_list는 학생이 듣는 수업
        super().__init__(student_name)
        self.subject_list = []
        self.best_solo_grades = [0 for _ in range(25)]
        self.total_credits = 3  # 총 학점 21 학점같은 - 기본 운영체제 팀플 3학점을 듣기 때문에

    def add_subject_list(self, subject):
        self.subject_list.append(subject)
        self.total_credits += subject.credit

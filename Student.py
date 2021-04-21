from CPU import *
from collections import defaultdict


class Student(CPU):
    def __init__(self, student_name):  # student_name는 학생 이름, class_list는 학생이 듣는 수업
        super().__init__(student_name)
        self.subject_list = []

    def add_subject_list(self, subject):
        self.subject_list.append(subject)

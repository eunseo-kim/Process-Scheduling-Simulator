from CPU import *
from collections import defaultdict
from itertools import product


class Student(CPU):
    def __init__(self, student_name):  # student_name는 학생 이름, class_list는 학생이 듣는 수업
        super().__init__(student_name)
        self.subject_list = []
        self.best_solo_avg_grades = [0 for _ in range(25)]
        self.best_solo_subject_study_cases = defaultdict(list)
        self.best_solo_subjects_grades = defaultdict(list)

        self.best_solo_total_study_time = 0 # 개인 공부 투자 시간
        self.best_solo_subject_study_case = [] # 각 과목 공부 투자시간 순서대로
        self.best_solo_subjects_grade = [] # 각 과목 학점 순서대로
        self.best_each_team_play_time = 0 # 개인의 팀플 투자시간
        self.best_team_play_grade = 0 # 개인
        self.best_avg_grade = 0

        self.total_credits = 3  # 총 학점 21 학점같은 - 기본 운영체제 팀플 3학점을 듣기 때문에

    def add_subject_list(self, subject):
        self.subject_list.append(subject)
        self.total_credits += subject.credit

    # max_solo_study_time 이걸로 best 시간 구하고 이걸로 구해도 똑같은 값이 나올거 같은데?
    def calculate_best_case(self, best_team_play_case):
        best_each_team_play_time = best_team_play_case[0][self.id]
        total_team_play_time = sum(best_team_play_case[0])
        max_solo_study_time = 24 - best_each_team_play_time
        self.best_solo_subject_study_case = self.best_solo_subject_study_cases[max_solo_study_time]
        self.best_solo_total_study_time = sum(self.best_solo_subject_study_case)
        self.best_solo_subjects_grade = self.best_solo_subjects_grades[max_solo_study_time]
        self.best_each_team_play_time = best_each_team_play_time
        self.best_team_play_grade = best_team_play_case[2]
        self.best_avg_grade = best_team_play_case[1][self.id]
        print("---------------------------")
        print("self.best_solo_subject_study_case", self.best_solo_subject_study_case)
        print("self.best_solo_total_study_time", self.best_solo_total_study_time)
        print("self.best_solo_subjects_grade", self.best_solo_subjects_grade)
        print("self.best_each_team_play_time", self.best_each_team_play_time)
        print("self.best_team_play_grade", self.best_team_play_grade)
        print("self.best_avg_grade", self.best_avg_grade)

    def get_team_play_grade(self, total_team_play_time, max_team_play_time):
        team_play_score = 100 * (total_team_play_time / max_team_play_time)
        team_play_grade = self.convert_score_to_grade(team_play_score)
        return team_play_grade

    def get_final_student_grade(self, each_solo_study_time, total_team_play_time, max_team_play_time ):
        team_play_grade = self.get_team_play_grade(total_team_play_time, max_team_play_time ) * 3  # 운영체제는 3학점임
        solo_study_grade = self.best_solo_avg_grades[each_solo_study_time] * (self.total_credits - 3)
        return (team_play_grade + solo_study_grade) / self.total_credits

    def set_best_solo_cases(self):
        all_study_cases = self.get_all_study_cases(self.subject_list)
        for study_time in range(25):
            # 모든 과목 공부시간(BT)을 다 합쳐도 시간이 남아서 현재 study_time에 대한 경우가 없을 때
            if study_time not in all_study_cases:
                # print("all_study_cases =", study_time)
                self.best_solo_avg_grades[study_time] = 4.5
                self.best_solo_subject_study_cases[study_time] = [subject.BT for subject in self.subject_list]
                self.best_solo_subjects_grades[study_time] = [4.5 for subject in self.subject_list]
                continue

            for study_case in all_study_cases[study_time]:
                # print("study_case", study_case)
                grade_list = []  # 받은 학점들의 합
                total_grade_sum = 0
                for subject_idx, subject_study_hour in enumerate(study_case):
                    score = subject_study_hour * self.subject_list[subject_idx].score_per_hour
                    grade = self.convert_score_to_grade(score)
                    grade_list.append(grade)
                    total_grade_sum += grade * self.subject_list[subject_idx].credit
                avg_grade = total_grade_sum / (self.total_credits - 3)
                if self.best_solo_avg_grades[study_time] <= avg_grade:
                    if self.best_solo_avg_grades[study_time] < avg_grade:
                        self.best_solo_avg_grades[study_time] = avg_grade
                        self.best_solo_subject_study_cases[study_time] = study_case[:]
                        # print()
                        self.best_solo_subjects_grades[study_time] = grade_list[:]
                        # print("study_case", study_case)
                        # print("grade_list", grade_list)
                    # self.best_solo_subject_study_cases[study_time].append(study_case[:])
                    # self.best_solo_subjects_grades[study_time].append(grade_list[:])

                    # print("self.best_solo_subject_study_cases[", study_time, "]", self.best_solo_subject_study_cases[study_time])

        # test
        # for study_time, best_solo_grade in enumerate(best_solo_avg_grades):
        #     print("best_solo_avg_grades", study_time, best_solo_grade)
        # print("best_solo_subjects_grades", study_time, self.best_solo_subjects_grades)
        # print("best_solo_subjects_grades", study_time, self.best_solo_subjects_grades)
        # for study_time in range(25):
        #     print("======================")
        #     print("best_solo_avg_grades", study_time, self.best_solo_avg_grades[study_time])
        #     print("best_solo_subject_study_case", study_time, self.best_solo_subject_study_cases[study_time])
        #     print("best_solo_subjects_grade", study_time, self.best_solo_subjects_grades[study_time])

    def get_all_study_cases(self, subject_list):
        all_study_cases = defaultdict(list)

        for study_subject_time_case in product(*[range(subject.BT + 1) for subject in subject_list]):
            study_time = sum(study_subject_time_case)
            if study_time <= 24:
                all_study_cases[study_time].append(study_subject_time_case)
        # print("all_study_cases", all_study_cases)
        return all_study_cases

    def convert_score_to_grade(self, score):
        if score >= 95:
            return 4.5
        elif score >= 90:
            return 4.0
        elif score >= 85:
            return 3.5
        elif score >= 80:
            return 3.0
        elif score >= 75:
            return 2.5
        elif score >= 70:
            return 2.0
        elif score >= 65:
            return 1.5
        elif score >= 60:
            return 1.0
        else:
            return 0

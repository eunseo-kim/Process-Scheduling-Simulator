from collections import defaultdict
from itertools import product
import copy
from subject import Subject
from cpu import CPU


class Student(CPU):
    def __init__(self, student_name):  # student_name는 학생 이름, class_list는 학생이 듣는 수업
        super().__init__(student_name)
        self.subject_list = []
        # 0~ 24 시간에서 각 시간에따른 --------------------
        # 이 학생의 최고 평균 학점
        self.best_solo_avg_grades = [-1 for _ in range(25)]
        # 이 학생의 최고의 각 과목별 공부 투자 시간
        self.best_solo_subject_study_cases = defaultdict(list)
        # 이 학생의 최고의 각 과목별 학점
        self.best_solo_subjects_grades = defaultdict(list)
        # -------------------------------------------------

        # 최종적으로 제일 좋은 -------------------------------------
        self.best_solo_total_study_time = 0  # 개인 공부 투자 시간
        self.best_solo_subject_study_case = []  # 각 과목 공부별 투자시간 순서대로
        self.best_solo_subjects_grade = []  # 각 과목별 학점 순서대로
        self.best_each_team_play_time = 0  # 개인의 팀플 투자시간
        self.best_team_play_grade = 0  # 팀플 학점
        self.best_avg_grade = 0  # 최종적인 개인 학점(개인 공부 학점과 팀플 학점의 평균)
        # ------------------------------------------------------------
        self.total_credits = 3  # 총 학점 21 학점같은 - 기본 운영체제 팀플 3학점을 듣기 때문에

    def add_subject_list(self, subject):
        """
        학생에게 과목을 추가하면서, 총학점도 같이 구함
        """
        self.subject_list.append(subject)
        self.total_credits += subject.credit

    # max_solo_study_time 이걸로 best 시간 구하고 이걸로 구해도 똑같은 값이 나올거 같은데?
    def calculate_best_case(self, best_team_play_case, max_team_play_time):
        """
        최종적으로 구한 best_team_play_case와 처음에 설정해준 목표 팀플 실행 시간을 통해서
        학생의 최종적인 각 과목의 실제 공부 시간, 총 공부 시간,각 과목들의 학점,
        이 학생이 투자한 팀플 시간, 이 팀의 팀플 학점
        이 학생의 최종 평균 학점을
        계산하여 설정한다.
        """
        best_each_team_play_time = best_team_play_case[0][self.id]
        total_team_play_time = sum(best_team_play_case[0])
        max_solo_study_time = 24 - best_each_team_play_time
        self.best_solo_subject_study_case = self.best_solo_subject_study_cases[max_solo_study_time]
        self.best_solo_total_study_time = sum(self.best_solo_subject_study_case)
        self.best_solo_subjects_grade = self.best_solo_subjects_grades[max_solo_study_time]
        self.best_each_team_play_time = best_each_team_play_time
        self.best_team_play_grade = self.get_team_play_grade(total_team_play_time, max_team_play_time)
        self.best_avg_grade = best_team_play_case[1][self.id]
        print("---------------------------")
        print("self.best_solo_subject_study_case", self.best_solo_subject_study_case)
        print("self.best_solo_total_study_time", self.best_solo_total_study_time)
        print("self.best_solo_subjects_grade", self.best_solo_subjects_grade)
        print("self.best_each_team_play_time", self.best_each_team_play_time)
        print("self.best_team_play_grade", self.best_team_play_grade)
        print("self.best_avg_grade", self.best_avg_grade)

    def get_team_play_grade(self, total_team_play_time, max_team_play_time):
        """
        팀플 학점을 구한다(팀 전체가 투자한 총 팀플시간과 목표 팀플시간을 통해서)
        """
        team_play_score = 100 * (total_team_play_time / max_team_play_time)
        team_play_grade = self.convert_score_to_grade(team_play_score)
        return team_play_grade

    def get_final_student_grade(self, each_solo_study_time, total_team_play_time, max_team_play_time):
        """
        개인 공부시간에 따른 학점, 팀플에서 받은 학점의 평균을 통해 개인 최종 평균 학점을 구한다.
        개인 공부 학점 - 개인 공부시간(each_solo_study_time)에 따라서 구함
        팀플 학점 - 팀 전체가 투자한 팀플레이 시간, 목표 팀플레이시간을 통해 구함
        """
        team_play_grade = self.get_team_play_grade(total_team_play_time, max_team_play_time) * 3  # 운영체제는 3학점임
        solo_study_grade = self.best_solo_avg_grades[each_solo_study_time] * (self.total_credits - 3)
        return (team_play_grade + solo_study_grade) / self.total_credits

    def set_best_solo_cases(self):
        """
        공부시간에 따른
        이 학생의 최고 평균 학점
        이 학생의 최고의 각 과목별 공부 투자 시간
        이 학생의 최고의 각 과목별 학점
        을 구하는 함수이다.
        """
        all_study_cases = self.get_all_study_cases()
        if len(all_study_cases) > 1:  # 과목을 아무것도 할당받지 못하면 all_study_cases =
            for study_time in range(25):
                # 모든 과목 공부시간(BT)을 다 합쳐도 시간이 남아서 현재 study_time에 대한 경우가 없을 때
                # ex) 알고리즘 7시간, 컴구조 4시간 일때 최대 공부시간은 11시간이다.
                # 12, 13 ...시간인 경우는 존재하지 않는다.
                # 이때 개인 평균 학점을 4.5로 설정해주고
                # 각 과목의 공부 투자시간을 목표 시간과 똑같이 설정해준다.(다 공부할 수 있으므로)
                # 그리고 각 과목별 학점 4.5이다.
                if study_time not in all_study_cases:
                    # print("all_study_cases =", study_time)
                    self.best_solo_avg_grades[study_time] = 4.5
                    self.best_solo_subject_study_cases[study_time] = [subject.bt for subject in self.subject_list]
                    self.best_solo_subjects_grades[study_time] = [4.5 for subject in self.subject_list]
                    continue
                # 각 공부시간에 따른 과목별 투자 시간의 경우의 수를 돌면서
                #  ex) 알고리즘 7시간, 컴구조 4시간 일때
                # study_case는 (0, 0), (3,2), (7,4) 등이 되는데
                # 이때의 각 과목별 투자시간에 따른 점수와 학점 및 평균 학점을 구한다.
                # 경우의 수를 돌면서 구한 평균학점이 높으면 갱신해주어서
                # 제일 높은 평균 학점을 받았을 때의 평균 학점, 과목별 투자시간, 과목별 학점을 저장한다.
                for study_case in all_study_cases[study_time]:
                    grade_list = []
                    total_grade_sum = 0
                    for subject_idx, subject_study_hour in enumerate(study_case):
                        score = subject_study_hour * self.subject_list[subject_idx].score_per_hour
                        grade = self.convert_score_to_grade(score)
                        grade_list.append(grade)
                        total_grade_sum += grade * self.subject_list[subject_idx].credit
                    avg_grade = total_grade_sum / (self.total_credits - 3)
                    if self.best_solo_avg_grades[study_time] < avg_grade:
                        self.best_solo_avg_grades[study_time] = avg_grade
                        self.best_solo_subject_study_cases[study_time] = study_case[:]
                        self.best_solo_subjects_grades[study_time] = grade_list[:]

    def get_all_study_cases(self):
        """
        중복 순열을 통해서 0 ~ 24시간까지의 모든 과목별 공부 투자 경우의 수를 구함
        """
        all_study_cases = defaultdict(list)

        for study_subject_time_case in product(*[range(subject.bt + 1) for subject in self.subject_list]):
            study_time = sum(study_subject_time_case)
            if study_time <= 24:
                all_study_cases[study_time].append(study_subject_time_case)
        return all_study_cases

    def make_student_real_subject_list(self):
        """
        학생에게 주어진 과목의 실제 공부 시간을 계산하는 함수

        :desc
            학생 A - 알고리즘 7시간, 컴구조 4시간
            self.best_solo_subject_study_case는 학생이 best 학점을 받기 위해 주어진 과목을 공부하는 시간의 경우이다.
            ex) [7, 4] or [0, 2](시간이 부족해서 컴구조 2시간 공부가 최선인 경우) 등
            여기서 [0, 2] 인 경우는 주어진 과목 공부 7, 4시간이지만 실제 공부시간은 0,2시간이다.
            실제 공부시간으로 스케줄링을 돌리기 위해서 주어진 과목들을 각각 복사하며
            주어진 공부시간(bt, remain_bt)를 실제 최적 공부시간(best_subject_study_time)으로 변환해서
            real_subject_list로 만들어준다.
        """
        real_subject_list = []
        for idx, best_subject_study_time in enumerate(self.best_solo_subject_study_case):
            if best_subject_study_time > 0:
                real_subject = copy.deepcopy(self.subject_list[idx])
                real_subject.bt = best_subject_study_time
                real_subject.remain_bt = best_subject_study_time
                real_subject_list.append(real_subject)
        if self.best_each_team_play_time > 0:
            real_subject_list.append(
                Subject("팀프", 3, self.best_each_team_play_time, 14, -1),
            )
        return real_subject_list

    def convert_score_to_grade(self, score):
        grade = 0
        if score >= 95:
            grade = 4.5
        elif score >= 90:
            grade = 4.0
        elif score >= 85:
            grade = 3.5
        elif score >= 80:
            grade = 3.0
        elif score >= 75:
            grade = 2.5
        elif score >= 70:
            grade = 2.0
        elif score >= 65:
            grade = 1.5
        elif score >= 60:
            grade = 1.0
        return grade

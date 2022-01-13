import random
from itertools import product
from numpy import std
from scheduler import Scheduler
from student import Student
from spn import SPN
from rr import RR


class YOSA(Scheduler):
    def __init__(self, subject_input_list, student_count, max_team_play_time):
        super().__init__(subject_input_list, student_count)
        self.student_count = student_count
        self.students = self.create_students()
        self.subjects = subject_input_list
        self.max_team_play_time = max_team_play_time
        self.team_avg_grade = 0
        self.each_student_history_list = []
        self.allocate_subject_to_student()

    def create_students(self):
        return [Student(idx) for idx in range(self.student_count)]

    def allocate_subject_to_student(self):
        # 과목 리스트를 돌면서
        for subject in self.subjects:
            # 그 과목을 할당받은 학생을 찾으면 할당해줌
            for student in self.students:
                if subject.student_id == student.id:
                    student.add_subject_list(subject)
                    break

    def run(self):
        """
        best_team_play_case_list의 한 case에는
        [0] 최적의 팀플 공부시간 ex)[7,4] (0번 학생 7시간, 1번 학생 4시간)
        [1] 이때의 각 학생의 학점 ex) [4.0, 3.5]
        [2] 이때의 팀 최종 평균
        """
        best_team_play_case = self.find_best_team_play_case()
        self.team_avg_grade = best_team_play_case[2]
        print("team_avg = ", self.team_avg_grade)
        for student in self.students:
            # 1.학생의 best인 경우 정보를 설정해줌
            student.calculate_best_case(best_team_play_case, self.max_team_play_time)
            # 현재 나온 학생들을 기준으로 각각 1개짜리로 돌려서
            # history를 모은 each_student_history_list를 만들어서 돌린다.
            # 2. 학생의 실제 공부 시간 계산
            student_real_subject_list = student.make_student_real_subject_list()
            # 3. 이 정보를 가지고 스케줄링을 돌림
            if random.choice([True, False]):
                scheduler = SPN(student_real_subject_list, 1)
            else:
                scheduler = RR(student_real_subject_list, 1, random.randrange(1, 4))
            scheduler.run()
            # 학생이 4명이면 4개의 히스토리를 저장함
            self.each_student_history_list.append(scheduler.history)

    def find_best_team_play_case(self):
        """
        1. 각 학생들의 각 개인 공부시간에 따른
        best_case(평균 학점, 과목별 투자시간, 과목별 학점)를 구해서 각 학생들에게 저장해놓는다.
        2. 각 학생들의 모든 팀플 투자 하는 경우의 수를 구한다.
        3. 팀플 투자 경우의 수에 따른
           각 학생의 팀플 투자시간과 따른 개인공부시간(24 - each_team_play_time)을 통해서
           최종 학점을 구한다.
        4. 각 학생의 최종 학점을 통해 팀 전체의 평균 학점을 구한다.
        5. 기존에 구한 최고 평균학점과 비교하며 팀 전체의 평균 학점이 제일 높은 경우들을 찾는다
        6. 팀 전체의 평균 학점이 제일 높은 경우중에
           팀원들의 팀플 투자시간이 합이 제일 적고 표준편차가 제일 작은 경우를 구해서
           최종적으로 반환해준다.
        """
        # @<1> 각 학생들의 각 개인 공부시간에 따른
        # best_case(평균 학점, 과목별 투자시간, 과목별 학점)를 구한다.
        for student in self.students:
            student.set_best_solo_cases()
            # print(student.best_solo_avg_grades)

        best_average_team_grade = 0
        best_team_play_case_list = []
        # final_grade = []
        # team_play_time_case = ex) [0,0,0,0] or [0,4,5,7] or [24,24,24,24]
        # [1, 7, 2, 4] 팀플에 학생1은 1시간, 학생2는 7시간, 학생3는 2시간, 학생4는 4시간 투자
        # @<2>각 학생들의 모든 팀플 투자 하는 경우의 수를 구한다.
        for team_play_time_case in product(*[range(25) for each_student_case in range(self.student_count)]):
            # 목표 팀플시간이 20시간인데 40시간을 투자할 수는 없다.
            if sum(team_play_time_case) <= self.max_team_play_time:
                final_student_grade_list = []
                final_average_team_grade = 0

                # @<3>각 학생의 팀플 투자시간과 따른 개인공부시간(24 - each_team_play_time)을 통해서
                # 최종 학점을 구한다.
                for student_idx, each_team_play_time in enumerate(team_play_time_case):
                    final_student_grade_list.append(
                        self.students[student_idx].get_final_student_grade(
                            24 - each_team_play_time, sum(team_play_time_case), self.max_team_play_time
                        )
                    )
                # final_grade.append(final_student_grade_list)
                # @<4> 각 학생의 최종 학점을 통해 팀 전체의 평균 학점을 구한다.
                final_average_team_grade = sum(final_student_grade_list) / len(final_student_grade_list)
                # @<5>팀 전체의 평균 학점이 제일 높은 경우들을 찾는다
                if final_average_team_grade >= best_average_team_grade:
                    if final_average_team_grade > best_average_team_grade:
                        best_average_team_grade = final_average_team_grade
                        best_team_play_case_list = []
                    """
                    best_team_play_case_list의 한 case에는
                    [0] 최적의 팀플 공부시간 ex)[7,4] (0번 학생 7시간, 1번 학생 4시간)
                    [1] 이때의 각 학생의 학점 ex) [4.0, 3.5]
                    [2] 이때의 팀 최종 평균
                    """
                    best_team_play_case_list.append(
                        (team_play_time_case[:], final_student_grade_list[:], final_average_team_grade)
                    )
        print("==========================================================================")
        print("MAX_TEAM_PLAY_TIME", self.max_team_play_time)
        print("best_team_play_case_list", best_team_play_case_list)
        # @ <6>팀 전체의 평균 학점이 제일 높은 경우중에
        # 팀원들의 팀플 투자시간이 합이 제일 적고 표준편차가 제일 작은 경우를 구해서
        # 최종적으로 반환해준다.
        best_team_play_case = sorted(best_team_play_case_list, key=lambda x: (sum(x[0]), std(x[0])))[0]
        print("best_team_play_case", best_team_play_case)

        return best_team_play_case

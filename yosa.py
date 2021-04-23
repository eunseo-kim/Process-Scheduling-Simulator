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

    def find_best_team_play_case(self):
        for student in self.students:
            student.set_best_solo_cases()
            # print(student.best_solo_avg_grades)

        best_average_team_grade = 0
        best_team_play_case_list = []
        # final_grade = []
        # team_play_time_case = ex) [0,0,0,0] or [0,4,5,7] or [24,24,24,24]
        # [1, 7, 2, 4] 팀플에 학생1은 1시간, 학생2는 7시간, 학생3는 2시간, 학생4는 4시간 투자
        for team_play_time_case in product(*[range(25) for each_student_case in range(self.student_count)]):
            if sum(team_play_time_case) <= self.max_team_play_time:
                final_student_grade_list = []
                final_average_team_grade = 0

                for student_idx, each_team_play_time in enumerate(team_play_time_case):
                    final_student_grade_list.append(
                        self.students[student_idx].get_final_student_grade(
                            24 - each_team_play_time, sum(team_play_time_case), self.max_team_play_time
                        )
                    )
                # final_grade.append(final_student_grade_list)
                final_average_team_grade = sum(final_student_grade_list) / len(final_student_grade_list)
                # 이거 원래 > 이렇게 되어야 함
                if final_average_team_grade >= best_average_team_grade:
                    if final_average_team_grade > best_average_team_grade:
                        best_average_team_grade = final_average_team_grade
                        best_team_play_case_list = []
                    best_team_play_case_list.append(
                        (team_play_time_case[:], final_student_grade_list[:], final_average_team_grade)
                    )
        # print("final_grade by 1", sorted(final_grade, key=lambda x: x[0], reverse=True)[:20])
        # print("final_grade by 2", sorted(final_grade, key=lambda x: x[1], reverse=True)[:20])
        # print("best_average_team_grade", best_average_team_grade)
        # print("best_team_play_case_grade_list", best_team_play_case_grade_list)
        print("==========================================================================")
        print("MAX_TEAM_PLAY_TIME", self.max_team_play_time)
        print("best_team_play_case_list", best_team_play_case_list)
        # best는 합이 제일 적고 표준편차가 제일 작은 경우
        best_team_play_case = sorted(best_team_play_case_list, key=lambda x: (sum(x[0]), std(x[0])))[0]
        print("best_team_play_case", best_team_play_case)

        return best_team_play_case

    def create_students(self):
        return [Student(idx) for idx in range(self.student_count)]

    # best_team_play_case 의 학생들의 평균 학점하고, 팀 전체 평균 학점이 같은지 확인
    def run(self):
        best_team_play_case = self.find_best_team_play_case()
        self.team_avg_grade = best_team_play_case[2]
        print("team_avg = ", self.team_avg_grade)
        for student in self.students:
            student.calculate_best_case(best_team_play_case, self.max_team_play_time)
            # 현재 나온 학생들을 기준으로 각각 1개짜리로 돌려서
            # history를 모은 each_student_history_list를 만들어서 돌린다.
            student_real_subject_list = student.make_student_real_subject_list()
            if random.choice([True, False]):
                scheduler = SPN(student_real_subject_list, 1)
            else:
                scheduler = RR(student_real_subject_list, 1, random.randrange(1, 4))
            scheduler.run()
            self.each_student_history_list.append(scheduler.history)

    def allocate_subject_to_student(self):
        # 과목 리스트를 돌면서
        for subject in self.subjects:
            # 그 과목을 할당받은 학생을 찾으면 할당해줌
            for student in self.students:
                if subject.student_id == student.id:
                    student.add_subject_list(subject)
                    break

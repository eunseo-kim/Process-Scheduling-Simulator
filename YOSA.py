from Scheduler import *
from itertools import combinations_with_replacement
from itertools import permutations
from itertools import product
from Student import *
from Subject import *
from numpy import std

# 24^(학생수)의 행렬을 만들고 최적값을 찾는
# 미리 예외처리를 통해 가지치기?
# get_best_grade 함수 사용
# find_best_team_play_case => 최적 찾는 경우
# calculate_grade => 계산해서 값 할당해주는 함수
# [GUI]
# gui에 어떻게 뿌려줄지 생각
# => 그냥 내가 best_case 찾고 그에 따라서 학생들한테 값을 배정해주면 gui에서 학생들 순회하면서 값 출력
# 학생들한테 배정할 값 - 베스트 개인 공부시간/ 팀플시간, 이에 따른 각 과목 학점 및 최종 학점, 학생 전체의 평균 학점
# [Student] = CPU
# best_solo_avg_grades = 미리 0으로 25개 초기화

# TODO. 팀플시간 1일때 왜 전부 4.5가 안 나오는지
# TODO. 일단 개인 과목 1과목씩 받아서 하기ㅠ
class YOSA(Scheduler):
    # TODO 직접 객체 리스트를 넣어줄지, 숫자(입력값)를 넣어줄지 고민
    def __init__(self, subject_input_list, student_count, max_team_play_time):
        super().__init__(subject_input_list, student_count)
        self.students = self.create_students(student_count)
        self.subjects = subject_input_list
        self.max_team_play_time = max_team_play_time
        self.team_avg_grade = 0
        self.allocate_subject_to_student()

    # TODO team_play_case로 할지 best_team_play_case로 할지
    # TODO best_team_play_case 묶어서
    def find_best_team_play_case(self):
        for student in self.students:
            student.set_best_solo_cases()
            # print(student.best_solo_avg_grades)

        best_average_team_grade = 0
        best_team_play_case_list = []
        # final_grade = []
        # team_play_time_case = ex) [0,0,0,0] or [0,4,5,7] or [24,24,24,24]
        # [1, 7, 2, 4] 팀플에 학생1은 1시간, 학생2는 7시간, 학생3는 2시간, 학생4는 4시간 투자
        for team_play_time_case in product(*[range(25) for each_student_case in range(len(self.students))]):
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

    def create_students(self, student_count):
        return [Student(idx) for idx in range(student_count)]

    # best_team_play_case 의 학생들의 평균 학점하고, 팀 전체 평균 학점이 같은지 확인
    def run(self):
        best_team_play_case = self.find_best_team_play_case()
        self.team_avg_grade = best_team_play_case[2]
        print("team_avg = ", self.team_avg_grade)
        for student in self.students:
            student.calculate_best_case(best_team_play_case)

    def allocate_subject_to_student(self):
        # 과목 리스트를 돌면서
        for subject in self.subjects:
            # 그 과목을 할당받은 학생을 찾으면 할당해줌
            for student in self.students:
                if subject.student_id == student.id:
                    student.add_subject_list(subject)
                    break

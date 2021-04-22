from Scheduler import *
from itertools import combinations_with_replacement
from itertools import permutations
from itertools import product
from Student import *
from Subject import *

# 24^(학생수)의 행렬을 만들고 최적값을 찾는
# 미리 예외처리를 통해 가지치기?
# get_best_grade 함수 사용
# find_best_cram_case => 최적 찾는 경우
# calculate_grade => 계산해서 값 할당해주는 함수
# [GUI]
# gui에 어떻게 뿌려줄지 생각
# => 그냥 내가 best_case 찾고 그에 따라서 학생들한테 값을 배정해주면 gui에서 학생들 순회하면서 값 출력
# 학생들한테 배정할 값 - 베스트 개인 공부시간/ 팀플시간, 이에 따른 각 과목 학점 및 최종 학점, 학생 전체의 평균 학점
# [Student] = CPU
# best_solo_grades = 미리 0으로 25개 초기화

# TODO. 팀플시간 1일때 왜 전부 4.5가 안 나오는지
# TODO. 일단 개인 과목 1과목씩 받아서 하기ㅠ
class YOSA(Scheduler):
    # TODO 직접 객체 리스트를 넣어줄지, 숫자(입력값)를 넣어줄지 고민
    def __init__(self, subject_input_list, student_count):
        super().__init__(subject_input_list, student_count)
        self.students = self.create_students(student_count)
        self.subjects = subject_input_list
        self.allocate_subject_to_student()

    def find_best_cram_case(self, total_team_play_time):
        for student in self.students:
            student.best_solo_grades = self.get_best_solo_grades(student)
            # print(student.best_solo_grades)

        best_average_team_grade = 0
        best_cram_case = []
        best_cram_case_grade_list = []
        best_cram_case_list = []
        # team_play_time_case = ex) [0,0,0,0] or [0,4,5,7] or [24,24,24,24]
        # [1, 7, 2, 4] 팀플에 학생1은 1시간, 학생2는 7시간, 학생3는 2시간, 학생4는 4시간 투자
        for team_play_time_case in product(*[range(25) for each_student_case in range(len(self.students))]):
            if sum(team_play_time_case) <= total_team_play_time:
                final_student_grade_list = []
                final_average_team_grade = 0

                for student_idx, each_team_play_time in enumerate(team_play_time_case):
                    final_student_grade_list.append(
                        self.get_final_student_grade(
                            self.students[student_idx],
                            24 - each_team_play_time,
                            sum(team_play_time_case),
                            total_team_play_time,
                        )
                    )
                final_average_team_grade = sum(final_student_grade_list) / len(final_student_grade_list)
                # 이거 원래 > 이렇게 되어야 함
                if final_average_team_grade >= best_average_team_grade:
                    if final_average_team_grade > best_average_team_grade:
                        best_average_team_grade = final_average_team_grade
                        best_cram_case_grade_list = []
                        best_cram_case_list = []
                        best_cram_case_grade_list.append(final_student_grade_list[:])
                    best_cram_case_list.append(team_play_time_case[:])

        print("best_average_team_grade", best_average_team_grade)
        print("best_cram_case_grade_list", best_cram_case_grade_list)
        print("best_cram_case_list", best_cram_case_list)

        return best_cram_case

    def get_final_student_grade(self, student, each_solo_study_time, team_play_time, total_team_play_time):
        team_play_score = 100 * (team_play_time / total_team_play_time)
        team_play_grade = self.convert_score_to_grade(team_play_score) * 3  # 운영체제는 3학점임
        # print("team_play_grade", team_play_grade)
        solo_study_grade = student.best_solo_grades[each_solo_study_time] * (student.total_credits - 3)

        return (team_play_grade + solo_study_grade) / student.total_credits

    def create_students(self, student_count):
        return [Student(idx) for idx in range(student_count)]

    def run(self):
        for i in range(1, 73):
            print("[{0}]==========================".format(i))
            print(self.find_best_cram_case(i))
        # print(self.find_best_cram_case(55))

    def allocate_subject_to_student(self):
        # 과목 리스트를 돌면서
        for subject in self.subjects:
            # 그 과목을 할당받은 학생을 찾으면 할당해줌
            for student in self.students:
                if subject.student_id == student.cpu_id:
                    student.add_subject_list(subject)
                    break

    def get_best_solo_grades(self, student):
        all_study_cases = self.get_all_study_cases(student.subject_list)
        best_solo_grades = [0 for _ in range(25)]
        for study_time in range(25):
            best_solo_grades[study_time] = self.get_best_grade(student, study_time, all_study_cases)
        # test
        # for study_time, best_solo_grade in enumerate(best_solo_grades):
        #     print("best_solo_grades", study_time, best_solo_grade)
        return best_solo_grades

    def get_best_grade(self, student, study_time, all_study_cases):  # study_time: 학생 1명에게 할당된 개인 공부 시간
        # 모든 과목 공부시간(BT)을 다 합쳐도 시간이 남아서 현재 study_time에 대한 경우가 없을 때
        if study_time not in all_study_cases:
            return 4.5

        best_grade = 0
        for study_case in all_study_cases[study_time]:
            grade_sum = 0  # 받은 학점들의 합
            for subject_idx, subject_study_hour in enumerate(study_case):
                score = subject_study_hour * student.subject_list[subject_idx].score_per_hour
                grade = self.convert_score_to_grade(score) * student.subject_list[subject_idx].credit
                grade_sum += grade
            average_grade = grade_sum / (student.total_credits - 3)
            best_grade = max(best_grade, average_grade)

        return best_grade

    # ======================================================
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

    def get_all_study_cases(self, subject_list):
        all_study_cases = defaultdict(list)

        for study_subject_time_case in product(*[range(subject.BT + 1) for subject in subject_list]):
            study_time = sum(study_subject_time_case)
            if study_time <= 24:
                all_study_cases[study_time].append(study_subject_time_case)
        # print("all_study_cases", all_study_cases)
        return all_study_cases

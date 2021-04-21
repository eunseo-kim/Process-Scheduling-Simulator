from Scheduler import *
from itertools import combinations_with_replacement
from itertools import permutations
from Student import *
from Subject import *


class YOSA(Scheduler):
    def __init__(self, subject_input_list, student_count):
        super().__init__(subject_input_list, student_count)
        self.students = self.create_students(student_count)
        self.subjects = subject_input_list
        self.allocate_subject_to_student()

    # def create_subjects(self, subject_input_list):
    #     subject_list = []
    #     for idx, s in enumerate(subject_input_list):
    #         new_subject = Subject(s[0], s[1], s[2], idx)
    #         subject_list.append(new_subject)
    #     return subject_list

    def create_students(self, student_count):
        student_list = []
        for i in range(student_count):
            student_list.append(Student(i))
        return student_list

    def run(self):
        for s in self.students[0].subject_list:
            print(s.process_id)
        # print(self.students[0].subject_list)
        for i in range(0, 20):
            print("[study_time -", i, "]")
            print("best_grade", self.get_best_grade(self.students[0], i))

    def allocate_subject_to_student(self):
        # 과목 리스트를 돌면서
        for subject in self.subjects:
            # 그 과목을 할당받은 학생을 찾으면 할당해줌
            for student in self.students:
                if subject.student_id == student.cpu_id:
                    student.add_subject_list(subject)
                    break

    # A 학생, 10시간들어오면
    def get_best_grade(self, student, study_time):  # study_time: 학생 1명에게 할당된 개인 공부 시간
        # 모든 과목 공부시간(BT)을 다 합쳐도 study_time이 남을 때
        if self.is_enough_time_to_study(student, study_time):
            return 4.5

        best_grade = 0
        all_study_cases = self.get_all_study_cases(student.subject_list, study_time)
        for study_case in all_study_cases:
            # print("study_case", study_case)
            grade_sum = 0  # 받은 학점들의 합
            all_grade = 0  # 1학점, 2학점의 grade
            for subject_idx, subject_study_hour in enumerate(study_case):
                score = subject_study_hour * self.subjects[subject_idx].score_per_hour
                grade = self.convert_score_to_grade(score) * self.subjects[subject_idx].grade
                grade_sum += grade
                all_grade += self.subjects[subject_idx].grade
            average_grade = grade_sum / all_grade
            best_grade = max(best_grade, average_grade)

        # grade 비교, 누가 더 작은지
        return best_grade

    def is_enough_time_to_study(self, student, study_time):
        # 모든 과목 공부시간(BT)을 다 합쳐도 study_time이 남을 때
        study_time_sum = 0
        for subject in student.subject_list:
            study_time_sum += subject.BT
        if study_time_sum <= study_time:
            return True
        return False

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

    def get_all_study_cases(self, subject_list, study_time):
        max_bt_subject = max(subject_list, key=lambda x: x.BT)
        # print("max_bt_subject", max_bt_subject.BT)
        num_list = [x for x in range(0, max_bt_subject.BT + 1)]
        result = []
        for arr in combinations_with_replacement(num_list, len(subject_list)):  # (0, 0, 0, 24)
            if sum(arr) == study_time:
                for each_case in permutations(arr, len(subject_list)):  # (24, 0, 0, 0), (0, 24, 0, 0), (0, 0, 24, 0)...
                    if each_case not in result:
                        can_append = True
                        for subject_idx, subject in enumerate(
                            subject_list
                        ):  # 모든 과목 BT가 8시간이라고 가정(8시간보다 더 많이 공부할 수는 없음)
                            if each_case[subject_idx] > subject.BT:
                                can_append = False
                                break
                        if can_append:
                            result.append(each_case)
        return result


# 결과
# for each_case in result:
#     print(each_case)

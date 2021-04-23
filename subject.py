from process import Process


class Subject(Process):
    def __init__(self, id, credit, bt, color_idx, student_id):
        super().__init__(id, 0, bt, color_idx)
        self.student_id = student_id
        self.credit = credit
        if bt > 0:
            self.score_per_hour = 100 / bt

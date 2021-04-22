import random
from Process import *


class Subject(Process):
    def __init__(self, process_id, credit, BT, color_idx, student_id):
        super().__init__(process_id, 0, BT, color_idx)
        self.student_id = student_id
        self.credit = credit
        self.score_per_hour = 100 / BT

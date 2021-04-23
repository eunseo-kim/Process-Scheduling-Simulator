class CPU:
    def __init__(self, id):
        self.id = id
        self.process = None
        self.work_time = 0

    def is_idle(self):
        return self.process is None

    def set_idle(self):
        self.process = None
        self.work_time = 0

    def set_process(self, process):
        self.process = process

    def is_finished(self, quantum=-1):
        if not self.is_idle():
            if self.process.remain_bt == 0:
                return True
            if self.work_time == quantum:
                return True
        return False

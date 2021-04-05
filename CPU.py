class CPU:
    def __init__(self, cpu_id):
        self.cpu_id = cpu_id
        self.process = None
        self.end_time = -1

    def is_idle(self):
        return self.process is None

    def set_idle(self):
        self.process = None

    def set_process(self, process, cur_time, end_time):
        self.process = process
        self.end_time = end_time
        self.process.remain_BT -= end_time - cur_time

    def is_finished(self, cur_time):
        if cur_time == self.end_time:
            return True
        return False

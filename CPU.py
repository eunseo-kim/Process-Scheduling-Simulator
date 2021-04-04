class CPU:
    def __init__(self, cpu_id):
        self.cpu_id = cpu_id
        self.process = None

    def is_idle(self):
        return self.process is None



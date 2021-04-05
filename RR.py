from Scheduler import *



class RR(Scheduler):
    def __init__(self, process_input_list, cpu_count, quantum):
        super().__init__(process_input_list, cpu_count)
        self.quantum = quantum


    def run(self):
        pass

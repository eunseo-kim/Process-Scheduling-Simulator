from abc import *
from Process import *
from CPU import *


class Scheduler(metaclass=ABCMeta):
    def __init__(self, process_input_list, cpu_count):
        self.process_count = len(process_input_list)
        self.process = self.create_processes(self.process_count, process_input_list)
        self.cpu_count = cpu_count
        self.cpu = self.create_cpu(self.cpu_count)
        self.ready_queue = []

    def create_process(self, process_input_list):
        process_list = []
        for i, p in enumerate(process_input_list):
            process[i].append(Process(p[0], p[1], p[2]))
        return process_list

    def create_cpu(self, cpu_count):
        cpu_list = []
        for i in range(cpu_count):
            cpu_list.append(CPU(i + 1))
        return cpu_list

    @abstractmethod
    def run(self):
        pass
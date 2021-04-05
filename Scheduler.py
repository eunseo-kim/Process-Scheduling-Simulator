from abc import *
from Process import *
from CPU import *


class Scheduler(metaclass=ABCMeta):
    def __init__(self, process_input_list, cpu_count):
        self.process_count = len(process_input_list)
        self.processes = self.create_processes(process_input_list)
        self.cpu_count = cpu_count
        self.cpus = self.create_cpus(self.cpu_count)
        self.ready_queue = []

    def create_processes(self, process_input_list):
        process_list = []
        for p in process_input_list:
            process_list.append(Process(p[0], p[1], p[2]))
        return process_list

    def create_cpus(self, cpu_count):
        cpu_list = []
        for i in range(cpu_count):
            cpu_list.append(CPU(i + 1))
        return cpu_list

    @abstractmethod
    def run(self):
        pass

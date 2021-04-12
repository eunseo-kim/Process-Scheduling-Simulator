from abc import *
from Process import *
from CPU import *


class Scheduler(metaclass=ABCMeta):
    def __init__(self, process_input_list, cpu_count):
        self.process_count = len(process_input_list)
        self.processes = process_input_list
        self.cpu_count = cpu_count
        self.cpus = self.create_cpus(self.cpu_count)
        self.ready_queue = []
        # 각 초마다
        # 레디큐에 어떤 프로세스들이 들어있는지(remain_BT)
        # 각 CPU에 프로세스가 존재하는지
        # 0초 => [[P1,P2],[P3, None, P4, None]]
        # history = [[P1,P2],[P3, None]], [[P2],[P3, None], ...]
        self.history = []

    def record_history(self, ready_queue, cpus, processes):
        record = []
        record.append(ready_queue)
        record.append([cpu.process for cpu in cpus])
        record.append(processes)
        self.history.append(record)

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

    def work(self):
        for cpu in self.cpus:
            if not cpu.is_idle():
                cpu.process.remain_BT -= 1
                cpu.work_time += 1

    @abstractmethod
    def run(self):
        pass

from abc import ABCMeta, abstractmethod
from cpu import CPU


class Scheduler(metaclass=ABCMeta):
    def __init__(self, process_input_list, cpu_count):
        self.process_count = len(process_input_list)
        self.processes = process_input_list
        self.cpu_count = cpu_count
        self.cpus = self.create_cpus()
        self.ready_queue = []
        self.history = []

    def record_history(self, ready_queue, cpus, processes):
        record = []
        record.append(ready_queue)
        record.append([cpu.process for cpu in cpus])
        record.append(processes)
        self.history.append(record)

    def create_cpus(self):
        cpu_list = []
        for i in range(self.cpu_count):
            cpu_list.append(CPU(i + 1))
        return cpu_list

    def work(self):
        for cpu in self.cpus:
            if not cpu.is_idle():
                cpu.process.remain_bt -= 1
                cpu.work_time += 1

    # 쉬게되는 CPU 개수 - 레디큐 프로세스 개수 만큼
    # 일이 끝나도 그 프로세스는 빼지 않는다.
    def get_cpu_keep_working_count(self, quantum=-1):
        cpu_work_continue_count = 0
        for cpu in self.cpus:
            if cpu.is_finished(quantum) or cpu.is_idle():
                cpu_work_continue_count += 1
        return cpu_work_continue_count - len(self.ready_queue)

    @abstractmethod
    def run(self):
        pass

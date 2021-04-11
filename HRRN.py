from Scheduler import *


class HRRN(Scheduler):
    def __init__(self, process_input_list, cpu_count):
        super().__init__(process_input_list, cpu_count)

    def run(self):
        cur_time = 0
        finish_processes_count = 0
        AT_idx = 0
        sorted_processes = sorted(self.processes, key=lambda x: x.AT)
        while finish_processes_count < self.process_count:
            # 현재 시간과 AT가 일치하는 프로세스를 대기열 큐에 넣어주기
            for process_idx in range(AT_idx, self.process_count):
                process = sorted_processes[process_idx]
                if process.AT == cur_time:
                    print("process arrived - cur_time:", cur_time, " p_id :", process.process_id)
                    self.ready_queue.append(process)
                elif process.AT > cur_time:  # 더이상 검사할 필요가 없으므로 종료
                    AT_idx = process_idx
                    break

            super().work()
            for cpu in self.cpus:
                # 만약 cpu의 일이 끝났으면, 끝난 프로세스의 output을 저장하고 cpu를 쉬게 한다.
                if cpu.is_finished():
                    print("process finished - cur_time:", cur_time, " p_id :", cpu.process.process_id)
                    cpu.process.calculate_finished_process(cur_time)
                    finish_processes_count += 1
                    cpu.set_idle()

                # 다음 프로세스(next process)를 선택한다. (대기열 큐 중 response ratio가 가장 높은 것)
                if cpu.is_idle():
                    if self.ready_queue:
                        max_response_ratio = float("-inf")
                        for process in self.ready_queue:
                            response_ratio = (process.WT + process.BT) / process.BT
                            if response_ratio > max_response_ratio:
                                max_response_ratio = response_ratio
                                next_process = process
                        self.ready_queue.remove(next_process)  # 선택한 프로세스를 대기열 큐에서 삭제
                        cpu.set_process(next_process)

            # ready_queue의 모든 프로세스의 WT를 1씩 추가
            for process in self.ready_queue:
                process.WT += 1

            # 현재 시간 1 증가
            cur_time += 1

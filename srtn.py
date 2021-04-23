from scheduler import Scheduler


class SRTN(Scheduler):
    def run(self):
        cur_time = 0  # 시간 증가
        at_idx = 0
        finished_processes_count = 0  # 종료된 프로세스 = 총 프로세스

        sorted_processes = sorted(self.processes, key=lambda x: x.at)

        while finished_processes_count < self.process_count:
            for process_idx in range(at_idx, self.process_count):
                process = sorted_processes[process_idx]

                if process.at == cur_time:
                    print("process arrived - cur_time: ", cur_time, "p_id: ", process.id)
                    self.ready_queue.append(process)

                elif process.at > cur_time:
                    at_idx = process_idx
                    break

            # history 기록하기
            self.record_history(self.ready_queue[:], self.cpus, self.processes)

            self.ready_queue = sorted(self.ready_queue, key=lambda x: x.remain_bt)

            for cpu in self.cpus:
                # 종료된 거 있을 때 남은 remain_bt==0인 경우 => cpu free
                if cpu.is_finished():
                    print("process finished - cur_time:", cur_time, " p_id :", cpu.process.id)
                    cpu.process.calculate_finished_process(cur_time)
                    finished_processes_count += 1
                    cpu.set_idle()  # 현재 cpu free

                if cpu.is_idle():  # cpu 사용 가능하면
                    if self.ready_queue:
                        next_process = self.ready_queue.pop(0)
                        cpu.process = next_process

            if self.ready_queue:  # ready_queue가 있으면 그 후 비교
                # cpu 리스트 생성
                cpu_list = []
                for cpu in self.cpus:
                    cpu_list.append(cpu)
                cpu_list.sort(key=lambda x: x.process.remain_bt)  # 오름차순으로 정렬 (+한번만해도 괜찮을듯)

                max_idx = min(self.cpu_count, len(self.ready_queue))  # 인덱스 에러 안 뜨게
                for process_check_idx in range(max_idx):
                    back_check_idx = -(process_check_idx + 1)
                    if cpu_list[back_check_idx].process.remain_bt > self.ready_queue[process_check_idx].remain_bt:
                        print("context switching: ", cpu_list[-1].process.id, ", ", self.ready_queue[0].id)
                        swap_process = cpu_list[back_check_idx].process
                        cpu_list[back_check_idx].set_process(self.ready_queue.pop(0))
                        self.ready_queue.append(swap_process)
                    else:
                        break

            cur_time += 1
            super().work()

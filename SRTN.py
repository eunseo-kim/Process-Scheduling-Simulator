from Scheduler import *

# 유진님이 올려주신 코드로 수정


class SRTN(Scheduler):
    def run(self):
        cur_time = 0  # 시간 증가
        AT_idx = 0
        finished_processes_count = 0  # 종료된 프로세스 = 총 프로세스

        sorted_processes = sorted(self.processes, key=lambda x: x.AT)

        while finished_processes_count < self.process_count:
            for process_idx in range(AT_idx, self.process_count):
                process = sorted_processes[process_idx]

                if process.AT == cur_time:
                    print("process arrived - cur_time: ", cur_time, "p_id: ", process.process_id)
                    self.ready_queue.append(process)

                elif process.AT > cur_time:
                    AT_idx = process_idx
                    break

            # history 기록하기
            self.record_history(self.ready_queue[:], self.cpus, self.processes)

            for cpu in self.cpus:
                self.ready_queue = sorted(self.ready_queue, key=lambda x: x.remain_BT)
                # 종료된 거 있을 때 남은 remain_BT==0인 경우 => cpu free
                if cpu.is_finished():
                    print("process finished - cur_time:", cur_time, " p_id :", cpu.process.process_id)
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

                cpu_list.sort(key=lambda x: x.process.remain_BT)  # 오름차순으로 정렬

                while 1:
                    if cpu_list[-1].process.remain_BT > self.ready_queue[0].remain_BT:
                        print(
                            "context switching: ", cpu_list[-1].process.process_id, ", ", self.ready_queue[0].process_id
                        )
                        now_cpu_process = cpu_list[-1].process
                        cpu_list[-1].set_process(self.ready_queue[0])
                        self.ready_queue[0] = now_cpu_process

                        # 재정렬
                        cpu_list.sort(key=lambda x: x.process.remain_BT)
                        self.ready_queue.sort(key=lambda x: x.remain_BT)

                    else:
                        break

            cur_time += 1
            super().work()

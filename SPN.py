from Scheduler import *

class SPN(Scheduler):
    def run(self):
        cur_time = 0
        finish_processes_count = 0
        AT_idx = 0
        sorted_processes = sorted(self.processes, key= lambda x : x.AT)
        # 끝난 프로세스가 총 프로세스의 수와 같아질때까지 작동
        while(finish_processes_count < self.process_count):
            # 현재 시간에 도착할 프로세스 대기열 큐에 넣어주기
            for process_idx in range(AT_idx, self.process_count):
                process = sorted_processes[process_idx]
                if process.AT == cur_time:
                    print("processe arrived - cur_time:", cur_time, " p_id :", process.process_id)
                    self.ready_queue.append(process)
                elif process.AT > cur_time:
                    AT_idx = process_idx
                    break

            # cpu들을 돌면서
            for cpu in self.cpus:
                # cpu의 일이 끝났으면
                if cpu.is_finished(cur_time):
                    print("processe finished - cur_time:", cur_time, " p_id :", cpu.process.process_id)
                    cpu.process.calculate_finished_process(cur_time)
                    finish_processes_count += 1
                    # 일이 끝난 CPU는 쉬게 해준다.
                    cpu.set_idle()
                # cpu가 쉬고 있고
                if cpu.is_idle():
                    # 대기열에 프로세스가 하나 이상 존재한다면
                    if len(self.ready_queue) >= 1 :
                        # 대기열 내의 프로세스 중 BT가 가장 작은 프로세스를 선별하여 cpu에 set
                        process_num = 0
                        for i in range(1,len(self.ready_queue)):
                            if self.ready_queue[i].BT < self.ready_queue[process_num].BT:
                                process_num = i
                        input_process = self.ready_queue.pop(process_num)
                        cpu.set_process(input_process, cur_time, cur_time + input_process.BT)
            # 현재시간 증가
            cur_time += 1
from Scheduler import *

class SRTN(Scheduler):
    def run(self):
        cur_time=0 #시간 증가
        AT_idx=0
        finished_processes_count=0 #종료된 프로세스 = 총 프로세스

        sorted_processes=sorted(self.processes,key=lambda x:x.AT)

        while(finished_processes_count<self.process_count):
            for process_idx in range(AT_idx,self.process_count):
                process=sorted_processes[process_idx]

                if process.AT==cur_time:
                    print("process arrived - cur_time: ", cur_time,"p_id: ",process.process_id)
                    self.ready_queue.append(process)

                elif process.AT>cur_time:
                    AT_idx=process_idx
                    break

            super().work()

            for cpu in self.cpus:
                self.ready_queue=sorted(self.ready_queue,key=lambda x:x.remain_BT)
                #종료된 거 있을 때 남은 remain_BT==0인 경우 => cpu free
                if cpu.is_finished():
                        cpu.process.calculate_finished_process(cur_time)
                        finished_processes_count+=1
                        cpu.set_idle() #현재 cpu free

                if cpu.is_idle(): #cpu 사용 가능하면
                    if self.ready_queue:
                        next_process=self.ready_queue.pop(0)
                        cpu.process=next_process

            #ready_queue랑 cpu의 remain_bt랑 비교

            if self.ready_queue:#ready_queue가 있으면 그 후 비교
                for cpu in self.cpus:
                    idx=-1
                    for i in range (len(self.ready_queue)):
                        if cpu.process.remain_BT>self.ready_queue[i].remain_BT:
                            idx=i
                    if idx!=-1:
                        self.ready_queue.append(cpu.process)
                        cpu.set_process(self.ready_queue.pop(idx))

            cur_time+=1

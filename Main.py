from RR import *

def print_process_time_table(processes):
    print("----------------------------------------------------")
    print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format('PID', 'AT', 'BT', 'WT', 'TT', 'NTT'))
    average_response_time = 0
    for process in processes:
        print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(process.process_id,
                    process.AT,
                    process.BT,
                    process.WT,
                    process.TT,
                    round(process.NTT,1)))
        average_response_time += process.TT
    average_response_time /= len(processes)
    print("\nAverage response time(TT) : ", round(average_response_time, 2))
    print("----------------------------------------------------\n")


def test(process_input_list, cpu_count):
    scheduler_list = []
    # fcfs = FCFS(process_input_list, cpu_count)
    scheduler_list.append(RR(process_input_list, cpu_count, 2)) # quantum = 2
    scheduler_list.append(RR(process_input_list, cpu_count, 3)) # quantum = 3
    # scheduler_list.append(HRRN(process_input_list, cpu_count))
    # ...
    for test_idx, scheduler in enumerate(scheduler_list):
        print("[ TEST {0} - {1}]=======================================".format(test_idx + 1, type(scheduler).__name__))
        scheduler.run()
        print_process_time_table(scheduler.processes)


def main():
    test([["P1", 0, 3], ["P2", 1, 7], ["P3", 3, 2], ["P4", 5, 5], ["P5", 6, 3]], 1)
    # print("[TEST 02]")
    # test([["P1", 0, 3], ["P2", 2, 7], ["P3", 3, 2], ["P4", 5, 5], ["P5", 6, 3]], 1)
    # print("[TEST 03]")
    # test([["P1", 1, 3], ["P2", 2, 7], ["P3", 3, 2], ["P4", 5, 5], ["P5", 6, 3]], 1)
    # print("[TEST 04]")
    # test([["P1", 0, 3], ["P2", 5, 5], ["P3", 6, 3]], 1)


if __name__ == "__main__":
    main()

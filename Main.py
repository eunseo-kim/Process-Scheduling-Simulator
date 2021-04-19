from RR import *
from FCFS import *
from HRRN import *
from SPN import *
from SRTN import *
# from YOSA import *


def print_history(history):
    # ready_queue_record, cpu_record
    for cur_time, record in enumerate(history):
        print("[{0}]".format(cur_time))
        # print("ready_queue : ".format(" ".join(map(lambda x: x.process_id, record[0]))))
        print("ready_queue : ")
        # for process in record[0]:
        # print(process.process_id)
        # print(process.process_id, end=" ")
        for cpu_idx, cpu_process in enumerate(record[1]):
            print("cpu {0}: {1}".format(cpu_idx + 1, cpu_process.process_id if cpu_process else None))


def print_process_time_table(processes):
    print("----------------------------------------------------")
    print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format("PID", "AT", "BT", "WT", "TT", "NTT"))
    average_response_time = 0
    for process in processes:
        print(
            "{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(
                process.process_id, process.AT, process.BT, process.WT, process.TT, round(process.NTT, 1)
            )
        )
        average_response_time += process.TT
    average_response_time /= len(processes)
    print("\nAverage response time(TT) : ", round(average_response_time, 2))
    print("----------------------------------------------------\n")


def test(process_input_list, cpu_count):
    scheduler_list = []
    scheduler_list.append(FCFS(process_input_list, cpu_count))
    # scheduler_list.append(RR(process_input_list, cpu_count, 2))  # quantum = 2
    # scheduler_list.append(RR(process_input_list, cpu_count, 3))  # quantum = 3
    # scheduler_list.append(HRRN(process_input_list, cpu_count))
    # ...
    for test_idx, scheduler in enumerate(scheduler_list):
        print(
            "[ TEST {0} - {1} - CPU 개수: {2}]=======================================".format(
                test_idx + 1, type(scheduler).__name__, scheduler.cpu_count
            )
        )
        scheduler.run()
        print_process_time_table(scheduler.processes)
        print_history(scheduler.history)


def main():
    test([["P1", 0, 3], ["P2", 1, 7], ["P3", 3, 2], ["P4", 5, 5], ["P5", 6, 3]], 1)
    # test([["P1", 0, 3], ["P2", 1, 7], ["P3", 3, 2], ["P4", 5, 5], ["P5", 6, 3]], 2)

    # print("[TEST 02]")
    # test([["P1", 0, 3], ["P2", 2, 7], ["P3", 3, 2], ["P4", 5, 5], ["P5", 6, 3]], 1)
    # print("[TEST 03]")
    # test([["P1", 1, 3], ["P2", 2, 7], ["P3", 3, 2], ["P4", 5, 5], ["P5", 6, 3]], 1)
    # print("[TEST 04]")
    # test([["P1", 0, 3], ["P2", 5, 5], ["P3", 6, 3]], 1)


if __name__ == "__main__":
    main()

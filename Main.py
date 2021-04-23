from RR import *
from FCFS import *
from HRRN import *
from SPN import *
from SRTN import *
from YOSA import *
from Subject import *


def print_history(history):
    # ready_queue_record, cpu_record
    for cur_time, record in enumerate(history):
        print("[{0}]".format(cur_time))
        print("ready_queue : ", end="")
        for ready_queue_process in record[0]:
            print(ready_queue_process.process_id, end=" ")
        print()
        for idx, cpu_process in enumerate(record[1]):
            print("cpu {0}: {1}".format(idx + 1, cpu_process.process_id if cpu_process else None))


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


def test_YOSA():
    # subject_input_list = [
    #     Subject("알고리즘", 4, 1, 0, 0),
    #     # Subject("웹프", 3, 7, 1, 0),
    #     # Subject("직능훈", 2, 4, 2, 0),
    #     # Subject("알고리즘", 4, 5, 3, 1),
    #     Subject("C++", 4, 24, 4, 1),
    #     # Subject("웹프", 3, 3, 5, 1),
    #     # Subject("알고리즘", 4, 4, 6, 2),
    #     # Subject("데베설", 3, 5, 7, 2),
    #     # Subject("운영체제", 2, 6, 8, 2),
    # ]

    subject_input_list = [
        Subject("알고리즘", 1, 1, 0, 0),
        # Subject("웹프", 3, 7, 1, 0),
        # Subject("직능훈", 2, 4, 2, 0),
        # Subject("알고리즘", 4, 5, 3, 1),
        Subject("C++", 1, 23, 4, 1),
        # Subject("웹프", 3, 3, 5, 1),
        # Subject("알고리즘", 4, 4, 6, 2),
        # Subject("데베설", 3, 5, 7, 2),
        # Subject("운영체제", 2, 6, 8, 2),
    ]

    student_count = 2
    # for i in range(1, 40):
    #     yosa = YOSA(subject_input_list, student_count, i)
    #     yosa.run()
    yosa = YOSA(subject_input_list, student_count, 40)
    yosa.run()
    yosa = YOSA(subject_input_list, student_count, 35)
    yosa.run()


def main():
    test(
        [
            Process("p0", 8, 7, 0),
            Process("p1", 3, 4, 1),
            Process("p2", 4, 7, 2),
            Process("p3", 9, 5, 3),
            Process("p4", 1, 6, 4),
            Process("p5", 0, 6, 5),
            Process("p6", 9, 6, 6),
            Process("p7", 0, 7, 7),
            Process("p8", 1, 7, 8),
        ],
        3,
    )  # test([["P1", 0, 3], ["P2", 1, 7], ["P3", 3, 2], ["P4", 5, 5], ["P5", 6, 3]], 2)

    # print("[TEST 02]")
    # test([["P1", 0, 3], ["P2", 2, 7], ["P3", 3, 2], ["P4", 5, 5], ["P5", 6, 3]], 1)
    # print("[TEST 03]")
    # test([["P1", 1, 3], ["P2", 2, 7], ["P3", 3, 2], ["P4", 5, 5], ["P5", 6, 3]], 1)
    # print("[TEST 04]")
    # test([["P1", 0, 3], ["P2", 5, 5], ["P3", 6, 3]], 1)


if __name__ == "__main__":
    # main()
    test_YOSA()

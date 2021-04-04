def test(process_input_list, cpu_count):
    scheduler_list = []
    # fcfs = FCFS(process_input_list, cpu_count)
    # scheduler_list.append(RR(process_input_list, cpu_count))
    # scheduler_list.append(HRRN(process_input_list, cpu_count))
    # ...
    for scheduler in scheduler_list:
        scheduler.run()


def main():
    test([["p1", 0, 3], ["p2", 2, 7], ["p3", 3, 2], ["p4", 5, 5], ["p5", 6, 3]], 1)
    test([["p1", 1, 3], ["p2", 2, 7], ["p3", 3, 2], ["p4", 5, 5], ["p5", 6, 3]], 1)
    test([["p1", 0, 3], ["p2", 5, 5], ["p3", 6, 3]], 1)


if __name__ == "__main__":
    main()

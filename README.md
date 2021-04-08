# Process-Scheduling-Simulator

> 2021 Operating System_Team Project

### Python Coding Convention

-   [PEP 8 - Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)

-   [PEP 8 번역본](https://b.luavis.kr/python/python-convention)

### Code formatter

-   Prettier

---

## 클래스 구조도

#### Process(프로세스)

#### CPU(프로세서)

#### Scheduler (abstarct class)

-   속성
    -   process_count
    -   process_list
    -   cpu_count
    -   cpu_list
    -   ready_queue
-   메소드
    -   create_process(self, process_count, AT, BT)
    -   create_cpu(self, cpu_count)
    -   run(self)

##### FCFS

##### RR

##### SPN

##### SRTN

##### HRRN

##### YOSA(Your own scheduling algorithm)

> 각 스케줄링(FCFS, RR, SPN...) class는 scheduler class를 상속받는다.

---

## TODO

1. 클래스 다이어그램 작성하기
2. 각 스케줄러의 리턴값 포맷 정하기(GUI와 연동하기 위함)

class Process:
    def __init__(self, process_id, AT, BT):
        self.process_id = process_id
        self.AT = AT  # arrival time
        self.BT = BT  # burst time
        self.WT = 0  # waiting time(TT - BT)
        self.TT = 0  # turnaround time
        self.NTT = 0  # normalized turnaround time(TT/BT)

    def get_AT(self):
        return self.AT

    def get_BT(self):
        return self.BT

    def calculate_finished_process(self, cur_time) -> int:
        self.TT = cur_time - self.AT
        self.WT = self.TT - self.BT
        self.NTT = self.TT / self.BT

import random


class Process:
    def __init__(self, process_id, AT, BT, color_idx):
        self.process_id = process_id
        self.AT = AT  # arrival time
        self.BT = BT  # burst time
        self.remain_BT = BT  # remain burst time
        self.WT = 0  # waiting time(TT - BT)
        self.TT = 0  # turnaround time
        self.NTT = 0  # normalized turnaround time(TT/BT)

        # 수정 : color_palette 추가
        self.color_palette = [
            [255, 200, 162],
            [255, 150, 138],
            [243, 176, 195],
            [246, 210, 88],
            [255, 255, 181],
            [181, 236, 241],
            [170, 186, 204],
            [126, 197, 213],
            [194, 232, 141],
            [141, 196, 129],
            [154, 173, 103],
            [145, 168, 208],
            [203, 170, 203],
            [207, 208, 254],
            [236, 213, 227],
        ]
        # self.Color = random.choice(self.color_palette)
        self.Color = self.color_palette[color_idx]

    def calculate_finished_process(self, cur_time) -> int:
        self.TT = cur_time - self.AT
        if self.BT != 0:
            self.WT = self.TT - self.BT
            self.NTT = self.TT / self.BT

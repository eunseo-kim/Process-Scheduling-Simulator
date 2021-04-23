class Process:
    def __init__(self, id, at, bt, color_idx):
        self.id = id
        self.at = at  # arrival time
        self.bt = bt  # burst time
        self.remain_bt = bt  # remain burst time
        self.wt = 0  # waiting time(tt - bt)
        self.tt = 0  # turnaround time
        self.ntt = 0  # normalized turnaround time(tt/bt)

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
        self.color = self.color_palette[color_idx]

    def calculate_finished_process(self, cur_time) -> int:
        self.tt = cur_time - self.at
        if self.bt > 0:
            self.wt = self.tt - self.bt
            self.ntt = self.tt / self.bt

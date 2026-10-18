"""Vẽ comp-labeling.svg: Label Studio trong một vòng gán nhãn."""
from svgkit import Canvas

c = Canvas(1160, 356, dy=30)
c.box("sfn", 0, 50, 180, 70, ["Step Functions"])
c.box("lfn", 270, 50, 200, 70, ["Lambda", "gán nhãn"])
c.box("ls", 570, 50, 250, 180, ["Label Studio", "", "mỗi job một dự án,", "nhãn gợi ý sẵn"], "key")
c.box("hook", 920, 50, 240, 70, ["Webhook", "(Lambda)"])
c.box("pg", 920, 170, 240, 60, ["Postgres"])
c.box("exp", 0, 250, 180, 70, ["Chuyên gia"], "lab")
c.box("gate", 270, 250, 230, 70, ["Cổng đăng nhập", "(nhóm labelers)"])
c.arrow(("sfn", "r"), ("lfn", "l"))
c.arrow(("lfn", "r"), ("ls", "l", 0.194), "k ảnh")
c.arrow(("ls", "r", 0.194), ("hook", "l"), "mỗi nhãn")
c.arrow(("hook", "b"), ("pg", "t"))
c.arrow(("hook", "t"), [(1040, 14), (90, 14), ("sfn", "t")], "đủ nhãn: job chạy tiếp", dashed=True, label_seg=1, label_dy=-8)
c.arrow(("exp", "r"), ("gate", "l"))
c.arrow(("gate", "r"), [(695, 285), ("ls", "b")])
print(c.svg(), end="")

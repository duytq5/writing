"""Vẽ comp-worker.svg: worker trên máy GPU lấy job từ SQS."""
from svgkit import Canvas

c = Canvas(1160, 330)
c.box("sfn", 0, 110, 180, 70, ["Step Functions"])
c.box("sqs", 260, 110, 170, 70, ["SQS"])
c.zone(500, 0, 300, 270, "Máy GPU")
c.box("w", 520, 60, 260, 190, ["GPU Worker", "", "huấn luyện", "chấm điểm", "xuất ONNX"], "key")
c.box("s3", 920, 60, 240, 80, ["S3"], shape="cyl")
c.box("ml", 920, 190, 240, 70, ["MLflow"])
c.arrow(("sfn", "r"), ("sqs", "l"), "job")
c.arrow(("sqs", "r"), ("w", "l", 0.447), "lấy job")
c.arrow(("w", "r", 0.21), ("s3", "l", 0.5), ["ảnh vào,", "kết quả ra"], label_at=0.58)
c.arrow(("w", "r", 0.868), ("ml", "l", 0.5), ["chỉ số,", "mô hình"], label_at=0.58)
c.arrow(("w", "b"), [(650, 310), (90, 310), ("sfn", "b")], "báo xong", dashed=True, label_seg=1, label_dy=-8)
print(c.svg(), end="")

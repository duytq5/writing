"""Vẽ comp-release.svg: từ lần huấn luyện tới mô hình trên điện thoại."""
from svgkit import Canvas

c = Canvas(980, 310)
c.box("w", 0, 30, 180, 80, ["Worker"])
c.box("ml", 290, 10, 300, 120, ["MLflow", "tham số, chỉ số,", "phiên bản mô hình"], "key")
c.box("eng", 720, 30, 260, 80, ["Kỹ sư ML", "so sánh, chọn"], "mle")
c.box("rel", 720, 220, 260, 80, ["Phát hành", "(qua GitHub)"], "sys")
c.box("s3", 290, 200, 300, 110, ["S3", "model.onnx,", "manifest.json"], shape="cyl")
c.box("app", 0, 220, 180, 80, ["Ứng dụng", "kiểm SHA-256"], "app")
c.arrow(("w", "r"), ("ml", "l"), "ghi")
c.arrow(("ml", "r"), ("eng", "l"), "xem")
c.arrow(("eng", "b"), ("rel", "t"), "duyệt", label_dy=4, label_anchor="start", label_at=0.45)
c.arrow(("rel", "l"), ("s3", "r", 0.545), "xuất ONNX")
c.arrow(("s3", "l", 0.545), ("app", "r"), "tải về")
print(c.svg(), end="")

"""Vẽ comp-app.svg: ứng dụng di động và những gì nó nối tới."""
from svgkit import Canvas

c = Canvas(1160, 350, dy=30)
c.box("user", 0, 125, 170, 70, ["Người dùng"], "app")
c.box("app", 270, 10, 250, 300, ["Ứng dụng", "di động", "", "mô hình ONNX", "chạy trên máy"], "key")
c.box("api", 880, 10, 280, 70, ["Lambda API"])
c.box("auth", 880, 125, 280, 70, ["Cognito + Google"])
c.box("s3", 880, 245, 280, 75, ["S3"], shape="cyl")
c.arrow(("user", "r"), ("app", "l", 0.5), "chụp lá")
c.arrow(("app", "r", 0.117), ("api", "l"), ["danh sách cây trồng,", "phiên bản mô hình"])
c.arrow(("app", "r", 0.5), ("auth", "l"), "đăng nhập khi gửi ảnh")
c.arrow(("app", "r", 0.908), ("s3", "l", 0.53), ["gửi ảnh lên,", "tải mô hình về"])
print(c.svg(), end="")

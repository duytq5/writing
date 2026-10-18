"""Vẽ comp-api.svg: một yêu cầu đi qua API Gateway và Lambda API."""
from svgkit import Canvas

c = Canvas(1160, 250)
c.box("client", 0, 150, 180, 80, ["Ứng dụng,", "trình duyệt"], "ext")
c.box("cog", 300, 0, 220, 64, ["Cognito"])
c.box("gw", 300, 150, 220, 80, ["API Gateway"])
c.box("fn", 660, 150, 220, 80, ["Lambda API", "(FastAPI)"], "key")
c.box("pg", 960, 110, 200, 60, ["Postgres"])
c.box("s3", 960, 185, 200, 65, ["S3"], shape="cyl")
c.arrow(("client", "t", 0.4), [(72, 32), ("cog", "l")], "đăng nhập, nhận JWT", label_seg=1, label_at=0.5)
c.arrow(("cog", "b"), ("gw", "t"), "khóa kiểm tra", label_dy=4, label_at=0.5)
c.arrow(("client", "r"), ("gw", "l"), "kèm JWT")
c.arrow(("gw", "r"), ("fn", "l"), "JWT hợp lệ")
c.arrow(("fn", "r", 0.25), [(920, 170), (920, 140), ("pg", "l")])
c.arrow(("fn", "r", 0.75), [(920, 210), (920, 218), ("s3", "l", 0.5)])
print(c.svg(), end="")

"""Vẽ comp-viewer.svg: FiftyOne cho kỹ sư ML xem toàn bộ kho ảnh."""
from svgkit import Canvas

c = Canvas(1160, 200)
c.box("pg", 0, 10, 170, 64, ["Postgres"])
c.box("s3", 0, 100, 170, 90, ["S3"], shape="cyl")
c.box("fo", 360, 40, 260, 120, ["FiftyOne"], "key")
c.box("gate", 740, 55, 220, 90, ["Cổng đăng nhập", "(nhóm admins)"])
c.box("eng", 1040, 55, 120, 90, ["Kỹ sư", "ML"], "mle")
c.arrow(("pg", "r"), [(265, 42), (265, 80), ("fo", "l", 40 / 120)])
c.arrow(("s3", "r"), [(265, 145), (265, 120), ("fo", "l", 80 / 120)])
c.arrow(("eng", "l"), ("gate", "r"))
c.arrow(("gate", "l"), ("fo", "r"))
print(c.svg(), end="")

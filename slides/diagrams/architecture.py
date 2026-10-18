"""Vẽ architecture.svg: kiến trúc logic theo lớp.

Ngoài AWS: người (trái) và máy (phải). Trong AWS, từ trên xuống: Cognito,
cổng, dịch vụ, dữ liệu. Mọi người đăng nhập ở Cognito trước (dải ngang) rồi
mới tới cổng: người dùng ứng dụng qua API Gateway; chuyên gia, kỹ sư ML,
quản trị viên qua cổng xác thực (reverse proxy). Máy (GitHub Actions,
worker) không qua Cognito, vào qua IAM. Ứng dụng gửi ảnh, tải mô hình thẳng
với S3 bằng link ký sẵn. Mọi dịch vụ dùng chung Postgres và S3 (đường ngang).
Không ghi nơi triển khai (máy EC2...), phần đó ở slide triển khai.
Chạy: python3 architecture.py > architecture.svg
"""
from svgkit import Canvas, MUTED

c = Canvas(1160, 552, dy=25)
# Ngoài AWS: người và máy
c.box("app", 0, 0, 170, 80, ["Người dùng", "ứng dụng"], "app")
c.box("lab", 300, 0, 130, 80, ["Chuyên gia"], "lab")
c.box("mle", 445, 0, 130, 80, ["Kỹ sư ML"], "mle")
c.box("adm", 590, 0, 150, 80, ["Quản trị viên"], "adm")
c.box("gh", 840, 0, 150, 80, ["GitHub", "Actions"], "ext")
c.box("w", 1010, 0, 150, 80, ["GPU", "Worker"], "ext")
c.arrow(("mle", "t"), [(510, -15), (915, -15), ("gh", "t")])
c.arrow(("adm", "r"), ("gh", "l"))

c.zone(0, 105, 1160, 420, "")
c.text(40, 128, "AWS", fill=MUTED, bold=True, anchor="start", layer=c.back)
# Người: đăng nhập ở Cognito trước, rồi tới cổng. Máy: qua IAM.
c.box("cog", 30, 140, 710, 45, ["Cognito: đăng nhập, cấp token"], bold=True)
c.box("gw", 30, 215, 150, 50, ["API Gateway"], "key", bold=True)
c.box("px", 300, 215, 440, 50, ["Cổng xác thực (reverse proxy)"], "key", bold=True)
c.box("iam", 840, 215, 320, 50, ["IAM"], "key", bold=True)
for k, x in [("app", 105), ("lab", 365), ("mle", 510), ("adm", 665)]:
    c.arrow((k, "b", (x - c.boxes[k][0]) / c.boxes[k][2]), (x, 140))
    c.arrow((x, 185), (x, 215))
c.arrow(("gh", "b"), ("iam", "t", 75 / 320))
c.arrow(("w", "b", 60 / 150), ("iam", "t", 230 / 320))

# Dịch vụ
c.box("api", 30, 300, 150, 70, ["Lambda API"])
c.box("fo", 300, 300, 135, 70, ["FiftyOne"])
c.box("ls", 450, 300, 135, 70, ["Label", "Studio"])
c.box("ml", 600, 300, 140, 70, ["MLflow"])
c.box("sfn", 840, 300, 150, 70, ["Step", "Functions"])
c.box("sqs", 1010, 300, 120, 70, ["SQS"])
c.arrow(("gw", "b"), ("api", "t"))
for k in ["fo", "ls", "ml"]:
    c.arrow(("px", "b", (c.anchor(k, "t")[0] - 300) / 440), (k, "t"))
c.arrow(("iam", "b", 75 / 320), ("sfn", "t"))
c.arrow(("iam", "b", 230 / 320), ("sqs", "t"))
c.arrow(("iam", "l"), [(790, 240), (790, 335), ("ml", "r")])
c.arrow(("sfn", "r"), ("sqs", "l"))
c.arrow(("ls", "b", 110 / 135), [(560, 400), (880, 400), (880, 370)], "dự án, nhãn",
        both=True, label_seg=1, label_at=0.78)

# Dữ liệu: mọi dịch vụ dùng chung Postgres và S3
c.arrow((150, 428), (1147, 428), head=False)
for x in [150, 367, 500, 670, 950]:
    c.arrow((x, 370), (x, 428), head=False)
c.arrow(("w", "b", 137 / 150), (1147, 428), head=False)
c.box("s3", 30, 448, 540, 65, ["S3 (ảnh, mô hình)"], shape="cyl")
c.box("pg", 590, 448, 540, 65, ["Postgres (siêu dữ liệu)"], shape="cyl")
c.arrow((300, 428), (300, 448))
c.arrow((860, 428), (860, 448))
c.arrow(("app", "b", 10 / 170), [(10, 480), ("s3", "l")])
c.text(18, 410, "link ký sẵn", size=20, fill=MUTED, anchor="start")
print(c.svg(), end="")

"""Vẽ slide FiftyOne có chú thích: bên trái là phần đầu ảnh chụp, đánh số các trường;
bên phải là chú thích theo số.

Chạy từ thư mục slides: python3 diagrams/fiftyone.py
Ảnh ra ở 2x (2320x1120) và được đặt trên slide với w:1160.
Toạ độ vùng đo trên ảnh chụp thu về 2000 px chiều ngang.
"""
from PIL import Image, ImageDraw, ImageFont

SRC = "assets/fiftyone/fiftyone-grid.png"
OUT = "assets/fiftyone/fiftyone-grid-annotated.png"
W, H = 2320, 1120
CROP = (0, 85, 1000, 1238)  # thanh bên và bốn cột ảnh đầu
ORANGE = (255, 109, 4)
INK = (31, 41, 51)
MUTED = (82, 96, 109)
FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

src = Image.open(SRC).convert("RGB")
k = src.width / 2000
s = H / (CROP[3] - CROP[1])  # px trên ảnh ra cho 1 px của ảnh 2000
shot = src.crop(tuple(round(v * k) for v in CROP)).resize(
    (round((CROP[2] - CROP[0]) * s), H), Image.LANCZOS)


def p(x, y):
    return (x - CROP[0]) * s, (y - CROP[1]) * s


# (số, các vùng cần chỉ, tiêu đề, dòng mô tả)
NOTES = [
    (1, [(15, 150, 345, 178)], "Lọc dữ liệu",
     ["Bấm mũi tên cuối một trường để lọc.",
      "Ví dụ: source = edge, status = unlabeled."]),
    (2, [(15, 498, 345, 634)], "Ba loại nhãn",
     ["ground_truth: nhãn do chuyên gia gán",
      "new_label: vừa gán, chưa gộp vào phiên bản dữ liệu",
      "app_prediction: mô hình trên điện thoại đoán"]),
    (3, [(15, 912, 345, 978)], "Ảnh đang ở đâu",
     ["status: đã gán nhãn hay chưa",
      "source: edge = ảnh gửi về từ ứng dụng"]),
    (4, [(15, 1082, 345, 1116)], "Ai gán nhãn",
     ["labeled_by: tài khoản chuyên gia gán nhãn.",
      "Chọn một tên để chỉ xem ảnh của người đó."]),
    (5, [(15, 1048, 345, 1082), (15, 1116, 345, 1150)], "Gán nhãn ở vòng nào",
     ["label_round, new_label_round: vòng học chủ động.",
      "Lọc theo vòng để xem k ảnh được chọn mỗi vòng."]),
    (6, [(356, 168, 516, 284)], "Nhãn hiện trên ảnh",
     ["Chip màu trên mỗi ảnh là nhãn của ảnh đó.",
      "Ảnh đầu tiên vừa gửi về từ ứng dụng."]),
]
TITLE, LINE, GAP = 56, 42, 26  # khoảng dòng của chú thích, px

# Làm mờ ảnh chụp, giữ sáng các vùng được chỉ.
dim = Image.blend(shot, Image.new("RGB", shot.size, (0, 0, 0)), 0.45)
for _, boxes, *_ in NOTES:
    for b in boxes:
        box = tuple(round(v) for v in (*p(b[0], b[1]), *p(b[2], b[3])))
        dim.paste(shot.crop(box), box[:2])

img = Image.new("RGB", (W, H), "white")
img.paste(dim, (0, 0))
d = ImageDraw.Draw(img)
d.rounded_rectangle((0, 0, dim.width - 1, H - 1), radius=12, outline=(217, 226, 236), width=2)
f_title = ImageFont.truetype(BOLD, 42)
f_body = ImageFont.truetype(FONT, 34)
f_num = ImageFont.truetype(BOLD, 28)


def badge(cx, cy, n, r=22):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=ORANGE, outline="white", width=3)
    d.text((cx, cy), str(n), font=f_num, fill="white", anchor="mm")


for n, boxes, *_ in NOTES:
    for b in boxes:
        x0, y0 = p(b[0], b[1])
        x1, y1 = p(b[2], b[3])
        d.rounded_rectangle((x0, y0, x1, y1), radius=8, outline=ORANGE, width=5)
        if n == 6:
            badge(x1 - 28, y0 + 28, n)
        elif n == 1:
            badge(p(250, 0)[0], (y0 + y1) / 2, n)
        else:
            badge(x1 + (76 if n == 5 else 28), (y0 + y1) / 2, n)

# Chú thích bên phải, theo thứ tự số.
x, y = dim.width + 90, 30
for n, _, title, lines in NOTES:
    badge(x, y + 24, n)
    d.text((x + 44, y), title, font=f_title, fill=INK)
    for i, line in enumerate(lines):
        d.text((x + 44, y + TITLE + LINE * i), line, font=f_body, fill=MUTED)
    y += TITLE + LINE * len(lines) + GAP

img.save(OUT, optimize=True)

"""Vẽ slide màn hình gán nhãn Label Studio có chú thích: bên trái là ảnh chụp
(bỏ khung bên phải), đánh số các chỗ chính; bên phải là chú thích theo số.

Chạy từ thư mục slides: python3 diagrams/labelstudio.py
Ảnh ra ở 2x (2320x1120) và được đặt trên slide với w:1160.
Toạ độ vùng đo trên ảnh chụp thu về 2000 px chiều ngang.
"""
from PIL import Image, ImageDraw, ImageFont

SRC = "assets/labelstudio/labeling.png"
OUT = "assets/labelstudio/labeling-annotated.png"
W, H = 2320, 1120
CROP = (0, 0, 1636, 1238)  # thanh trên, ảnh, các lựa chọn, nút Submit
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


# (số, vùng cần chỉ, vị trí số trên ảnh, tiêu đề, dòng mô tả)
NOTES = [
    (1, (388, 8, 606, 46), (497, 74), "Project của job gán nhãn",
     ["ACTIVE: chờ nhãn. Gán xong: DONE.",
      "537b6d15: đầu mã của job."]),
    (2, (16, 70, 1571, 945), (60, 115), "Ảnh do job chọn",
     ["Entropy: ảnh mô hình ít chắc nhất."]),
    (3, (12, 960, 182, 1064), (210, 1012), "Chọn một nhãn",
     ["Dự đoán của mô hình được chọn sẵn.",
      "Phím 1–4. Không phải lá: ảnh bị loại."]),
    (4, (1406, 1185, 1628, 1235), (1376, 1210), "Submit",
     ["Nhãn đầu tiên được lưu.",
      "Ảnh tiếp theo tự hiện."]),
    (5, (4, 1186, 142, 1234), (172, 1210), "Ảnh đang gán",
     ["#6: mã task trong Label Studio."]),
]
TITLE, LINE, GAP = 54, 42, 30  # khoảng dòng của chú thích, px

# Làm mờ ảnh chụp, giữ sáng các vùng được chỉ.
dim = Image.blend(shot, Image.new("RGB", shot.size, (0, 0, 0)), 0.5)
for _, b, *_ in NOTES:
    box = tuple(round(v) for v in (*p(b[0], b[1]), *p(b[2], b[3])))
    dim.paste(shot.crop(box), box[:2])

img = Image.new("RGB", (W, H), "white")
img.paste(dim, (0, 0))
d = ImageDraw.Draw(img)
d.rounded_rectangle((0, 0, dim.width - 1, H - 1), radius=12, outline=(217, 226, 236), width=2)
f_title = ImageFont.truetype(BOLD, 40)
f_body = ImageFont.truetype(FONT, 32)
f_num = ImageFont.truetype(BOLD, 28)


def badge(cx, cy, n, r=22):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=ORANGE, outline="white", width=3)
    d.text((cx, cy), str(n), font=f_num, fill="white", anchor="mm")


for n, b, at, *_ in NOTES:
    d.rounded_rectangle((*p(b[0], b[1]), *p(b[2], b[3])), radius=8, outline=ORANGE, width=5)
    badge(*p(*at), n)

# Chú thích bên phải, theo thứ tự số.
x, y = dim.width + 70, 60
for n, _, _, title, lines in NOTES:
    badge(x, y + 22, n)
    d.text((x + 42, y), title, font=f_title, fill=INK)
    for i, line in enumerate(lines):
        d.text((x + 42, y + TITLE + LINE * i), line, font=f_body, fill=MUTED)
    y += TITLE + LINE * len(lines) + GAP

img.save(OUT, optimize=True)

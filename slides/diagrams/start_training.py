"""Vẽ slide GitHub Actions sau khi merge pull request huấn luyện: bên trái là
danh sách các lần chạy, đánh số theo thứ tự thời gian (từ dưới lên); bên phải
là chú thích theo số.

Chạy từ thư mục slides: python3 diagrams/start_training.py
Ảnh ra ở 2x (2320 px ngang) và được đặt trên slide với w:1160.
Toạ độ vùng đo trên ảnh chụp thu về 2000 px chiều ngang.
"""
from PIL import Image, ImageDraw, ImageFont

SRC = "assets/training/start-training-runs.png"
OUT = "assets/training/start-training-runs-annotated.png"
CROP = (0, 0, 1380, 500)  # tên các lần chạy; bỏ cột thời gian bên phải
SHOT_W = 1420  # bề rộng phần ảnh chụp trên ảnh ra, px
W = 2320
ORANGE = (255, 109, 4)
INK = (31, 41, 51)
MUTED = (82, 96, 109)
FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

src = Image.open(SRC).convert("RGB")
k = src.width / 2000
s = SHOT_W / (CROP[2] - CROP[0])  # px trên ảnh ra cho 1 px của ảnh 2000
H = round((CROP[3] - CROP[1]) * s)
shot = src.crop(tuple(round(v * k) for v in CROP)).resize((SHOT_W, H), Image.LANCZOS)


def p(x, y):
    return (x - CROP[0]) * s, (y - CROP[1]) * s


# (số, vùng cần chỉ, tiêu đề, dòng mô tả); số theo thứ tự thời gian
NOTES = [
    (1, (10, 290, 1340, 390), "CI trên pull request",
     ["Kiểm tra tệp huấn luyện trước khi review."]),
    (2, (10, 185, 1060, 285), "Merge vào main",
     ["CI chạy lại trên main sau khi merge."]),
    (3, (10, 80, 1060, 180), "start-training khởi động job",
     ["Kiểm tra phiên bản dữ liệu, ghi job",
      "kèm người merge và commit."]),
]
TITLE, LINE, GAP = 50, 40, 30  # khoảng dòng của chú thích, px

# Làm mờ ảnh chụp, giữ sáng các vùng được chỉ.
dim = Image.blend(shot, Image.new("RGB", shot.size, (0, 0, 0)), 0.45)
for _, b, *_ in NOTES:
    box = tuple(round(v) for v in (*p(b[0], b[1]), *p(b[2], b[3])))
    dim.paste(shot.crop(box), box[:2])

img = Image.new("RGB", (W, H), "white")
img.paste(dim, (0, 0))
d = ImageDraw.Draw(img)
d.rounded_rectangle((0, 0, dim.width - 1, H - 1), radius=12, outline=(217, 226, 236), width=2)
f_title = ImageFont.truetype(BOLD, 38)
f_body = ImageFont.truetype(FONT, 30)
f_num = ImageFont.truetype(BOLD, 28)


def badge(cx, cy, n, r=22):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=ORANGE, outline="white", width=3)
    d.text((cx, cy), str(n), font=f_num, fill="white", anchor="mm")


for n, b, *_ in NOTES:
    x0, y0 = p(b[0], b[1])
    x1, y1 = p(b[2], b[3])
    d.rounded_rectangle((x0, y0, x1, y1), radius=8, outline=ORANGE, width=5)
    badge(x1 - 6, y0 + 6, n)

# Chú thích bên phải, theo thứ tự số.
x, y = dim.width + 70, 40
for n, _, title, lines in NOTES:
    badge(x, y + 20, n)
    d.text((x + 40, y), title, font=f_title, fill=INK)
    for i, line in enumerate(lines):
        d.text((x + 40, y + TITLE + LINE * i), line, font=f_body, fill=MUTED)
    y += TITLE + LINE * len(lines) + GAP

img.save(OUT, optimize=True)

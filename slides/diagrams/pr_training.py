"""Vẽ slide pull request huấn luyện có chú thích: bên trái là diff của tệp
configs/trainings/, đánh số các phần; bên phải là chú thích theo số.

Chạy từ thư mục slides: python3 diagrams/pr_training.py
Ảnh ra ở 2x (2320x880) và được đặt trên slide với w:1160.
Toạ độ vùng đo trên ảnh chụp thu về 2000 px chiều ngang.
"""
from PIL import Image, ImageDraw, ImageFont

SRC = "assets/training/pr-training-diff.png"
OUT = "assets/training/pr-training-diff-annotated.png"
W, H = 2320, 880
CROP = (0, 0, 1140, 692)  # tên tệp và 17 dòng code
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


# (số, vùng cần chỉ, tiêu đề, dòng mô tả)
NOTES = [
    (1, (115, 90, 985, 195), "Vì sao có job này",
     ["Mô hình thứ hai của rocole:",
      "thêm 10 nhãn từ job gán nhãn 537b6d15."]),
    (2, (115, 196, 915, 265), "Dữ liệu huấn luyện",
     ["Phiên bản 2 = phiên bản 1 + 10 nhãn mới.",
      "Ghi rõ số phiên bản: chạy lại, cùng kết quả."]),
    (3, (115, 300, 965, 650), "Công thức và tham số",
     ["Giống hệt mô hình phiên bản 1,",
      "nên chỉ có dữ liệu thay đổi."]),
    (4, (115, 651, 1080, 686), "Điểm xuất phát",
     ["null: từ trọng số ImageNet.",
      "Tên một mô hình: tinh chỉnh từ mô hình đó."]),
]
TITLE, LINE, GAP = 54, 42, 34  # khoảng dòng của chú thích, px

# Làm mờ ảnh chụp, giữ sáng các vùng được chỉ.
dim = Image.blend(shot, Image.new("RGB", shot.size, (0, 0, 0)), 0.45)
for _, b, *_ in NOTES:
    box = tuple(round(v) for v in (*p(b[0], b[1]), *p(b[2], b[3])))
    dim.paste(shot.crop(box), box[:2])

img = Image.new("RGB", (W, H), "white")
img.paste(dim, (0, 0))
d = ImageDraw.Draw(img)
d.rounded_rectangle((0, 0, dim.width - 1, H - 1), radius=12, outline=(217, 226, 236), width=2)
f_title = ImageFont.truetype(BOLD, 40)
f_body = ImageFont.truetype(FONT, 31)
f_num = ImageFont.truetype(BOLD, 28)


def badge(cx, cy, n, r=22):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=ORANGE, outline="white", width=3)
    d.text((cx, cy), str(n), font=f_num, fill="white", anchor="mm")


for n, b, *_ in NOTES:
    x0, y0 = p(b[0], b[1])
    x1, y1 = p(b[2], b[3])
    d.rounded_rectangle((x0, y0, x1, y1), radius=8, outline=ORANGE, width=5)
    badge(x1 + 30, (y0 + y1) / 2, n)

# Chú thích bên phải, theo thứ tự số.
x, y = dim.width + 80, 60
for n, _, title, lines in NOTES:
    badge(x, y + 22, n)
    d.text((x + 42, y), title, font=f_title, fill=INK)
    for i, line in enumerate(lines):
        d.text((x + 42, y + TITLE + LINE * i), line, font=f_body, fill=MUTED)
    y += TITLE + LINE * len(lines) + GAP

img.save(OUT, optimize=True)

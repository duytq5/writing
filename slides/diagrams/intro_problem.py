"""Vẽ slide đầu của Phần I: ảnh lá cà phê bị gỉ sắt bên trái, ba con số thiệt
hại bên phải (mục 1.1 Đặt vấn đề), một dòng kết ở dưới.

Chạy từ thư mục slides: python3 diagrams/intro_problem.py
Ảnh ra ở 2x (2320x1080) và được đặt trên slide với w:1160.
"""
from PIL import Image, ImageDraw, ImageFont, ImageOps

SRC = "assets/intro/coffee-rust.jpg"
OUT = "assets/intro/problem.png"
W, H = 2320, 1080
PHOTO_W = 1200
RED = (207, 34, 46)
INK = (31, 41, 51)
MUTED = (82, 96, 109)
FAINT = (154, 165, 177)
FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

# (con số, hai dòng giải thích); nguồn trong chapters/01-intro.md, mục 1.1
STATS = [
    ("10–40%", ["sản lượng nông nghiệp mất do sâu bệnh", "≈ 220 tỷ USD mỗi năm"]),
    ("16–34%", ["năng suất cà phê giảm do gỉ sắt", "Tây Nguyên, Tây Bắc"]),
    ("> 30%", ["sản lượng sầu riêng giảm do cháy lá", "Cai Lậy, Tiền Giang"]),
]

img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

# Ảnh: cắt cho vừa khung, bo góc.
photo = ImageOps.fit(Image.open(SRC).convert("RGB"), (PHOTO_W, H), Image.LANCZOS, centering=(0.45, 0.5))
mask = Image.new("L", photo.size, 0)
ImageDraw.Draw(mask).rounded_rectangle((0, 0, PHOTO_W - 1, H - 1), 24, fill=255)
img.paste(photo, (0, 0), mask)
d.text((24, H - 24), "Ảnh: Hemileia vastatrix trên lá cà phê, Wikimedia Commons",
       font=ImageFont.truetype(FONT, 24), fill="white", anchor="ls")

# Ba con số, chia đều chiều cao.
x = PHOTO_W + 90
f_num = ImageFont.truetype(BOLD, 104)
f_line = ImageFont.truetype(FONT, 38)
row = (H - 40) / len(STATS)
for i, (num, lines) in enumerate(STATS):
    y = 40 + i * row + 20
    d.text((x, y), num, font=f_num, fill=RED)
    for j, s in enumerate(lines):
        d.text((x, y + 124 + 48 * j), s, font=f_line, fill=INK if j == 0 else MUTED)

img.save(OUT, optimize=True)

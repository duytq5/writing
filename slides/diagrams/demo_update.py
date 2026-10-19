"""Ghép hai ảnh chụp ứng dụng thành một dải cho slide "ứng dụng nhận mô hình
mới", với khung đánh số trên các chỗ chính.

Chạy từ thư mục slides: python3 diagrams/demo_update.py
Ảnh ra ở 2x (2320 px) và được đặt trên slide với w:1160. Chú thích theo số nằm
trong danh sách cards bên dưới ảnh.
Toạ độ khung đo trên ảnh điện thoại thu về 920x2000.
"""
from PIL import Image, ImageDraw, ImageFont

W, H, S = 1160, 400, 2  # bề rộng slide, chiều cao dải, tỉ lệ
SRC = "assets/release/"
ORANGE = (255, 109, 4)
BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
GAP = 120  # khoảng giữa hai điện thoại, px trên ảnh ra

# (ảnh, các khung: (số, x0, y0, x1, y1))
PHONES = [
    ("app-update-available.png", [(1, 75, 690, 380, 738), (2, 95, 875, 425, 945)]),
    ("app-update-downloading.png", [(3, 75, 845, 845, 925)]),
]


def rounded(img, radius):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, img.width - 1, img.height - 1), radius, fill=255)
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    ImageDraw.Draw(out).rounded_rectangle((0, 0, img.width - 1, img.height - 1), radius, outline=(217, 226, 236), width=2)
    return out


h = (H - 4) * S
f_num = ImageFont.truetype(BOLD, 28)
canvas = Image.new("RGBA", (W * S, H * S), (255, 255, 255, 0))
d = ImageDraw.Draw(canvas)
phones = []
for name, _ in PHONES:
    img = Image.open(SRC + name).convert("RGB")
    phones.append(img.resize((round(img.width * h / img.height), h), Image.LANCZOS))
total = sum(p.width for p in phones) + GAP * (len(phones) - 1)
x = (W * S - total) // 2
y = (H * S - h) // 2
for img, (_, boxes) in zip(phones, PHONES):
    canvas.paste(rounded(img, 22 * S), (x, y), rounded(img, 22 * S))
    k = img.width / 920
    for n, x0, y0, x1, y1 in boxes:
        pad = 12  # khoảng trống quanh chữ, trong khung 920x2000
        bx0, by0 = x + (x0 - pad) * k, y + (y0 - pad) * k
        bx1, by1 = x + (x1 + pad) * k, y + (y1 + pad) * k
        d.rounded_rectangle((bx0, by0, bx1, by1), radius=8, outline=ORANGE, width=4)
        cx, cy, r = bx1 + 30, (by0 + by1) / 2, 22
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=ORANGE, outline="white", width=3)
        d.text((cx, cy), str(n), font=f_num, fill="white", anchor="mm")
    x += img.width + GAP

canvas.save(SRC + "app-update-strip.png", optimize=True)

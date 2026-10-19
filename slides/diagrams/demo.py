"""Ghép ảnh chụp màn hình điện thoại thành một dải cho mỗi slide Demo.

Chạy từ thư mục slides: python3 diagrams/demo.py
Ảnh ra ở 2x (2320 px) và được đặt trên slide với w:1160. Mỗi điện thoại nằm
đúng giữa một thẻ của danh sách cards bên dưới (flex: 1, gap 18px).
"""
from PIL import Image, ImageDraw

W, GAP, H, S = 1160, 18, 400, 2  # bề rộng slide, khoảng cách thẻ, chiều cao dải, tỉ lệ
SRC = "assets/demo/"


def centers(n):
    card = (W - GAP * (n - 1)) / n
    return [card / 2 + i * (card + GAP) for i in range(n)]


def rounded(img, radius):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, img.width - 1, img.height - 1), radius, fill=255)
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    ImageDraw.Draw(out).rounded_rectangle((0, 0, img.width - 1, img.height - 1), radius, outline=(217, 226, 236), width=2)
    return out


def phone(name, height):
    img = Image.open(SRC + name).convert("RGB")
    img = img.resize((round(img.width * height / img.height), height), Image.LANCZOS)
    return rounded(img, 22 * S)


def strip(items, out):
    """items: một ảnh (đã thu nhỏ) cho mỗi cột, hoặc None để bỏ trống cột đó."""
    canvas = Image.new("RGBA", (W * S, H * S), (255, 255, 255, 0))
    for c, img in zip(centers(len(items)), items):
        if img is not None:
            canvas.paste(img, (round(c * S - img.width / 2), round((H * S - img.height) / 2)), img)
    canvas.save(SRC + out, optimize=True)


h = (H - 4) * S
strip([phone(f, h) for f in ["01-dong-y.png", "02-dang-nhap.png", "03-chon-mo-hinh.png",
                            "04-dang-tai.png", "05-san-sang.png"]], "demo-tai-mo-hinh.png")

# Cột thứ ba: phóng to ảnh lá trong màn hình kết quả, để người xem thấy đây là gỉ sắt.
res = Image.open(SRC + "07-ket-qua.png").convert("RGB")
k = res.width / 920  # toạ độ đo trên ảnh 920 px
leaf = res.crop((round(46 * k), round(334 * k), round(874 * k), round(1110 * k)))
lw = 340 * S
leaf = rounded(leaf.resize((lw, round(leaf.height * lw / leaf.width)), Image.LANCZOS), 16 * S)
strip([phone("06-chon-anh.png", h), phone("07-ket-qua.png", h), leaf], "demo-chan-doan.png")

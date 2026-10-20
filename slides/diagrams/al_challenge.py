"""Vẽ al-challenge.svg: ảnh người dùng gửi về là cơ hội, nhưng có ba rào cản trước chuyên gia.

Ảnh điện thoại và các ô ảnh lấy từ ảnh chụp màn hình ứng dụng (assets/demo/07-ket-qua.png),
thu nhỏ và nhúng thẳng vào SVG (data URI) để SVG tự đứng được khi đặt bằng thẻ ảnh.
SVG đặt trên slide ở tỉ lệ 1:1 (rộng 1160). Chạy: python3 al_challenge.py > al-challenge.svg
"""
import base64
import io
import random
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

from svgkit import Canvas, INK, MUTED, FAINT, STYLE

W, H = 1160, 500
SHOT = Path(__file__).resolve().parent.parent / "assets/demo/07-ket-qua.png"
RED = STYLE["adm"][1]
LAB_FILL, LAB = STYLE["lab"]


def uri(im, size):
    im = im.convert("RGB").resize(size, Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=80)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


shot = Image.open(SHOT)
k = shot.width / 920  # toạ độ dưới đây đo trên ảnh hiển thị rộng 920
leaf = shot.crop([int(v * k) for v in (60, 345, 862, 1100)])

c = Canvas(W, H)
clips = []


def image(x, y, w, h, data, rx=8, rotate=0, stroke=None):
    cid = f"c{len(clips)}"
    clips.append(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/></clipPath>')
    t = f' transform="rotate({rotate} {x + w / 2} {y + h / 2})"' if rotate else ""
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="none" stroke="{stroke}" stroke-width="3"/>' if stroke else ""
    c.front.append(f'<g{t}><image x="{x}" y="{y}" width="{w}" height="{h}" href="{data}" '
                   f'clip-path="url(#{cid})" preserveAspectRatio="xMidYMid slice"/>{s}</g>')


# 1. Điện thoại: màn hình kết quả của ứng dụng
PW, PH = 200, round(200 * shot.height / shot.width)
image(0, 20, PW, PH, uri(shot, (PW * 2, PH * 2)), rx=26, stroke=STYLE["app"][1])
c.arrow((PW + 12, 240), (288, 240))

# 2. Đống ảnh mới: các ô cắt từ ảnh lá, xoay lệch nhau
rnd = random.Random(7)
for i in range(9):
    r, col = divmod(i, 3)
    s = rnd.randint(260, 520)
    x0, y0 = rnd.randint(0, leaf.width - s), rnd.randint(0, leaf.height - s)
    tile = leaf.crop((x0, y0, x0 + s, y0 + s))
    if i in (2, 6):
        tile = tile.filter(ImageFilter.GaussianBlur(10))
    if i == 4:
        tile = ImageEnhance.Brightness(tile).enhance(0.45)
    image(300 + col * 76 + rnd.randint(-6, 6), 128 + r * 76 + rnd.randint(-6, 6), 70, 70,
          uri(tile, (140, 140)), rx=6, rotate=rnd.randint(-9, 9))
c.text(410, 400, "ảnh mới mỗi ngày", bold=True, fill=MUTED)

# 3. Đường tới chuyên gia, bị ba rào cản chắn ngang
c.back.append(f'<path d="M532,240 L948,240" stroke="{FAINT}" stroke-width="3" stroke-dasharray="9 7" marker-end="url(#ar)"/>')
CX, CW, CH = 580, 350, 128
for j, label in enumerate(["chuyên gia đắt", "ảnh nhiễu", "quá nhiều"]):
    y = 26 + j * (CH + 16)
    c.front.append(f'<rect x="{CX}" y="{y}" width="{CW}" height="{CH}" rx="10" fill="#ffffff" stroke="{RED}" stroke-width="2.5"/>')
    ix, iy = CX + 22, y + 19  # ô biểu tượng 90x90
    if j == 0:  # đồng hồ
        cx, cy = ix + 45, iy + 45
        c.front.append(f'<circle cx="{cx}" cy="{cy}" r="38" fill="#ffffff" stroke="{INK}" stroke-width="4"/>'
                       f'<path d="M{cx},{cy} L{cx},{cy - 26} M{cx},{cy} L{cx + 18},{cy + 10}" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
    elif j == 1:  # ảnh mờ
        image(ix, iy, 90, 90, uri(leaf.filter(ImageFilter.GaussianBlur(14)), (180, 180)), rx=8)
    else:  # chồng ảnh cao, chỉ một phần nhỏ được gán
        for b in range(9):
            fill = STYLE["sys"][1] if b == 8 else "#cbd2d9"
            c.front.append(f'<rect x="{ix + 10}" y="{iy + b * 10}" width="70" height="7" rx="2" fill="{fill}"/>')
    c.text(ix + 112, y + CH / 2 + 8, label, size=26, bold=True, anchor="start")

# 4. Chuyên gia
ex, ey = 1062, 196
c.front.append(f'<circle cx="{ex}" cy="{ey - 44}" r="30" fill="{LAB_FILL}" stroke="{LAB}" stroke-width="3"/>'
               f'<path d="M{ex - 56},{ey + 58} Q{ex - 56},{ey - 6} {ex},{ey - 6} Q{ex + 56},{ey - 6} {ex + 56},{ey + 58} Z" '
               f'fill="{LAB_FILL}" stroke="{LAB}" stroke-width="3"/>')
c.text(ex, ey + 96, "chuyên gia", bold=True)

c.front.insert(0, "<defs>" + "".join(clips) + "</defs>")
print(c.svg(), end="")

"""Vẽ hai slide chiến lược chọn mẫu của phần III:
  python3 al_strategies.py uncertainty > al-uncertainty.svg
  python3 al_strategies.py balance > al-balance.svg

uncertainty: một ảnh mô hình chắc và một ảnh mô hình phân vân; ba chiến lược least confidence,
margin, entropy đọc cùng ba điểm của ảnh phân vân theo ba cách.
balance: random (mốc so sánh) và class-balanced (ưu tiên lớp hiếm).
Điểm số là ví dụ minh hoạ. Ảnh lá cắt từ assets/demo/07-ket-qua.png, nhúng thẳng vào SVG.
SVG đặt trên slide ở tỉ lệ 1:1 (rộng 1160).
"""
import base64
import io
import math
import random
import sys
from pathlib import Path

from PIL import Image

from svgkit import Canvas, INK, MUTED, FAINT

MODE = sys.argv[1] if len(sys.argv) > 1 else "uncertainty"
SHOT = Path(__file__).resolve().parent.parent / "assets/demo/07-ket-qua.png"
BRAND, GREEN, GREY = "#1e5631", "#2f7d4f", "#cbd2d9"
CLASSES = ["khỏe", "gỉ sắt", "nhện đỏ"]


def uri(im, size):
    im = im.convert("RGB").resize(size, Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=80)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def num(v):
    return f"{v:.2f}".replace(".", ",")


shot = Image.open(SHOT)
k = shot.width / 920  # toạ độ đo trên ảnh hiển thị rộng 920
leaf = shot.crop([int(v * k) for v in (60, 345, 862, 1100)])
clips = []


def image(c, x, y, w, h, im, rx=8):
    cid = f"c{len(clips)}"
    clips.append(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/></clipPath>')
    c.front.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="{uri(im, (w * 2, h * 2))}" '
                   f'clip-path="url(#{cid})" preserveAspectRatio="xMidYMid slice"/>')


def rect(c, x, y, w, h, fill, rx=4, stroke=None, sw=2):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    c.front.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"{s}/>')


def finish(c):
    c.front.insert(0, "<defs>" + "".join(clips) + "</defs>")
    print(c.svg(), end="")


def uncertainty():
    c = Canvas(1160, 500)
    SURE, UNSURE = [0.03, 0.92, 0.05], [0.40, 0.35, 0.25]

    # Trái: hai ảnh, mỗi ảnh một thanh điểm ngang cho ba lớp
    for j, (title, p, crop, picked) in enumerate([
            ("mô hình chắc chắn", SURE, (420, 160, 900, 640), False),
            ("mô hình phân vân", UNSURE, (40, 300, 520, 780), True)]):
        y = 10 + j * 230
        rect(c, 0, y, 430, 210, "#ffffff", rx=12, stroke=BRAND if picked else FAINT, sw=4 if picked else 2)
        c.text(20, y + 36, title, bold=True, anchor="start", fill=BRAND if picked else MUTED)
        image(c, 20, y + 56, 130, 130, leaf.crop(crop))
        for i, (name, v) in enumerate(zip(CLASSES, p)):
            by = y + 64 + i * 42
            c.text(170, by + 22, name, size=20, anchor="start", fill=MUTED)
            rect(c, 258, by + 4, 120 * v, 24, GREEN if picked else GREY)
            c.text(258 + 120 * v + 8, by + 23, num(v), size=20, anchor="start", fill=INK)
    c.text(215, 490, "được chọn: ảnh phân vân", bold=True, fill=BRAND)

    # Phải: ba cách đọc cùng ba điểm của ảnh phân vân
    H = -sum(v * math.log(v) for v in UNSURE)
    COLS = [
        ("Least confidence", "điểm cao nhất thấp", {0}, f"1 − {num(UNSURE[0])} = {num(1 - UNSURE[0])}"),
        ("Margin", "hai điểm đầu sát nhau", {0, 1}, f"{num(UNSURE[0])} − {num(UNSURE[1])} = {num(UNSURE[0] - UNSURE[1])}"),
        ("Entropy", "điểm dàn đều", {0, 1, 2}, f"H = {num(H)}"),
    ]
    BASE, MAXH, BW = 300, 230, 44
    for j, (name, desc, hot, calc) in enumerate(COLS):
        x0 = 480 + j * 230
        for i, v in enumerate(UNSURE):
            bx = x0 + 18 + i * 64
            h = MAXH * v / 0.45
            rect(c, bx, BASE - h, BW, h, BRAND if i in hot else GREY)
            c.text(bx + BW / 2, BASE - h - 8, num(v), size=20, fill=INK if i in hot else MUTED)
        if name == "Margin":  # phần cột đầu cao hơn cột thứ hai = khoảng cách margin
            y1, y2 = BASE - MAXH * UNSURE[0] / 0.45, BASE - MAXH * UNSURE[1] / 0.45
            rect(c, x0 + 18, y1, BW, y2 - y1, "#bf8700", rx=2)
            c.front.append(f'<line x1="{x0 + 10}" y1="{y2:.0f}" x2="{x0 + 82 + BW + 8}" y2="{y2:.0f}" '
                           f'stroke="#bf8700" stroke-width="2" stroke-dasharray="6 4"/>')
        c.front.append(f'<line x1="{x0 + 8}" y1="{BASE}" x2="{x0 + 210}" y2="{BASE}" stroke="{FAINT}" stroke-width="1.5"/>')
        c.text(x0 + 109, BASE + 40, name, bold=True)
        c.text(x0 + 109, BASE + 72, desc, size=20, fill=MUTED)
        c.text(x0 + 109, BASE + 104, calc, size=20, fill=BRAND, bold=True)
    c.text(824, 490, "cột: khỏe · gỉ sắt · nhện đỏ", size=20, fill=MUTED)
    finish(c)


def balance():
    c = Canvas(1160, 470)
    # Trái: random, 10 ô bốc ngẫu nhiên trong lưới 8x5
    c.text(250, 30, "Ngẫu nhiên (random)", bold=True, size=26)
    rnd = random.Random(3)
    picks = set(rnd.sample(range(40), 10))
    T, G = 48, 8
    for i in range(40):
        r, col = divmod(i, 8)
        rect(c, 22 + col * (T + G), 64 + r * (T + G), T, T, GREEN if i in picks else "#e4e7eb", rx=6)
    c.text(250, 380, "bốc 10 ảnh bất kỳ", size=22, fill=INK)
    c.text(250, 414, "không cần mô hình: mốc so sánh", size=20, fill=MUTED)

    c.front.append(f'<line x1="540" y1="10" x2="540" y2="440" stroke="{FAINT}" stroke-width="1.5"/>')

    # Phải: class-balanced, lớp càng ít nhãn thì trọng số càng lớn
    c.text(860, 30, "Cân bằng lớp (class-balanced)", bold=True, size=26)
    c.text(730, 84, "nhãn đã có", size=20, fill=MUTED)
    c.text(980, 84, "trọng số", size=20, fill=MUTED)
    FREQ = [0.55, 0.35, 0.10]  # minh hoạ: lớp nhện đỏ hiếm
    for i, (name, f) in enumerate(zip(CLASSES, FREQ)):
        y = 110 + i * 70
        c.text(640, y + 30, name, size=22, anchor="end")
        rect(c, 660, y + 8, 300 * f, 30, GREY)
        w = 0.06 / f  # nghịch với tần suất
        rect(c, 920, y + 8, 140 * w / (0.06 / FREQ[2]), 30, BRAND if i == 2 else GREEN)
    c.arrow((830, 78), (900, 78))
    c.text(860, 380, "ưu tiên ảnh có thể thuộc lớp hiếm", size=22, fill=INK)
    c.text(860, 414, "điểm = entropy × trọng số lớp", size=20, fill=BRAND, bold=True)
    finish(c)


{"uncertainty": uncertainty, "balance": balance}[MODE]()

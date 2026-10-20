"""Vẽ lưới ảnh pool cho phần III:
  python3 al_pool.py question > al-question.svg
  python3 al_pool.py pick > al-pick.svg

question: 40 ảnh chưa nhãn (xám), một huy hiệu ngân sách 10 nhãn và câu hỏi "chọn ảnh nào?".
pick: cùng 40 ảnh, 10 ảnh mô hình chọn hiện màu, bên phải là vòng lặp học chủ động.
Các ô ảnh cắt từ ảnh lá trong ảnh chụp màn hình ứng dụng (assets/demo/07-ket-qua.png),
thu nhỏ và nhúng thẳng vào SVG (data URI). SVG đặt trên slide ở tỉ lệ 1:1 (rộng 1160).
"""
import base64
import io
import random
import sys
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

from svgkit import Canvas, MUTED, STYLE

MODE = sys.argv[1] if len(sys.argv) > 1 else "question"
W, H = (1160, 545) if MODE == "question" else (1160, 430)
COLS, ROWS = 8, 5
T, GAP = (76, 10) if MODE == "question" else (64, 8)
BUDGET = 10
SHOT = Path(__file__).resolve().parent.parent / "assets/demo/07-ket-qua.png"
LAB_FILL, LAB = STYLE["lab"]
BRAND = "#1e5631"


def uri(im, size):
    im = im.convert("RGB").resize(size, Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=78)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


shot = Image.open(SHOT)
k = shot.width / 920  # toạ độ đo trên ảnh hiển thị rộng 920
leaf = shot.crop([int(v * k) for v in (60, 345, 862, 1100)])

c = Canvas(W, H)
clips = []


def image(x, y, w, h, data, rx=6):
    cid = f"c{len(clips)}"
    clips.append(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/></clipPath>')
    c.front.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="{data}" '
                   f'clip-path="url(#{cid})" preserveAspectRatio="xMidYMid slice"/>')


# Lưới ảnh pool: mỗi ô là một mảnh cắt khác nhau của ảnh lá, lật/xoay để trông như nhiều ảnh.
# Cùng seed cho cả hai chế độ để slide "pick" hiện lại đúng các ảnh của slide "question".
rnd = random.Random(11)
PICKED = set(random.Random(5).sample(range(COLS * ROWS), BUDGET)) if MODE == "pick" else set()
GX, GY = (0, 10) if MODE == "question" else (6, 24)
for i in range(COLS * ROWS):
    r, col = divmod(i, COLS)
    s = rnd.randint(220, 560)
    x0, y0 = rnd.randint(0, leaf.width - s), rnd.randint(0, leaf.height - s)
    tile = leaf.crop((x0, y0, x0 + s, y0 + s)).rotate(rnd.choice((0, 90, 180, 270)))
    if rnd.random() < 0.15:
        tile = tile.filter(ImageFilter.GaussianBlur(8))
    if i not in PICKED:
        tile = ImageEnhance.Color(tile).enhance(0.12)
        tile = ImageEnhance.Brightness(tile).enhance(1.15)
    x, y = GX + col * (T + GAP), GY + r * (T + GAP)
    image(x, y, T, T, uri(tile, (T * 2, T * 2)))
    if i in PICKED:
        c.front.append(f'<rect x="{x - 3}" y="{y - 3}" width="{T + 6}" height="{T + 6}" rx="8" fill="none" stroke="{BRAND}" stroke-width="5"/>')
grid_w = COLS * T + (COLS - 1) * GAP
grid_h = ROWS * T + (ROWS - 1) * GAP

if MODE == "pick":
    # Vòng lặp học chủ động, chạy theo chiều kim đồng hồ
    c.text(grid_w / 2, GY + grid_h + 34, f"{BUDGET} ảnh mô hình chọn", fill=BRAND, bold=True)
    BW, BH = 230, 84
    c.box("score", 640, 60, BW, BH, ["Mô hình", "chấm điểm"])
    c.box("pick", 920, 60, BW, BH, [f"Chọn {BUDGET} ảnh", "“phù hợp” nhất"], cls="key", bold=True)
    c.box("label", 920, 280, BW, BH, ["Chuyên gia", "gán nhãn"], cls="lab")
    c.box("train", 640, 280, BW, BH, ["Huấn luyện lại"])
    c.arrow(("score", "r"), ("pick", "l"))
    c.arrow(("pick", "b"), ("label", "t"))
    c.arrow(("label", "l"), ("train", "r"))
    c.arrow(("train", "t"), ("score", "b"))
    c.text(895, 222, "lặp lại", fill=MUTED, bold=True)
    c.front.insert(0, "<defs>" + "".join(clips) + "</defs>")
    print(c.svg(), end="")
    sys.exit()

c.text(grid_w / 2, GY + grid_h + 34, "ảnh chưa có nhãn", fill=MUTED, bold=True)

# Huy hiệu ngân sách: chuyên gia chỉ gán được 10 ảnh
bx, by, bw, bh = 800, 40, 330, 300
c.front.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="16" fill="{LAB_FILL}" stroke="{LAB}" stroke-width="3"/>')
ex, ey = bx + bw / 2, by + 92
c.front.append(f'<circle cx="{ex}" cy="{ey - 30}" r="24" fill="#ffffff" stroke="{LAB}" stroke-width="3"/>'
               f'<path d="M{ex - 44},{ey + 44} Q{ex - 44},{ey - 2} {ex},{ey - 2} Q{ex + 44},{ey - 2} {ex + 44},{ey + 44} Z" '
               f'fill="#ffffff" stroke="{LAB}" stroke-width="3"/>')
c.text(ex, by + 186, "ngân sách", fill=MUTED, bold=True)
c.text(ex, by + 252, f"{BUDGET} nhãn", size=52, bold=True)

# Câu hỏi
c.text(W / 2, H - 6, f"Chọn {BUDGET} ảnh nào để gán nhãn?", size=34, bold=True, fill=BRAND)

c.front.insert(0, "<defs>" + "".join(clips) + "</defs>")
print(c.svg(), end="")

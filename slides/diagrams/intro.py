"""Sơ đồ Phần I (Giới thiệu), theo mục "Mở đầu" của báo cáo:
  python3 intro.py loss > intro-loss.svg          bệnh trên lá gây mất mùa
  python3 intro.py diagnose > intro-diagnose.svg  ba cách chẩn đoán
  python3 intro.py gap > intro-gap.svg            phòng thí nghiệm khác thực địa
  python3 intro.py loop > intro-loop.svg          học tiếp từ ảnh thực tế
  python3 intro.py goals > intro-goals.svg        ba phần của luận văn

Ảnh nhúng thẳng vào SVG (data URI). SVG đặt trên slide ở tỉ lệ 1:1 (rộng 1160).
Trích dẫn không vẽ ở đây: slide đặt chúng ở chân trang (footer).
"""
import base64
import io
import sys
from pathlib import Path

from PIL import Image, ImageOps

from svgkit import Canvas, INK, MUTED, FAINT, STYLE, esc

MODE = sys.argv[1] if len(sys.argv) > 1 else "loss"
HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"
BRAND, RED = "#1e5631", "#cf222e"
clips = []


def uri(im, quality=80):
    buf = io.BytesIO()
    im.convert("RGB").save(buf, "JPEG", quality=quality)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def photo(c, x, y, w, h, path, centering=(0.5, 0.5), rx=14, scale=2):
    im = ImageOps.fit(Image.open(path).convert("RGB"), (w * scale, h * scale), Image.LANCZOS, centering=centering)
    cid = f"c{len(clips)}"
    clips.append(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/></clipPath>')
    c.front.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="{uri(im)}" '
                   f'clip-path="url(#{cid})" preserveAspectRatio="xMidYMid slice"/>')


def _tmp(im):
    buf = io.BytesIO()
    im.convert("RGB").save(buf, "PNG")
    buf.seek(0)
    return buf


def done(c):
    out = c.svg()
    if clips:
        out = out.replace("<defs>", "<defs>" + "".join(clips), 1)
    print(out, end="")


# ---------------------------------------------------------------- loss
if MODE == "loss":
    c = Canvas(1160, 500)
    photo(c, 0, 0, 560, 500, ASSETS / "intro/coffee-rust.jpg", centering=(0.45, 0.5))
    c.text(14, 488, "Gỉ sắt trên lá cà phê (Wikimedia Commons)", size=16, fill="#ffffff", anchor="start")
    STATS = [
        ("30% · 21,5%", "sản lượng lúa gạo · lúa mì mất do bệnh hại", "toàn cầu [1]"),
        ("16–34%", "năng suất cà phê giảm do gỉ sắt", "Tây Bắc [6]"),
        ("20–30%", "diện tích sầu riêng bị cháy lá", "Cái Bè, Tiền Giang, 2024 [7]"),
    ]
    for i, (num, line, where) in enumerate(STATS):
        y = 70 + i * 160
        c.text(610, y, num, size=60, bold=True, fill=RED, anchor="start")
        c.text(610, y + 40, line, anchor="start")
        c.text(610, y + 70, where, size=20, fill=MUTED, anchor="start")
    done(c)

# ---------------------------------------------------------------- diagnose
elif MODE == "diagnose":
    c = Canvas(1160, 500)
    CW, GAP, TOP = 360, 40, 0
    xs = [i * (CW + GAP) for i in range(3)]
    cards = [
        ("Nhìn bằng mắt", ["Cần chuyên gia", "Bệnh giống nhau dễ nhầm"], RED),
        ("Phòng thí nghiệm", ["Chính xác", "Đắt, không làm tại vườn"], RED),
        ("Điện thoại + mô hình", ["Chụp là biết, ngay tại vườn", "Không cần mạng [8], [9]"], BRAND),
    ]
    for x, (title, lines, color) in zip(xs, cards):
        c.back.append(f'<rect x="{x}" y="{TOP}" width="{CW}" height="490" rx="14" fill="#fafbfc" stroke="{FAINT}" stroke-width="1.5"/>')
        cx, cy = x + CW / 2, TOP + 150
        c.text(cx, TOP + 330, title, size=26, bold=True)
        for j, s in enumerate(lines):
            mark = "✓" if (color == BRAND or j == 0 and title == "Phòng thí nghiệm") else "✗"
            col = BRAND if mark == "✓" else RED
            c.text(x + 34, TOP + 386 + j * 40, mark, bold=True, fill=col, anchor="start")
            c.text(x + 64, TOP + 386 + j * 40, s, anchor="start")
    # Mắt và lá
    cx, cy = xs[0] + CW / 2, TOP + 150
    c.front.append(f'<path d="M{cx - 120},{cy} Q{cx},{cy - 100} {cx + 120},{cy} Q{cx},{cy + 100} {cx - 120},{cy} Z" fill="#ffffff" stroke="{INK}" stroke-width="5"/>')
    c.front.append(f'<circle cx="{cx}" cy="{cy}" r="38" fill="#2f7d4f"/><circle cx="{cx}" cy="{cy}" r="16" fill="{INK}"/>')
    c.front.append(f'<circle cx="{cx + 10}" cy="{cy - 10}" r="6" fill="#ffffff"/>')
    # Bình thí nghiệm và kính hiển vi đơn giản
    cx = xs[1] + CW / 2
    c.front.append(f'<path d="M{cx - 30},{cy - 100} h60 v70 l60,110 a14,14 0 0 1 -12,20 h-156 a14,14 0 0 1 -12,-20 l60,-110 Z" '
                   f'fill="#ffffff" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    c.front.append(f'<path d="M{cx - 73},{cy + 45} h146 l22,40 a10,10 0 0 1 -9,15 h-172 a10,10 0 0 1 -9,-15 Z" fill="#e7f0fd" stroke="none"/>')
    c.front.append(f'<line x1="{cx - 44}" y1="{cy - 100}" x2="{cx + 44}" y2="{cy - 100}" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>')
    for dx, dy, r in ((-20, 70, 7), (12, 55, 5), (30, 78, 6)):
        c.front.append(f'<circle cx="{cx + dx}" cy="{cy + dy}" r="{r}" fill="#2563eb"/>')
    # Điện thoại với ảnh chụp màn hình kết quả
    pw, ph = 120, 240
    px, py = xs[2] + CW / 2 - pw / 2, TOP + 30
    c.front.append(f'<rect x="{px - 8}" y="{py - 8}" width="{pw + 16}" height="{ph + 16}" rx="20" fill="{INK}"/>')
    shot = Image.open(ASSETS / "demo/07-ket-qua.png")
    photo(c, px, py, pw, ph, _tmp(shot.crop((0, 0, shot.width, int(shot.width * ph / pw)))), rx=12, scale=3)
    done(c)

# ---------------------------------------------------------------- gap
elif MODE == "gap":
    c = Canvas(1160, 500)
    # Trái: cùng một mô hình, hai loại ảnh
    c.text(0, 28, "Cùng một mô hình [8]", bold=True, anchor="start")
    c.box("lab", 0, 56, 400, 150, ["", ""], cls="ext")
    c.text(200, 120, "99,35%", size=56, bold=True, fill=BRAND)
    c.text(200, 168, "ảnh phòng thí nghiệm", size=22, fill=INK)
    c.box("field", 0, 290, 400, 150, ["", ""], cls="adm")
    c.text(200, 354, "≈ 31%", size=56, bold=True, fill=RED)
    c.text(200, 402, "ảnh từ nguồn khác", size=22, fill=INK)
    c.arrow(("lab", "b"), ("field", "t"))
    c.text(214, 256, "đổi nguồn ảnh", size=20, fill=MUTED, anchor="start")
    # Phải: số ảnh có nhãn
    c.text(480, 28, "Số ảnh lá có nhãn", bold=True, anchor="start")
    ROWS = [("PlantVillage", "phòng thí nghiệm", 54306, FAINT),
            ("Sầu riêng", "thực địa, Việt Nam [14]", 2595, BRAND),
            ("RoCoLe", "thực địa, Ecuador [11]", 1560, "#2f7d4f")]
    BX, BMAX = 700, 330
    for i, (name, desc, n, color) in enumerate(ROWS):
        y = 70 + i * 120
        c.text(BX - 16, y + 24, name, bold=True, anchor="end")
        c.text(BX - 16, y + 52, desc, size=18, fill=MUTED, anchor="end")
        w = max(6, BMAX * n / ROWS[0][2])
        c.front.append(f'<rect x="{BX}" y="{y + 6}" width="{w:.1f}" height="42" rx="6" fill="{color}"/>')
        c.text(BX + w + 12, y + 38, f"{n:,}".replace(",", "."), size=28, bold=True, anchor="start",
               fill=MUTED if i == 0 else INK)
    c.box("take", 480, 410, 676, 70, "Ảnh thực địa có nhãn: ít hơn 20 đến 35 lần", cls="key", bold=True)
    done(c)

# ---------------------------------------------------------------- loop
elif MODE == "loop":
    c = Canvas(1160, 500)
    BW, BH = 250, 76
    NODES = [  # key, x, y, chữ, kiểu
        ("app", 40, 40, ["Điện thoại", "gửi ảnh mới"], "app"),
        ("pool", 455, 40, ["Kho ảnh", "chưa có nhãn"], "sys"),
        ("pick", 870, 40, ["Chọn ảnh “đáng” gán", "(học chủ động)"], "key"),
        ("label", 870, 300, ["Chuyên gia", "gán nhãn"], "lab"),
        ("train", 455, 300, ["Huấn luyện lại", "mô hình"], "mle"),
        ("rel", 40, 300, ["Phát hành", "mô hình mới"], "sys"),
    ]
    for k, x, y, lines, cls in NODES:
        c.box(k, x, y, BW, BH, lines, cls=cls, bold=(k == "pick"))
    c.arrow(("app", "r"), ("pool", "l"))
    c.arrow(("pool", "r"), ("pick", "l"))
    c.arrow(("pick", "b"), ("label", "t"))
    c.arrow(("label", "l"), ("train", "r"))
    c.arrow(("train", "l"), ("rel", "r"))
    c.arrow(("rel", "t"), ("app", "b"))
    c.text(580, 222, "lặp lại liên tục", size=24, fill=MUTED)
    c.back.append(f'<rect x="20" y="20" width="1120" height="376" rx="18" fill="none" stroke="{BRAND}" stroke-width="2" stroke-dasharray="8 6"/>')
    c.text(580, 446, "MLOps: tự động hoá cả vòng lặp [13]", size=26, bold=True, fill=BRAND)
    c.text(580, 482, "Học chủ động: bớt số ảnh chuyên gia phải gán", size=22, fill=MUTED)
    done(c)

# ---------------------------------------------------------------- goals
elif MODE == "goals":
    c = Canvas(1160, 500)
    CW, GAP, TOP, CH = 336, 72, 2, 380
    PARTS = [
        ("II", "Đánh giá mô hình", ["Mô hình nào chạy tốt", "trên điện thoại?"], "mle"),
        ("III", "Mô phỏng học chủ động", ["Chọn ảnh có hơn", "chọn ngẫu nhiên?"], "lab"),
        ("IV", "Nền tảng MLOps", ["Nối chọn ảnh, gán nhãn,", "huấn luyện, phát hành"], "sys"),
    ]
    for i, (num, title, q, cls) in enumerate(PARTS):
        x = 2 + i * (CW + GAP)
        fill, stroke = STYLE[cls]
        c.back.append(f'<rect x="{x}" y="{TOP}" width="{CW}" height="{CH}" rx="16" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>')
        c.text(x + CW / 2, TOP + 80, f"Phần {num}", size=40, bold=True, fill=stroke)
        c.text(x + CW / 2, TOP + 140, title, size=26, bold=True)
        cy = TOP + 250
        # Biểu tượng nhỏ cho từng phần
        if num == "II":
            for j, hgt in enumerate((40, 70, 55, 90)):
                c.front.append(f'<rect x="{x + CW / 2 - 70 + j * 36}" y="{cy + 40 - hgt}" width="26" height="{hgt}" rx="4" fill="{stroke}" opacity="{0.45 + 0.15 * j}"/>')
        elif num == "III":
            for j in range(12):
                r, col = divmod(j, 4)
                on = j in (1, 6, 11)
                c.front.append(f'<rect x="{x + CW / 2 - 76 + col * 40}" y="{cy - 50 + r * 34}" width="32" height="26" rx="4" '
                               f'fill="{stroke if on else "#ffffff"}" stroke="{stroke}" stroke-width="2"/>')
        else:
            c.front.append(f'<circle cx="{x + CW / 2}" cy="{cy - 6}" r="46" fill="none" stroke="{stroke}" stroke-width="7" stroke-dasharray="230 60"/>')
            c.front.append(f'<path d="M{x + CW / 2 + 40},{cy - 40} l16,-2 l-6,18 z" fill="{stroke}"/>')
        c.text(x + CW / 2, TOP + 326, q[0], size=22)
        c.text(x + CW / 2, TOP + 354, q[1], size=22)
    # Mũi tên nối và thứ được chuyển sang phần sau
    for i, label in enumerate(("mô hình đã chọn", "chiến lược chọn ảnh")):
        x0 = 2 + (i + 1) * CW + i * GAP
        c.arrow((x0 + 6, TOP + CH / 2), (x0 + GAP - 6, TOP + CH / 2))
        c.text(x0 + GAP / 2, TOP + CH + 46, label, size=20, fill=MUTED)
        c.front.append(f'<line x1="{x0 + GAP / 2}" y1="{TOP + CH / 2 + 10}" x2="{x0 + GAP / 2}" y2="{TOP + CH + 22}" stroke="{FAINT}" stroke-width="1.5" stroke-dasharray="4 4"/>')
    c.text(580, 492, "Một hệ thống chẩn đoán bệnh lá cà phê và sầu riêng, học tiếp từ ảnh thực tế", size=22, bold=True, fill=BRAND)
    done(c)

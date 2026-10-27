"""Sơ đồ Phần II (Đánh giá mô hình), số liệu theo báo cáo (mục 2.2, 2.3.1, 3.1):
  python3 bench.py data > bench-data.svg          ảnh mẫu từng lớp
  python3 bench.py balance > bench-balance.svg    hai biểu đồ tròn tỉ lệ lớp
  python3 bench.py models > bench-models.svg      tám mô hình, ba họ
  python3 bench.py lpft > bench-lpft.svg          LP-FT và siêu tham số
  python3 bench.py tuning > bench-tuning.svg      vòng tinh chỉnh, ví dụ DeiT-Tiny
  python3 bench.py metrics > bench-metrics.svg    chỉ số đánh giá trên ví dụ DeiT-Tiny
  python3 bench.py eval > bench-eval.svg          chia dữ liệu và đánh giá
  python3 bench.py choose > bench-choose.svg      độ chính xác và độ trễ

Ảnh mẫu đọc từ /mnt/project-files/presentation/samples/ hoặc slides/assets/samples/;
thiếu ảnh thì vẽ ô xám có tên lớp. SVG đặt trên slide ở tỉ lệ 1:1 (rộng 1160).
"""
import base64
import io
import math
import sys
from pathlib import Path

from PIL import Image, ImageOps

from svgkit import Canvas, INK, MUTED, FAINT, STYLE

MODE = sys.argv[1] if len(sys.argv) > 1 else "data"
HERE = Path(__file__).resolve().parent
SAMPLES = [HERE.parent / "assets/samples", Path("/mnt/project-files/presentation/samples")]
BRAND, RED = "#1e5631", "#cf222e"
FAM = {"CNN": "#2563eb", "ViT": "#bf8700", "Hybrid": "#2f7d4f"}  # màu theo họ kiến trúc
clips = []

ROCOLE = [("Lá khoẻ", "healthy", 791), ("Nhện đỏ", "mite", 167), ("Gỉ sắt", "rust", 602)]
DURIAN = [("Algal", "algal", 462), ("Blight", "blight", 440), ("Colletotrichum", "colletotrichum", 400),
          ("Healthy", "healthy", 484), ("Phomopsis", "phomopsis", 411), ("Rhizoctonia", "rhizoctonia", 398)]
# tên, họ, tham số (triệu), F1 RoCoLe, CI, F1 sầu riêng, CI, ONNX MB, độ trễ 6 luồng (ms)
MODELS = [
    ("MobileNetV3-L", "CNN", 4.2, .677, (.603, .750), .935, (.908, .958), 16.2, 2.2),
    ("MobileNetV4-Conv-M", "CNN", 8.4, .753, (.666, .826), .942, (.917, .964), 32.3, 6.7),
    ("EfficientNetV2-S", "CNN", 20.2, .672, (.601, .746), .953, (.930, .972), 77.2, 34.8),
    ("ConvNeXt-T", "CNN", 27.8, .751, (.668, .828), .960, (.940, .978), 106.5, 36.4),
    ("DeiT-Tiny", "ViT", 5.5, .800, (.725, .865), .960, (.939, .978), 21.6, 11.2),
    ("Swin-T", "ViT", 27.5, .816, (.736, .888), .965, (.945, .981), 108.1, 41.3),
    ("MobileViTv2-0.75", "Hybrid", 2.5, .762, (.672, .843), .940, (.915, .962), 10.1, 9.9),
    ("FastViT-T8", "Hybrid", 3.3, .751, (.665, .830), .946, (.922, .967), 12.6, 7.8),
]


def vn(x, d=3):
    return f"{x:.{d}f}".replace(".", ",")


def uri(im):
    buf = io.BytesIO()
    im.convert("RGB").save(buf, "JPEG", quality=80)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def sample(c, x, y, w, h, name, label):
    for d in SAMPLES:
        f = d / f"{name}.jpg"
        if f.exists():
            im = ImageOps.fit(Image.open(f).convert("RGB"), (w * 2, h * 2), Image.LANCZOS)
            cid = f"c{len(clips)}"
            clips.append(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/></clipPath>')
            c.front.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="{uri(im)}" clip-path="url(#{cid})" '
                           f'preserveAspectRatio="xMidYMid slice"/>')
            return
    c.front.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#e4e7eb"/>')
    c.text(x + w / 2, y + h / 2, f"ảnh {label}", size=18, fill=MUTED)


def done(c):
    out = c.svg()
    if clips:
        out = out.replace("<defs>", "<defs>" + "".join(clips), 1)
    print(out, end="")


def pie(c, cx, cy, r, parts, colors, hole=0.55):
    total = sum(n for _, n in parts)
    a = -math.pi / 2
    for (label, n), col in zip(parts, colors):
        b = a + 2 * math.pi * n / total
        large = 1 if b - a > math.pi else 0
        x1, y1, x2, y2 = cx + r * math.cos(a), cy + r * math.sin(a), cx + r * math.cos(b), cy + r * math.sin(b)
        c.front.append(f'<path d="M{cx},{cy} L{x1:.1f},{y1:.1f} A{r},{r} 0 {large} 1 {x2:.1f},{y2:.1f} Z" fill="{col}" stroke="#ffffff" stroke-width="3"/>')
        m = (a + b) / 2
        lx, ly = cx + (r + 26) * math.cos(m), cy + (r + 26) * math.sin(m)
        anchor = "start" if math.cos(m) > 0.15 else ("end" if math.cos(m) < -0.15 else "middle")
        c.text(lx, ly - 2, label, size=20, anchor=anchor, bold=True)
        c.text(lx, ly + 22, f"{n} · {vn(100 * n / total, 1)}%", size=18, fill=MUTED, anchor=anchor)
        a = b
    c.front.append(f'<circle cx="{cx}" cy="{cy}" r="{r * hole}" fill="#ffffff"/>')


# ---------------------------------------------------------------- data
if MODE == "data":
    c = Canvas(1160, 500)
    c.text(0, 26, "RoCoLe: cà phê Robusta, Ecuador · 1.560 ảnh · 3 lớp", bold=True, anchor="start")
    W1 = 250
    for i, (label, key, n) in enumerate(ROCOLE):
        x = i * (W1 + 20)
        sample(c, x, 44, W1, 170, f"rocole-{key}", label)
        c.text(x + W1 / 2, 244, f"{label} · {n}", size=20, bold=key == "mite", fill=RED if key == "mite" else INK)
    c.text(0, 300, "Sầu riêng: Bình Phước, Tiền Giang · 2.595 ảnh · 6 lớp", bold=True, anchor="start")
    W2 = 178
    for i, (label, key, n) in enumerate(DURIAN):
        x = i * (W2 + 18)
        sample(c, x, 318, W2, 130, f"durian-{key}", label)
        c.text(x + W2 / 2, 476, f"{label} · {n}", size=18)
    done(c)

# ---------------------------------------------------------------- balance
elif MODE == "balance":
    c = Canvas(1160, 500)
    c.text(290, 30, "RoCoLe: lệch", bold=True, size=26)
    pie(c, 290, 250, 150, [(l, n) for l, _, n in ROCOLE], ["#2f7d4f", RED, "#bf8700"])
    c.text(290, 258, "1.560", size=30, bold=True)
    c.text(870, 30, "Sầu riêng: cân bằng", bold=True, size=26)
    pie(c, 870, 250, 150, [(l, n) for l, _, n in DURIAN], ["#2f7d4f", "#bf8700", "#8250df", "#2563eb", "#9aa5b1", "#cf6b2e"])
    c.text(870, 258, "2.595", size=30, bold=True)
    c.front.append(f'<line x1="580" y1="20" x2="580" y2="440" stroke="{FAINT}" stroke-width="1.5"/>')
    c.text(290, 486, "Nhện đỏ chỉ 10,7%: lớp khó học nhất", size=22, fill=RED, bold=True)
    c.text(870, 486, "Mỗi lớp 15–19%", size=22, fill=MUTED)
    done(c)

# ---------------------------------------------------------------- models
elif MODE == "models":
    c = Canvas(1160, 340)
    COLS = [("CNN", "CNN", 0, 520), ("ViT", "ViT", 560, 280), ("Hybrid", "Hybrid", 880, 280)]
    for fam, title, x, w in COLS:
        col = FAM[fam]
        c.back.append(f'<rect x="{x}" y="0" width="{w}" height="292" rx="16" fill="#fafbfc" stroke="{col}" stroke-width="2"/>')
        c.text(x + w / 2, 38, title, bold=True, fill=col, size=24)
        ms = [m for m in MODELS if m[1] == fam]
        step = w / len(ms)
        for j, m in enumerate(ms):
            cx = x + step * (j + 0.5)
            r = 12 + 6.5 * math.sqrt(m[2])
            c.front.append(f'<circle cx="{cx:.0f}" cy="140" r="{r:.0f}" fill="{col}" opacity="0.85"/>')
            c.text(cx, 146, f"{vn(m[2], 1)}M", size=16 if r < 34 else 20, bold=True, fill="#ffffff")
            name = m[0].replace("MobileNetV4-Conv-M", "MobileNetV4|Conv-M").replace("EfficientNetV2-S", "EfficientNet|V2-S") \
                       .replace("MobileViTv2-0.75", "MobileViTv2|0.75").replace("MobileNetV3-L", "MobileNet|V3-L")
            for k, part in enumerate(name.split("|")):
                c.text(cx, 236 + k * 24, part, size=20)
    c.text(580, 328, "Cùng tải trọng số ImageNet-1k · kích thước hình tròn = số tham số (triệu)", size=20, fill=MUTED)
    done(c)

# ---------------------------------------------------------------- lpft
elif MODE == "lpft":
    c = Canvas(1160, 500)

    def net(x, y, frozen, label):
        """Khối mô hình: thân (backbone) + đầu phân loại (head)."""
        fill = "#e4e7eb" if frozen else STYLE["mle"][0]
        stroke = MUTED if frozen else STYLE["mle"][1]
        c.front.append(f'<rect x="{x}" y="{y}" width="230" height="150" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        c.text(x + 115, y + 70, "Thân mô hình", bold=True)
        c.text(x + 115, y + 100, "đóng băng" if frozen else "cập nhật, LR nhỏ", size=20, fill=MUTED)
        c.front.append(f'<rect x="{x + 240}" y="{y + 35}" width="90" height="80" rx="10" fill="{STYLE["key"][0]}"/>')
        c.text(x + 285, y + 82, "Đầu", bold=True, fill="#ffffff")
        c.text(x + 165, y - 16, label, bold=True, size=24)

    net(0, 70, True, "1. Linear Probing (3 epoch)")
    c.text(165, 262, "chỉ học lớp phân loại mới,", size=20, fill=MUTED)
    c.text(165, 288, "LR 10⁻³", size=20, fill=MUTED)
    c.arrow((345, 145), (395, 145))
    net(410, 70, False, "2. Fine-Tuning (≤ 50 epoch)")
    c.text(575, 262, "mở toàn bộ, LR thấp,", size=20, fill=MUTED)
    c.text(575, 288, "tầng gần đầu vào học chậm hơn", size=20, fill=MUTED)
    c.text(370, 356, "Đầu đã học trước, nên không làm hỏng đặc trưng có sẵn [41]", size=20, fill=BRAND, bold=True)
    # Siêu tham số dùng chung
    X, Y = 790, 0
    c.back.append(f'<rect x="{X}" y="{Y}" width="370" height="446" rx="14" fill="#fafbfc" stroke="{FAINT}" stroke-width="1.5"/>')
    c.text(X + 20, Y + 38, "Siêu tham số chung", bold=True, anchor="start")
    ROWS = [("Bộ tối ưu", "AdamW"), ("Tốc độ học (LR)", "10⁻⁴, tinh chỉnh"), ("Suy giảm trọng số", "0,05"),
            ("Epoch tối đa", "50"), ("Dừng sớm", "sau 15 epoch"), ("Batch", "32, cố định"),
            ("Hàm mất mát", "cross-entropy"), ("Tăng cường ảnh", "cắt, lật, xoay, màu")]
    for i, (k, v) in enumerate(ROWS):
        y = Y + 88 + i * 45
        c.text(X + 20, y, k, size=20, fill=MUTED, anchor="start")
        c.text(X + 350, y, v, size=20, bold=True, anchor="end")
    done(c)

# ---------------------------------------------------------------- tuning
elif MODE == "tuning":
    c = Canvas(1160, 530)
    # Vòng tinh chỉnh
    STEPS = [("run", "Huấn luyện", "3 fold", "mle"), ("read", "Đọc đường học", "train và val", "sys"),
             ("diag", "Chẩn đoán", "", "lab"), ("fix", "Chỉnh 1–2 tham số", "theo bảng", "adm")]
    pos = [(0, 0), (250, 0), (250, 150), (0, 150)]
    for (k, t, s, cls), (x, y) in zip(STEPS, pos):
        c.box(k, x, y, 200, 90, [t, s] if s else [t], cls=cls)
    c.arrow(("run", "r"), ("read", "l"))
    c.arrow(("read", "b"), ("diag", "t"))
    c.arrow(("diag", "l"), ("fix", "r"))
    c.arrow(("fix", "t"), ("run", "b"))
    c.text(225, 135, "≤ 5 vòng", size=20, fill=MUTED)
    RULES = [("Underfitting", "tăng LR ×3", RED), ("Overfitting", "tăng weight decay, drop path; rồi giảm LR", "#bf8700"),
             ("Dao động", "giảm LR", MUTED), ("Tốt", "dừng", BRAND)]
    for i, (d, act, col) in enumerate(RULES):
        y = 290 + i * 46
        c.text(0, y, d, bold=True, fill=col, size=20, anchor="start")
        c.text(130, y, act, size=20, anchor="start")
    c.text(0, 492, "Chọn vòng có F1 trên tập đánh giá cao nhất", size=20, bold=True, fill=BRAND, anchor="start")
    # Ví dụ DeiT-Tiny trên RoCoLe
    X0, Y0, H0 = 560, 60, 330
    c.text(X0, 26, "Ví dụ: DeiT-Tiny trên RoCoLe", bold=True, anchor="start")
    R = [(.765, "overfitting", "LR 10⁻⁴"), (.799, "underfitting", "WD 0,1"), (.799, "overfitting", "LR 3·10⁻⁴"),
         (.774, "overfitting", "LR 1,5·10⁻⁴"), (.755, "overfitting", "LR 7,5·10⁻⁵")]
    LO, HI = .70, .82
    for i, (f1, d, hp) in enumerate(R):
        x = X0 + 10 + i * 118
        h = H0 * (f1 - LO) / (HI - LO)
        best = i == 2
        c.front.append(f'<rect x="{x}" y="{Y0 + H0 - h:.0f}" width="80" height="{h:.0f}" rx="6" fill="{BRAND if best else FAINT}"/>')
        c.text(x + 40, Y0 + H0 - h - 10, vn(f1), size=20, bold=True, fill=BRAND if best else INK)
        c.text(x + 40, Y0 + H0 + 28, f"Vòng {i + 1}", size=20, bold=best)
        c.text(x + 40, Y0 + H0 + 54, hp, size=16, fill=MUTED)
        c.text(x + 40, Y0 + H0 + 76, d, size=16, fill=MUTED)
    c.text(X0 + 300, 522, "Sầu riêng: cả 8 mô hình “tốt” ngay vòng 1", size=20, fill=MUTED)
    done(c)

# ---------------------------------------------------------------- eval
elif MODE == "eval":
    c = Canvas(1160, 500)
    # Dải dữ liệu: test giữ riêng, phần còn lại chia 5 phần
    X, Y, WTOT, HB = 0, 40, 1160, 64
    tw = 0.15 * WTOT
    c.text(0, 24, "Chia theo nhóm (cây, lá): ảnh của cùng một nhóm không nằm ở hai phía", size=20, fill=MUTED, anchor="start")
    c.front.append(f'<rect x="{X}" y="{Y}" width="{tw:.0f}" height="{HB}" rx="8" fill="{STYLE["adm"][0]}" stroke="{STYLE["adm"][1]}" stroke-width="2"/>')
    c.text(X + tw / 2, Y + 40, "Kiểm thử", bold=True)
    fw = (WTOT - tw - 10) / 5
    for k in range(5):
        x = X + tw + 10 + k * fw
        c.front.append(f'<rect x="{x:.0f}" y="{Y}" width="{fw - 6:.0f}" height="{HB}" rx="8" fill="{STYLE["sys"][0]}" stroke="{STYLE["sys"][1]}" stroke-width="2"/>')
        c.text(x + fw / 2 - 3, Y + 40, f"Phần {k + 1}")
    # 5 lần huấn luyện
    for k in range(5):
        y = 150 + k * 38
        c.text(0, y + 22, f"Mô hình {k + 1}", size=20, anchor="start")
        for j in range(5):
            x = X + tw + 10 + j * fw
            val = j == k
            c.front.append(f'<rect x="{x:.0f}" y="{y}" width="{fw - 6:.0f}" height="30" rx="6" fill="{STYLE["lab"][1] if val else STYLE["mle"][0]}"/>')
            if val:
                c.text(x + fw / 2 - 3, y + 22, "đánh giá", size=18, fill="#ffffff", bold=True)
    c.text(X + tw + 10 + 2.5 * fw, 362, "4 phần huấn luyện, 1 phần đánh giá (dừng sớm, chọn epoch)", size=20, fill=MUTED)
    c.box("ens", 0, 400, 360, 90, ["Gộp 5 mô hình", "(trung bình xác suất)"], cls="mle")
    c.box("test", 420, 400, 300, 90, ["Chấm trên tập", "kiểm thử, một lần"], cls="adm")
    c.box("ci", 780, 400, 380, 90, ["Bootstrap 2.000 lần", "→ khoảng tin cậy 95%"], cls="key", bold=True)
    c.arrow(("ens", "r"), ("test", "l"))
    c.arrow(("test", "r"), ("ci", "l"))
    done(c)

# ---------------------------------------------------------------- choose
elif MODE == "metrics":
    # DeiT-Tiny, tập kiểm thử RoCoLe (repeat 0, gộp 5 fold), hàng = nhãn thật, cột = dự đoán
    # nguồn: research/benchmark-raw/data-and-results.md, mục Test confusion matrices
    c = Canvas(1160, 486)
    NAMES = ["Lá khoẻ", "Nhện đỏ", "Gỉ sắt"]
    CM = [[119, 2, 2], [2, 12, 8], [1, 8, 72]]
    n = sum(map(sum, CM))
    X0, Y0, CW, CH = 120, 96, 104, 64
    c.text(X0 + 1.5 * CW, 40, "Mô hình dự đoán", size=20, fill=MUTED)
    c.text(0, Y0 - 16, "Nhãn thật", size=20, fill=MUTED, anchor="start")
    for j, name in enumerate(NAMES):
        c.text(X0 + j * CW + CW / 2, 76, name, size=18, bold=True)
    for i, name in enumerate(NAMES):
        y = Y0 + i * CH
        c.text(X0 - 12, y + CH / 2 + 7, name, size=20, bold=True, anchor="end", fill=RED if i == 1 else INK)
        for j in range(3):
            fill = STYLE["sys"][0] if i == j else "#ffffff"
            c.front.append(f'<rect x="{X0 + j * CW}" y="{y}" width="{CW}" height="{CH}" fill="{fill}" stroke="{FAINT}" stroke-width="1.5"/>')
            c.text(X0 + j * CW + CW / 2, y + CH / 2 + 8, str(CM[i][j]), size=24, bold=i == j,
                   fill=RED if (i == 1 and j != 1) else INK)
    c.front.append(f'<rect x="{X0 - 2}" y="{Y0 + CH - 2}" width="{3 * CW + 4}" height="{CH + 4}" fill="none" stroke="{RED}" stroke-width="3"/>')
    # bảng theo lớp
    TX = [560, 760, 910, 1060]
    for x, head, sub in [(TX[1], "Precision", ["đoán là lớp đó,", "đúng bao nhiêu"]),
                         (TX[2] + 10, "Recall", ["ảnh thật của lớp,", "tìm ra bao nhiêu"]),
                         (TX[3] + 20, "F1", ["cân bằng", "hai số"])]:
        c.text(x, 24, head, bold=True)
        for k, t in enumerate(sub):
            c.text(x, 50 + k * 22, t, size=18, fill=MUTED)
    f1s = []
    for i, name in enumerate(NAMES):
        tp = CM[i][i]
        fp = sum(CM[k][i] for k in range(3)) - tp
        fn = sum(CM[i]) - tp
        pr, rc = tp / (tp + fp), tp / (tp + fn)
        f1 = 2 * tp / (2 * tp + fp + fn)
        f1s.append(f1)
        y = Y0 + i * CH + CH / 2 + 8
        col = RED if i == 1 else INK
        c.text(TX[0], y, name, bold=True, anchor="start", fill=col)
        c.text(TX[1], y, vn(pr), fill=col)
        c.text(TX[2] + 10, y, vn(rc), fill=col)
        c.text(TX[3] + 20, y, vn(f1), bold=True, fill=col)
    c.front.append(f'<line x1="{TX[0]}" y1="{Y0}" x2="1160" y2="{Y0}" stroke="{FAINT}" stroke-width="1.5"/>')
    macro = sum(f1s) / 3
    acc = sum(CM[i][i] for i in range(3)) / n
    assert abs(macro - .800) < .001 and abs(acc - .898) < .001
    c.box("mf", 0, 330, 560, 96, [f"Macro-F1 = trung bình F1 ba lớp = {vn(macro)}"], cls="key", bold=True)
    c.box("acc", 600, 330, 560, 96, [f"Accuracy = {sum(CM[i][i] for i in range(3))}/{n} ảnh đúng = {vn(acc)}"], cls="sys")
    c.text(280, 464, "mỗi lớp nặng như nhau: lớp nhện đỏ kéo điểm xuống", size=19, fill=MUTED)
    c.text(880, 464, "lá khoẻ nhiều ảnh nên che lỗi lớp nhện đỏ", size=19, fill=MUTED)
    done(c)

elif MODE == "choose":
    c = Canvas(1160, 500)
    X0, X1, Y0, Y1 = 90, 1120, 30, 400
    LMAX, FLO, FHI = 45, .65, .84

    def px(ms):
        return X0 + (X1 - X0) * ms / LMAX

    def py(f):
        return Y1 - (Y1 - Y0) * (f - FLO) / (FHI - FLO)

    for f in (.65, .70, .75, .80):
        c.back.append(f'<line x1="{X0}" y1="{py(f):.0f}" x2="{X1}" y2="{py(f):.0f}" stroke="#e4e7eb" stroke-width="1"/>')
        c.text(X0 - 12, py(f) + 6, vn(f, 2), size=18, fill=MUTED, anchor="end")
    for ms in (0, 10, 20, 30, 40):
        c.text(px(ms), Y1 + 28, str(ms), size=18, fill=MUTED)
    c.front.append(f'<line x1="{X0}" y1="{Y1}" x2="{X1}" y2="{Y1}" stroke="{MUTED}" stroke-width="2"/>')
    c.front.append(f'<line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1}" stroke="{MUTED}" stroke-width="2"/>')
    c.text((X0 + X1) / 2, Y1 + 60, "Độ trễ trên CPU (ms/ảnh, ONNX, 6 luồng) → càng trái càng nhanh", size=20, fill=MUTED)
    c.text(X0 - 70, Y0 - 8, "Macro-F1 RoCoLe", size=18, fill=MUTED, anchor="start")
    OFF = {"MobileNetV4-Conv-M": (-10, 46, "middle"), "FastViT-T8": (14, 8, "start"), "MobileViTv2-0.75": (14, -10, "start"),
           "ConvNeXt-T": (0, -42, "middle"), "EfficientNetV2-S": (-14, 6, "end"), "Swin-T": (-10, -36, "end"),
           "MobileNetV3-L": (14, 6, "start"), "DeiT-Tiny": (18, 26, "start")}
    for name, fam, p, f1, ci, *_ , mb, lat in MODELS:
        x, y = px(lat), py(f1)
        r = 8 + 2.4 * math.sqrt(mb)
        pick = name == "DeiT-Tiny"
        c.front.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="{FAM[fam]}" opacity="0.8" '
                       f'stroke="{BRAND if pick else "#ffffff"}" stroke-width="{5 if pick else 1.5}"/>')
        dx, dy, a = OFF[name]
        c.text(x + dx + (r if a == "start" else -r if a == "end" else 0), y + dy, f"{name} ({vn(mb, 0)} MB)", size=18,
               anchor=a, bold=pick, fill=BRAND if pick else INK)
    c.box("pick", 420, 8, 420, 56, "Chọn DeiT-Tiny: chính xác, nhẹ, nhanh", cls="key", bold=True)
    c.arrow(("pick", "b", 0.12), (px(11.2) + 6, py(.800) - 24))
    for i, (fam, label) in enumerate((("CNN", "CNN"), ("ViT", "ViT"), ("Hybrid", "Hybrid"))):
        c.front.append(f'<circle cx="{X0 + 30 + i * 86}" cy="{Y0 + 20}" r="9" fill="{FAM[fam]}"/>')
        c.text(X0 + 45 + i * 86, Y0 + 27, label, size=18, anchor="start")
    done(c)

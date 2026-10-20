"""Kết quả giả lập học chủ động (phần III):
  python3 al_results.py > al-results.svg

Số liệu từ trang Notion (bảng "Số nhãn cần để đạt ngưỡng" của RoCoLe, "AUBC macro-F1" của sầu riêng).
Trái: mỗi chấm là một lần chạy (seed), tô màu nếu lần đó đạt recall lớp hiếm ≥ 0,70.
Phải: AUBC macro-F1 trung bình ± độ lệch chuẩn trên 5 seed, vẽ chấm vì trục không bắt đầu từ 0.
SVG đặt trên slide ở tỉ lệ 1:1 (rộng 1160).
"""
from svgkit import Canvas, INK, MUTED, FAINT, STYLE

W, H = 1160, 540
BRAND, RED = "#1e5631", "#cf222e"
c = Canvas(W, H)
NAMES = ["Random", "Least confidence", "Margin", "Entropy", "Class-balanced"]
ROW0, ROWH = 128, 46

# Trái: RoCoLe, lớp lệch.
c.zone(0, 0, 560, 420, "RoCoLe: lớp lệch, nhện đỏ hiếm")
c.text(20, 72, "Số lần chạy nhận đúng ≥ 70% ảnh nhện đỏ", size=20, fill=MUTED, anchor="start")
HIT = [0, 1, 1, 2, 2]
for i, (name, hit) in enumerate(zip(NAMES, HIT)):
    y = ROW0 + i * ROWH
    best = hit == max(HIT)
    color = RED if hit == 0 else (BRAND if best else INK)
    c.text(20, y + 8, name, anchor="start", bold=best or hit == 0, fill=color)
    for k in range(5):
        cx = 250 + k * 40
        fill = BRAND if k < hit else "#ffffff"
        c.front.append(f'<circle cx="{cx}" cy="{y}" r="14" fill="{fill}" stroke="{BRAND if k < hit else FAINT}" stroke-width="2"/>')
    c.text(470, y + 8, f"{hit}/5", bold=best or hit == 0, fill=color, anchor="start")
c.text(20, 400, "Điểm chung các lớp gần nhau: 0,738 đến 0,768", size=20, fill=MUTED, anchor="start")

# Phải: sầu riêng, lớp khá cân bằng. Trục 0,92 đến 0,96.
X0, X1, LO, HI = 820, 1130, 0.92, 0.96
AUBC = [(0.9310, 0.0050), (0.9417, 0.0043), (0.9423, 0.0016), (0.9429, 0.0036), (0.9427, 0.0030)]
CEIL = 0.9530


def px(v):
    return X0 + (v - LO) / (HI - LO) * (X1 - X0)


c.zone(600, 0, 560, 420, "Sầu riêng: lớp khá cân bằng")
c.text(620, 72, "Điểm chung các lớp, trung bình 5 lần chạy", size=20, fill=MUTED, anchor="start")
for i, (name, (m, sd)) in enumerate(zip(NAMES, AUBC)):
    y = ROW0 + i * ROWH
    color = RED if i == 0 else INK
    c.text(620, y + 8, name, anchor="start", bold=i == 0, fill=color)
    c.front.append(f'<line x1="{px(m - sd):.1f}" y1="{y}" x2="{px(m + sd):.1f}" y2="{y}" stroke="{FAINT}" stroke-width="4" stroke-linecap="round"/>')
    c.front.append(f'<circle cx="{px(m):.1f}" cy="{y}" r="9" fill="{RED if i == 0 else BRAND}"/>')
top, bot = ROW0 - 26, ROW0 + 4 * ROWH + 22
c.front.append(f'<line x1="{px(CEIL):.1f}" y1="{top}" x2="{px(CEIL):.1f}" y2="{bot}" stroke="{MUTED}" stroke-width="2" stroke-dasharray="6 4"/>')
c.text(px(CEIL), top - 6, "gán hết: 0,953", size=18, fill=MUTED)
for v in (0.92, 0.94, 0.96):
    c.front.append(f'<line x1="{px(v):.1f}" y1="{bot}" x2="{px(v):.1f}" y2="{bot + 6}" stroke="{MUTED}" stroke-width="2"/>')
    c.text(px(v), bot + 28, f"{v:.2f}".replace(".", ","), size=18, fill=MUTED)
c.front.append(f'<line x1="{X0}" y1="{bot}" x2="{X1}" y2="{bot}" stroke="{MUTED}" stroke-width="2"/>')
c.text(620, 400, "Hơn Random khoảng 0,011, ở cả 5 lần chạy", size=20, fill=MUTED, anchor="start")

# Dải kết luận.
c.box("take", 0, 446, 1160, 90, ["Lớp lệch: chọn ảnh giúp bắt được bệnh hiếm.",
                                 "Lớp cân bằng: lợi ít nhưng đều."], cls="key", bold=True)

print(c.svg())

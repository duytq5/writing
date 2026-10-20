"""Thiết lập giả lập học chủ động (phần III):
  python3 al_setup.py > al-setup.svg

Trái: cách chia RoCoLe (số ảnh lấy từ trang Notion, mục "Chia dữ liệu").
Giữa: vòng lặp giả lập, nhãn có sẵn được "mở" thay cho chuyên gia.
Phải: hai chỉ số đo và số lần chạy. SVG đặt trên slide ở tỉ lệ 1:1 (rộng 1160).
"""
from svgkit import Canvas, INK, MUTED, FAINT, STYLE

W, H = 1160, 470
c = Canvas(W, H)

# Cột trái: thanh chồng, chiều cao tỉ lệ số ảnh.
PARTS = [  # (số ảnh, nhãn, màu nền, viền)
    (213, "Kiểm tra: 213", "#f5f7fa", FAINT),
    (184, "Kiểm định: 184", "#f5f7fa", FAINT),
    (107, "Có nhãn sẵn: 107", *STYLE["sys"]),
    (977, "Che nhãn: 977", "#e4e7eb", MUTED),
]
BX, BY, BW, BH = 10, 56, 90, 400
total = sum(p[0] for p in PARTS)
c.text(BX, 30, "RoCoLe, 1.481 ảnh", bold=True, anchor="start")
y = BY
for n, label, fill, stroke in PARTS:
    h = BH * n / total
    c.front.append(f'<rect x="{BX}" y="{y:.1f}" width="{BW}" height="{h:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    c.text(BX + BW + 14, y + h / 2 + 8, label, anchor="start", bold=(n == 977))
    y += h
POOL_MID = y - BH * 977 / total / 2
# Dấu "?" trên phần che nhãn: nhãn có thật nhưng mô hình không được thấy.
for i in range(4):
    c.text(BX + BW / 2, POOL_MID - 75 + i * 50, "?", size=30, fill=MUTED, bold=True)
c.text(BX + BW + 14, POOL_MID + 36, "(nhãn có, nhưng giấu)", size=20, fill=MUTED, anchor="start")

# Giữa: vòng lặp bốn bước theo chiều kim đồng hồ.
L, R, T, B, BOXW, BOXH = 380, 630, 70, 250, 190, 90
c.box("train", L, T, BOXW, BOXH, ["Huấn luyện", "mô hình mới"], cls="mle")
c.box("eval", R, T, BOXW, BOXH, ["Chấm điểm", "trên tập kiểm tra"], cls="sys")
c.box("pick", R, B, BOXW, BOXH, ["Chiến lược", "chọn N ảnh"], cls="key", bold=True)
c.box("open", L, B, BOXW, BOXH, ["Mở nhãn có sẵn", "(thay chuyên gia)"], cls="lab")
c.arrow(("train", "r"), ("eval", "l"))
c.arrow(("eval", "b"), ("pick", "t"))
c.arrow(("pick", "l"), ("open", "r"))
c.arrow(("open", "t"), ("train", "b"))
c.text((L + R + BOXW) / 2, (T + B + BOXH) / 2 + 8, "lặp lại", fill=MUTED)
c.arrow((BX + BW + 200, POOL_MID - 8), ("open", "l", (POOL_MID - 8 - B) / BOXH), dashed=True)
c.text((L + R + BOXW) / 2, B + BOXH + 50, "6 lần chọn: 50, 50, 100, 100, 200, 200 ảnh", size=20, fill=MUTED)
c.text((L + R + BOXW) / 2, B + BOXH + 78, "tổng cộng mở thêm 700 nhãn", size=20, fill=MUTED)

# Phải: đo gì và chạy bao nhiêu lần.
X3, W3 = 870, 286
c.text(X3, 30, "Đo hai điều", bold=True, anchor="start")
c.box("f1", X3, T, W3, BOXH, ["Điểm chung các lớp", "(macro-F1)"], cls="ext")
c.box("rare", X3, T + 110, W3, BOXH, ["Bắt đúng lớp hiếm", "(recall nhện đỏ)"], cls="ext")
c.arrow(("eval", "r"), ("f1", "l"))
c.arrow((R + BOXW + 20, T + BOXH / 2), [(R + BOXW + 20, T + 110 + BOXH / 2), ("rare", "l")])
c.box("runs", X3, B + 90, W3, 100, ["5 chiến lược × 5 lần chạy", "RoCoLe và sầu riêng"], cls="key")

print(c.svg())

"""Vẽ al-problem.svg: số ảnh lá có nhãn, bộ phòng thí nghiệm so với hai bộ thực địa.

Thanh vẽ theo cùng một thang tuyến tính để thấy hai bộ thực địa nhỏ đến mức nào.
SVG đặt trên slide ở tỉ lệ 1:1 (rộng 1160). Chạy: python3 al_problem.py > al-problem.svg
"""
from svgkit import Canvas, INK, MUTED, FAINT

W, H = 1160, 470
LABEL_W, BAR_X, BAR_MAX, BAR_H = 330, 360, 590, 46
BIG = 34

# (tên, mô tả, số ảnh, màu thanh)
ROWS = [
    ("PlantVillage", "phòng thí nghiệm, nền trơn", 54306, "#9aa5b1"),
    ("Sầu riêng", "thực địa, Việt Nam", 2595, "#1e5631"),
    ("RoCoLe (cà phê)", "thực địa, Ecuador", 1560, "#2f7d4f"),
]
TOP = max(n for _, _, n, _ in ROWS)

c = Canvas(W, H)
for i, (name, desc, n, color) in enumerate(ROWS):
    y = 30 + i * 130
    c.text(LABEL_W, y + 20, name, bold=True, anchor="end")
    c.text(LABEL_W, y + 50, desc, fill=MUTED, anchor="end")
    w = max(6, BAR_MAX * n / TOP)
    c.front.append(f'<rect x="{BAR_X}" y="{y + 4}" width="{w:.1f}" height="{BAR_H}" rx="6" fill="{color}"/>')
    c.text(BAR_X + w + 16, y + 40, f"{n:,}".replace(",", "."), size=BIG, bold=True, anchor="start",
           fill=INK if i else MUTED)

# Đường ngăn và câu chốt
c.front.append(f'<line x1="{BAR_X - 10}" y1="20" x2="{BAR_X - 10}" y2="400" stroke="{FAINT}" stroke-width="1.5"/>')
c.text(W / 2, 450, "Ảnh lá thực địa có nhãn: ít hơn 20 đến 35 lần", size=28, bold=True, fill="#1e5631")
print(c.svg(), end="")

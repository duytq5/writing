"""Vẽ legend.svg: chú giải màu vai trò (chấm cùng màu với ô trong sơ đồ)."""
from svgkit import Canvas, STYLE, MUTED, width

items = [("app", "Người dùng"), ("lab", "Chuyên gia"), ("mle", "Kỹ sư ML"), ("adm", "Quản trị viên"), ("sys", "Hệ thống")]
SIZE, R, GAP = 20, 9, 30
total = sum(2 * R + 8 + width(s, SIZE) for _, s in items) + GAP * (len(items) - 1)
c = Canvas(round(total) + 4, 30)
x = 2
for cls, s in items:
    fill, stroke = STYLE[cls]
    c.front.append(f'<circle cx="{x + R}" cy="15" r="{R}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    c.text(x + 2 * R + 8, 22, s, size=SIZE, fill=MUTED, anchor="start")
    x += 2 * R + 8 + width(s, SIZE) + GAP
print(c.svg(), end="")

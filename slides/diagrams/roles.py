"""Vẽ roles.svg: bốn vai trò, mỗi vai trò đưa gì vào nền tảng và nhận lại gì.

SVG đặt trên slide ở tỉ lệ 1:1 (rộng 1160), nên chữ đúng cỡ --diagram = 22px.
Chạy: python3 roles.py > roles.svg
"""

W, FONT, LINE = 1160, 22, 28
BOX_W, BOX_H = 180, 96
BAR_W = 100
INK, MUTED, GREEN, GREY, BRAND = "#1f2933", "#52606d", "#2f7d4f", "#9aa5b1", "#1e5631"

# (tên, phía, dòng "đưa vào", dòng "nhận lại"); dòng đầu có nhãn in đậm.
ROLES = [
    ("Người dùng|ứng dụng", "left", ["ảnh chụp lá"], ["chẩn đoán,", "mô hình mới"]),
    ("Người gán nhãn|(chuyên gia)", "left", ["nhãn"], ["ảnh cần gán nhãn"]),
    ("Kỹ sư học máy", "right", ["vòng gán nhãn ảnh mới,", "cách huấn luyện, bản phát hành"],
     ["tình trạng vòng,", "kết quả huấn luyện"]),
    ("Quản trị viên", "right", ["duyệt thay đổi,", "cấp quyền"], ["nhật ký:", "ai làm gì, khi nào"]),
]

bar_x = (W - BAR_W) / 2
out = []


def text(x, y, s, fill=INK, bold=False, anchor="middle"):
    w = ' font-weight="bold"' if bold else ""
    out.append(f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{anchor}" font-size="{FONT}"{w} fill="{fill}">{s}</text>')


def label(x, y, head, lines, color):
    for i, s in enumerate(lines):
        if i == 0:
            s = f'<tspan fill="{color}" font-weight="bold">{head} </tspan>{s}'
        text(x, y + i * LINE, s, fill=INK if color == GREEN else MUTED)


def block(name, side, ins, outs, top):
    """Một vai trò: nhãn vào, mũi tên vào, mũi tên ra, nhãn ra. Trả về đáy khối."""
    y_in = top + len(ins) * LINE + 6
    y_out = y_in + 44
    if side == "left":
        bx, a, b = 0, BOX_W + 2, bar_x - 2
    else:
        bx, a, b = W - BOX_W, W - BOX_W - 2, bar_x + BAR_W + 2
    mid = (a + b) / 2
    by = (y_in + y_out) / 2 - BOX_H / 2
    out.append(f'<rect x="{bx + 1}" y="{by:.0f}" width="{BOX_W - 2}" height="{BOX_H}" rx="12" fill="#ffffff" stroke="{MUTED}" stroke-width="2"/>')
    parts = name.split("|")
    for i, p in enumerate(parts):
        text(bx + BOX_W / 2, by + BOX_H / 2 + 8 + (i - (len(parts) - 1) / 2) * LINE, p)
    out.append(f'<line x1="{a}" y1="{y_in}" x2="{b}" y2="{y_in}" stroke="{GREEN}" stroke-width="2.5" marker-end="url(#ar)"/>')
    out.append(f'<line x1="{b}" y1="{y_out}" x2="{a}" y2="{y_out}" stroke="{GREY}" stroke-width="2.5" stroke-dasharray="7 5" marker-end="url(#ar)"/>')
    label(mid, top + LINE - 6, "đưa vào:", ins, GREEN)
    label(mid, y_out + LINE + 2, "nhận lại:", outs, MUTED)
    return y_out + len(outs) * LINE + 10


GAP = 70
heights = {}
bottom = 0
for side in ("left", "right"):
    y = 20
    for r in [r for r in ROLES if r[1] == side]:
        y = block(*r, top=y) + GAP
    bottom = max(bottom, y - GAP)
H = bottom + 20
out.insert(0, f'<rect x="{bar_x}" y="0" width="{BAR_W}" height="{H}" rx="18" fill="{BRAND}"/>')
text(W / 2, H / 2 - 6, "Nền", fill="#ffffff", bold=True)
text(W / 2, H / 2 + LINE - 6, "tảng", fill="#ffffff", bold=True)

print(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H:.0f}" width="{W}" height="{H:.0f}" '
      f'font-family="Arial, Liberation Sans, Helvetica, sans-serif">')
print('<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" '
      f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker></defs>')
print("\n".join(out))
print("</svg>")

"""Vẽ overview.svg: bảng ý tưởng chính và vai trò được lợi, chấm màu theo vai trò.

Thay bảng markdown có chấm HTML (bản xem trước Marp trong VS Code bỏ HTML).
Chạy: python3 overview.py > overview.svg
"""
from svgkit import Canvas, STYLE, MUTED, FAINT

ROLES = [("Người dùng", "app"), ("Chuyên gia", "lab"), ("Kỹ sư ML", "mle"), ("Quản trị viên", "adm")]
ROWS = [
    ("Chẩn đoán trên điện thoại, mô hình mới tự tải về", "app"),
    ("Hệ thống chọn ảnh, chuyên gia chỉ gán ảnh được chọn", "lab mle"),
    ("Kỹ sư chỉ viết cách huấn luyện, nền tảng lo phần còn lại", "mle"),
    ("Mọi thay đổi phải được duyệt và có lịch sử", "mle adm"),
    ("Dữ liệu, mô hình có phiên bản, quay lại được", "app mle"),
    ("Một cổng đăng nhập, mỗi nhóm một quyền", "app lab adm"),
    ("Xem toàn bộ kho ảnh trên trình duyệt", "mle"),
]
X0, CW, HH, RH = 600, 140, 70, 50

c = Canvas(1160, HH + len(ROWS) * RH + 2)


def dot(x, y, cls, r=11):
    c.front.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{STYLE[cls][1]}"/>')


c.text(12, 56, "Ý tưởng chính", fill=MUTED, bold=True, anchor="start")
for i, (name, cls) in enumerate(ROLES):
    x = X0 + i * CW + CW / 2
    dot(x, 18, cls, 9)
    c.text(x, 56, name, fill=MUTED)
c.back.append(f'<line x1="0" y1="{HH}" x2="1160" y2="{HH}" stroke="{MUTED}" stroke-width="2"/>')
for r, (idea, who) in enumerate(ROWS):
    y = HH + r * RH
    if r % 2:
        c.back.append(f'<rect x="0" y="{y}" width="1160" height="{RH}" fill="#f5f7fa"/>')
    c.back.append(f'<line x1="0" y1="{y + RH}" x2="1160" y2="{y + RH}" stroke="{FAINT}" stroke-width="1"/>')
    c.text(12, y + RH / 2 + 8, idea, anchor="start")
    for i, (_, cls) in enumerate(ROLES):
        if cls in who.split():
            dot(X0 + i * CW + CW / 2, y + RH / 2, cls)
print(c.svg(), end="")

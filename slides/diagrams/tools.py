"""Vẽ tools.svg: ba công cụ mã nguồn mở, mỗi công cụ là gì và dùng để làm gì."""
from svgkit import Canvas, MUTED, INK, STYLE, width, LINE

TOOLS = [
    ("Label Studio", "Công cụ gán nhãn dữ liệu trên trình duyệt",
     "Mỗi job gán nhãn một dự án. Chuyên gia xác nhận hoặc sửa nhãn gợi ý của mô hình"),
    ("MLflow", "Công cụ theo dõi thí nghiệm và quản lý phiên bản mô hình",
     "Ghi tham số, chỉ số của mỗi lần huấn luyện, lưu các phiên bản mô hình, đánh dấu bản đang dùng"),
    ("FiftyOne", "Công cụ xem và lọc tập dữ liệu ảnh",
     "Xem toàn bộ kho ảnh kèm nhãn, tập, trạng thái và nguồn ảnh, lọc để chọn ảnh cho job gán nhãn tiếp theo"),
]
W, GAP, H, PAD = 370, 25, 360, 20


def wrap(s, w):
    lines, cur = [], ""
    for word in s.split():
        t = (cur + " " + word).strip()
        if width(t) > w and cur:
            lines.append(cur)
            cur = word
        else:
            cur = t
    return lines + [cur]


c = Canvas(3 * W + 2 * GAP, H)
fill, stroke = STYLE["sys"]
for i, (name, what, use) in enumerate(TOOLS):
    x = i * (W + GAP)
    c.front.append(f'<rect x="{x + 1}" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="#ffffff" stroke="{stroke}" stroke-width="2"/>')
    c.box(f"h{i}", x, 0, W, 64, [name], "key", bold=True)
    y = 64 + 44
    for head, body in (("Là gì", what), ("Dùng để", use)):
        c.text(x + PAD, y, head, fill=MUTED, bold=True, anchor="start")
        y += LINE + 4
        for line in wrap(body, W - 2 * PAD):
            c.text(x + PAD, y, line, fill=INK, anchor="start")
            y += LINE
        y += 26
print(c.svg(), end="")

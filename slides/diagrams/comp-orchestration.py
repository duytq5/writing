"""Vẽ comp-orchestration.svg: hai job tách rời, mỗi job một sơ đồ làn.

Job gán nhãn (máy trạng thái al-round, tệp configs/rounds/) và job huấn luyện
(al-train, tệp configs/trainings/). Mỗi làn là ai làm bước đó: Step Functions
(hệ thống), worker trên máy GPU, chuyên gia trên Label Studio.
Chạy: python3 comp-orchestration.py > comp-orchestration.svg
"""
from svgkit import Canvas, MUTED

LANES = {
    "sys": (["Step Functions", "(hệ thống)"], "sys"),
    "gpu": (["GPU Worker"], "ext"),
    "lab": (["Chuyên gia", "(Label Studio)"], "lab"),
}
JOBS = [
    ("Job gán nhãn", ["sys", "gpu", "lab"], [
        ("sys", ["Snapshot", "dữ liệu"]),
        ("gpu", ["Chấm điểm", "(nếu cần)"]),
        ("sys", ["Chọn k ảnh"]),
        ("lab", ["Gán nhãn", "k ảnh"]),
        ("sys", ["Gộp nhãn,", "phiên bản mới"]),
    ]),
    ("Job huấn luyện", ["sys", "gpu"], [
        ("sys", ["Snapshot", "dữ liệu"]),
        ("gpu", ["Huấn luyện"]),
        ("sys", ["Ghi mô hình"]),
    ]),
]
TITLE, LH, LG, X0, W, G = 30, 64, 8, 208, 160, 37

height = sum(TITLE + len(l) * LH + (len(l) - 1) * LG for _, l, _ in JOBS) + 22
c = Canvas(1160, height)
y = 0
for j, (name, lanes, steps) in enumerate(JOBS):
    c.text(0, y + 21, name, fill=MUTED, bold=True, anchor="start")
    y += TITLE
    top = {}
    for i, lane in enumerate(lanes):
        ly = y + i * (LH + LG)
        top[lane] = ly
        lines, cls = LANES[lane]
        c.back.append(f'<rect x="1" y="{ly}" width="1158" height="{LH}" rx="8" fill="#fafbfc" stroke="#d9dee3" stroke-width="1.5"/>')
        c.box(f"j{j}{lane}", 0, ly, 190, LH, lines, cls)
    keys = []
    for i, (lane, lines) in enumerate(steps):
        k = f"j{j}s{i}"
        c.box(k, X0 + i * (W + G), top[lane] + 6, W, LH - 12, lines, LANES[lane][1])
        keys.append(k)
    for a, b in zip(keys, keys[1:]):
        (ax, ay), (bx, by) = c.anchor(a, "r"), c.anchor(b, "l")
        mid = (ax + bx) / 2
        c.arrow((a, "r"), [(mid, ay), (mid, by), (b, "l")] if ay != by else (b, "l"))
    y += len(lanes) * LH + (len(lanes) - 1) * LG + 22
print(c.svg(), end="")

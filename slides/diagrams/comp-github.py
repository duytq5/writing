"""Vẽ comp-github.svg: chạy job bằng pull request.

Trái: hai tệp thật trong kho vận hành, bỏ dòng chú thích: một job gán nhãn
(configs/rounds/2026-10-15-rocole-second.yaml) và một job huấn luyện
(configs/trainings/2026-10-16-rocole-v1.yaml), có ghi chú từng phần.
Phải: ba bước từ pull request tới AWS.
Chạy: python3 comp-github.py > comp-github.svg
"""
from svgkit import Canvas, MUTED, INK, esc

MONO = 'font-family="Liberation Mono, Menlo, Consolas, monospace"'
FILES = [
    ("Job gán nhãn", "configs/rounds/2026-10-15-rocole-second.yaml", [
        ("dataset: rocole", "← tập dữ liệu"),
        ("selection:", None),
        ("  strategy: random", "← cách chọn ảnh"),
        ("  params: {}", None),
        ("  k: 5", "← số ảnh gán nhãn"),
        ("  seed: 42", None),
    ]),
    ("Job huấn luyện", "configs/trainings/2026-10-16-rocole-v1.yaml", [
        ("dataset: rocole", "← tập dữ liệu"),
        ("version: 1", "← phiên bản dữ liệu"),
        ("train:", "← cách huấn luyện"),
        ("  recipe: timm_classifier", None),
        ("  params: {epochs: 20}", None),
    ]),
]
HEAD, LH = 56, 25

c = Canvas(1160, 440)
y0, tops = 1, []
for title, name, code in FILES:
    h = HEAD + len(code) * LH + 16
    c.front.append(f'<rect x="1" y="{y0}" width="560" height="{h}" rx="8" fill="#ffffff" stroke="#52606d" stroke-width="2"/>')
    c.front.append(f'<path d="M1,{y0 + 8} a8,8 0 0,1 8,-8 h544 a8,8 0 0,1 8,8 v{HEAD - 8} h-560 z" fill="#f5f7fa" stroke="#52606d" stroke-width="2"/>')
    c.text(18, y0 + 24, title, size=20, bold=True, anchor="start")
    c.front.append(f'<text x="18" y="{y0 + 46}" font-size="16" {MONO} fill="{MUTED}">{esc(name)}</text>')
    for i, (line, note) in enumerate(code):
        y = y0 + HEAD + 26 + i * LH
        c.front.append(f'<text x="20" y="{y}" font-size="19" {MONO} fill="{INK}" xml:space="preserve">{esc(line)}</text>')
        if note:
            c.text(335, y, note, size=20, fill=MUTED, anchor="start")
    tops.append(y0)
    y0 += h + 20

# Ba bước
steps = [
    ("pr", ["Quản trị viên viết tệp,", "mở pull request"], "adm"),
    ("ok", ["Người duyệt xem, merge"], "adm"),
    ("run", ["GitHub gọi qua AWS để trigger", "workflow Step Functions"], "sys"),
]
for i, (k, lines, cls) in enumerate(steps):
    c.box(k, 640, 1 + i * 169, 519, 100, lines, cls)
for a, b in zip(steps, steps[1:]):
    c.arrow((a[0], "b"), (b[0], "t"))
c.arrow((561, tops[0] + 28), ("pr", "l", 27 / 100))
c.arrow((561, tops[1] + 28), [(600, tops[1] + 28), (600, 70), ("pr", "l", 69 / 100)])
print(c.svg(), end="")

"""Sơ đồ phần IV: câu chuyện bốn khối, rồi kiến trúc mở từng khối ra.

Chạy (trong thư mục diagrams):
  python3 p4s.py overview > p4s-overview.svg   bốn khối, ba người, vòng lặp
  python3 p4s.py strip N  > p4s-strip-N.svg    dải bốn khối, khối N nổi (N = 1..4)
  python3 p4s.py arch     > p4s-arch.svg       kiến trúc: các thành phần đặt theo nơi chạy
  python3 p4s.py upload   > p4s-upload.svg     luồng 1: ảnh từ điện thoại vào kho
  python3 p4s.py label    > p4s-label.svg      luồng 2: một job gán nhãn
  python3 p4s.py train    > p4s-train.svg      luồng 3: huấn luyện và phát hành

Màu theo khối của câu chuyện: Ứng dụng tím, Kho ảnh xanh lá, Gán nhãn vàng,
Huấn luyện và phát hành xanh dương; phần điều phối job màu xám.
Các bước theo design doc, mục Main flows F1–F6. SVG đặt 1:1 trên slide.
"""
import sys
from p4_kit import Svg, BRAND, MUTED, FAINT, INK
from svgkit import STYLE, width

mode = sys.argv[1] if len(sys.argv) > 1 else "overview"
FADE = 0.2

BLOCKS = [("app", "Ứng dụng", ["chụp lá, chẩn đoán", "ngay trên máy"]),
          ("sys", "Kho ảnh", ["lưu ảnh gửi về,", "chưa có nhãn"]),
          ("lab", "Gán nhãn", ["chuyên gia gán", "ảnh được chọn"]),
          ("mle", ["Huấn luyện", "và phát hành"], ["mô hình mới"])]

# ---------------------------------------------------------------- overview
if mode == "overview":
    BW, BH, GAP, L, Y = 220, 130, 86, 8, 120
    X = [L + i * (BW + GAP) for i in range(4)]
    s = Svg(1160, 400)
    for i, (cls, title, sub) in enumerate(BLOCKS):
        s.box(f"b{i}", X[i], Y, BW, BH, title, sub, cls=cls, num=i + 1)
        if i < 3:
            s.arrow([(X[i] + BW, Y + BH / 2), (X[i + 1] - 3, Y + BH / 2)], width_=3)
    for i, name, cls in [(0, "Người dùng", "app"), (2, "Chuyên gia", "lab"), (3, "Kỹ sư", "mle")]:
        pw = width(name, 22, True) + 62
        x = X[i] + (BW - pw) / 2
        s.person(x, 20, name, cls)
        s.arrow([(X[i] + BW / 2, 62), (X[i] + BW / 2, Y - 3)], color=STYLE[cls][1])
    s.text(X[3] + BW / 2 - 12, 98, "mở job bằng pull request", size=18, fill=STYLE["mle"][1], anchor="end")
    RY = Y + BH + 80
    s.arrow([(X[3] + BW / 2, Y + BH), (X[3] + BW / 2, RY), (X[0] + BW / 2, RY), (X[0] + BW / 2, Y + BH + 3)],
            width_=3, color=BRAND)
    s.text((X[0] + X[3] + BW) / 2, RY + 34, "mô hình mới về điện thoại, vòng lặp tiếp tục", size=22,
           bold=True, fill=BRAND)
    print(s.svg(), end="")

# ---------------------------------------------------------------- strip
elif mode == "strip":
    n = int(sys.argv[2])
    names = ["Ứng dụng", "Kho ảnh", "Gán nhãn", "Huấn luyện và phát hành"]
    W = [200, 200, 200, 330]
    GAP = (1160 - sum(W)) / 3
    s = Svg(1160, 52)
    x = 0
    for i, name in enumerate(names):
        on = i + 1 == n
        cls = "key" if on else BLOCKS[i][0]
        s.box(f"s{i}", x, 4, W[i], 44, f"{i + 1}  {name}", cls=cls, op=1 if on else 0.35, bold=on)
        if i < 3:
            s.arrow([(x + W[i] + 4, 26), (x + W[i] + GAP - 6, 26)], op=0.5)
        x += W[i] + GAP
    print(s.svg(), end="")

# ---------------------------------------------------------------- architecture
else:
    H = 480
    # (key, x, y, w, h, title, sub, màu)
    C = [
        ("app", 10, 226, 130, 120, "Ứng dụng", ["Flutter,", "mô hình", "ONNX"], "app"),
        ("gw", 178, 106, 160, 76, "API Gateway", "Cognito", "sys"),
        ("fo", 352, 106, 160, 76, "FiftyOne", "xem kho ảnh", "sys"),
        ("ls", 526, 106, 160, 76, "Label Studio", "gán nhãn", "lab"),
        ("ml", 700, 106, 160, 76, "MLflow", "kết quả chạy", "mle"),
        ("lam", 178, 226, 160, 76, "Lambda", "xử lý yêu cầu", "sys"),
        ("sfn", 526, 226, 160, 76, ["Step", "Functions"], None, "ext"),
        ("sqs", 700, 226, 160, 76, "SQS", "hàng đợi job", "ext"),
        ("s3", 178, 350, 334, 96, "S3", "ảnh, mô hình ONNX", "sys"),
        ("pg", 526, 350, 334, 96, "Postgres", "ảnh, nhãn, phiên bản dữ liệu", "sys"),
        ("repo", 912, 106, 236, 62, "Kho cấu hình", "tệp job, pull request", "ext"),
        ("act", 912, 180, 236, 56, "GitHub Actions", None, "ext"),
        ("wk", 912, 320, 236, 120, "GPU Worker", ["chấm điểm,", "huấn luyện,", "xuất ONNX"], "mle"),
    ]
    PEOPLE = [("user", 4, "Người dùng", "app"), ("exp", 526, "Chuyên gia", "lab"), ("eng", 950, "Kỹ sư", "mle")]
    ZONES = [(0, 58, 150, 410, "Điện thoại"), (164, 58, 722, 410, "AWS"),
             (900, 58, 260, 190, "GitHub"), (900, 262, 260, 206, "")]

    # luồng: (các thành phần rõ, các mũi tên [(số, điểm, chỗ đặt số)], số đặt trên khối, chú thích)
    FLOWS = {
        "upload": ({"app", "gw", "lam", "s3", "pg", "user"}, [
            (1, [(140, 262), (159, 262), (159, 144), (175, 144)], (159, 205)),
            (1, [(258, 182), (258, 223)], None),
            (2, [(75, 346), (75, 420), (175, 420)], (75, 385)),
            (3, [(258, 350), (258, 305)], (236, 328)),
            (4, [(338, 264), (440, 264), (440, 322), (620, 322), (620, 347)], (440, 293)),
        ], [], ["Đăng nhập Google, gửi kết quả chẩn đoán", "Gửi ảnh thẳng lên S3 bằng link ký sẵn",
                "Kiểm tra đúng là ảnh, xoá thông tin vị trí", "Ghi ảnh mới: chưa có nhãn"]),
        "label": ({"repo", "act", "sfn", "sqs", "wk", "ls", "pg", "eng", "exp"}, [
            (1, [(1030, 44), (1030, 97)], (1050, 72)),
            (2, [(912, 207), (650, 207), (650, 223)], (800, 207)),
            (3, [(686, 264), (697, 264)], None),
            (3, [(860, 280), (909, 340)], (868, 314)),
            (5, [(560, 226), (560, 185)], (538, 205)),
            (6, [(606, 44), (606, 103)], (626, 72)),
            (7, [(606, 302), (606, 347)], (606, 325)),
        ], [(4, 1148, 320)], ["Kỹ sư mở pull request, được duyệt và merge", "GitHub Actions khởi động job trên AWS",
                            "Gửi việc qua hàng đợi tới GPU Worker", "Chấm điểm mọi ảnh chưa có nhãn",
                            "Chiến lược chọn k ảnh, tạo project", "Chuyên gia gán nhãn",
                            "Ghi phiên bản dữ liệu mới"]),
        "train": ({"repo", "act", "sfn", "sqs", "wk", "ml", "s3", "app", "eng", "user"}, [
            (1, [(1030, 44), (1030, 97)], (1050, 72)),
            (2, [(912, 207), (650, 207), (650, 223)], (800, 207)),
            (3, [(686, 264), (697, 264)], None),
            (3, [(860, 280), (909, 340)], (868, 314)),
            (4, [(912, 410), (876, 410), (876, 144), (863, 144)], (876, 380)),
            (6, [(1030, 440), (1030, 458), (345, 458), (345, 449)], (690, 458)),
            (7, [(178, 398), (110, 398), (110, 349)], (130, 398)),
        ], [(5, 912, 440)], ["Kỹ sư mở pull request huấn luyện", "GitHub Actions khởi động job trên AWS",
                            "Gửi việc qua hàng đợi tới GPU Worker", "Huấn luyện, ghi kết quả vào MLflow",
                            "Pull request phát hành: GPU Worker xuất ONNX", "Lưu mô hình ONNX lên S3",
                            "Ứng dụng tải mô hình mới, kiểm tra SHA-256"]),
    }

    flow = FLOWS.get(mode)
    show = flow[0] if flow else None

    def op(k):
        return 1 if show is None or k in show else FADE

    steps = flow[3] if flow else []
    rows = (len(steps) + 1) // 2
    s = Svg(1160, H + (24 + rows * 34 if flow else 50))
    for x, y, w, h, name in ZONES:
        s.back.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#fafbfc" stroke="{FAINT}" '
                      f'stroke-width="1.5" stroke-dasharray="6 4"/>')
        s.text(x + 14, y + 30, name, size=20, fill=MUTED, bold=True, anchor="start", layer=s.back)
    for key, x, name, cls in PEOPLE:
        s.person(x, 2, name, cls, op=op(key))
    for key, x, y, w, h, title, sub, cls in C:
        s.box(key, x, y, w, h, title, sub, cls=cls, op=op(key), shape="cyl" if key in ("s3", "pg") else "rect")
    if flow:
        for num, pts, at in flow[1]:
            s.arrow(pts, color=BRAND, width_=3.5)
            if at:
                s.badge(*at, num)
        for num, x, y in flow[2]:
            s.badge(x, y, num)
        for i, t in enumerate(steps):
            col, row = i // rows, i % rows
            x, y = 20 + col * 590, H + 34 + row * 34
            s.badge(x + 14, y - 7, i + 1)
            s.check("steps", t, 540)
            s.text(x + 40, y, t, size=21, anchor="start")
    else:
        # chú thích màu: mỗi thành phần thuộc khối nào trong câu chuyện
        x = 10
        for cls, name in [("app", "Ứng dụng"), ("sys", "Kho ảnh"), ("lab", "Gán nhãn"),
                          ("mle", "Huấn luyện và phát hành"), ("ext", "điều phối job")]:
            f, st = STYLE[cls]
            s.mid.append(f'<rect x="{x}" y="{H + 16}" width="26" height="22" rx="5" fill="{f}" stroke="{st}" stroke-width="2"/>')
            s.text(x + 36, H + 34, name, size=20, anchor="start")
            x += 36 + width(name, 20) + 34
    print(s.svg(), end="")

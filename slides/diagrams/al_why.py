"""Vẽ al-why.svg: vì sao phải giả lập. Ba bài báo cho thấy hiệu quả của học chủ động
đổi theo bộ dữ liệu, nên phải thử trên chính dữ liệu của luận văn.

Lời trên slide viết cho người chưa biết học chủ động; tên bài báo đầy đủ để trong ghi chú.
SVG đặt trên slide ở tỉ lệ 1:1 (rộng 1160). Chạy: python3 al_why.py > al-why.svg
"""
from svgkit import Canvas, INK, MUTED, FAINT, STYLE, width

BRAND = "#1e5631"
LAB_FILL, LAB = STYLE["lab"]
c = Canvas(1160, 552)

# (tác giả và năm, hội nghị, câu trích nguyên văn, ý tiếng Việt). Trích từ:
# Werner 2024, mục 1; Lüth 2023, mục 4 (P1); Hacohen 2022, tên bài báo.
PAPERS = [
    ("Werner và cộng sự, 2024", "NeurIPS [1]",
     ["“The superiority of methods", "is strongly dataset- and", "domain-dependent …”"],
     ["Chiến lược tốt nhất", "đổi theo từng bộ dữ liệu"]),
    ("Lüth và cộng sự, 2023", "NeurIPS [2]",
     ["“… class distribution is a crucial", "predictor for the potential", "performance gains of AL", "on a dataset”"],
     ["Mức lệch lớp quyết định", "học chủ động giúp bao nhiêu"]),
    ("Hacohen và cộng sự, 2022", "ICML [3]",
     ["“Opposite Strategies Suit", "High and Low Budgets”"],
     ["Ít nhãn và nhiều nhãn", "cần hai cách chọn ngược nhau"]),
]
CW, CH, GAP, QUOTE = 360, 312, 40, 21
for j, (who, venue, quote, gloss) in enumerate(PAPERS):
    x = 1 + j * (CW + GAP)
    c.front.append(f'<rect x="{x}" y="0" width="{CW - 2}" height="{CH}" rx="14" fill="#ffffff" stroke="{FAINT}" stroke-width="2"/>')
    # biểu tượng bài báo: tờ giấy gấp góc và vài dòng chữ
    px, py = x + 22, 22
    c.front.append(f'<path d="M{px},{py} h36 l14,14 v46 h-50 Z" fill="{LAB_FILL}" stroke="{LAB}" stroke-width="2.5"/>'
                   f'<path d="M{px + 36},{py} v14 h14" fill="none" stroke="{LAB}" stroke-width="2.5"/>')
    for i in range(3):
        c.front.append(f'<line x1="{px + 9}" y1="{py + 30 + i * 11}" x2="{px + 41}" y2="{py + 30 + i * 11}" stroke="{LAB}" stroke-width="2"/>')
    c.text(x + 88, 46, who, size=20, bold=True, anchor="start")
    c.text(x + 88, 72, venue, size=20, fill=MUTED, anchor="start")
    top = 128 + (4 - len(quote)) * 14  # căn giữa khối trích dẫn theo chiều dọc
    for i, s in enumerate(quote):
        assert width(s, QUOTE) < CW - 30, s
        c.front.append(f'<text x="{x + CW / 2:.0f}" y="{top + i * 28:.0f}" text-anchor="middle" font-size="{QUOTE}" '
                       f'font-style="italic" fill="{INK}">{s}</text>')
    c.front.append(f'<line x1="{x + 40}" y1="232" x2="{x + CW - 42}" y2="232" stroke="{FAINT}" stroke-width="1.5"/>')
    for i, s in enumerate(gloss):
        assert width(s, 20, bold=True) < CW - 30, s
        c.text(x + CW / 2, 260 + i * 26, s, size=20, bold=True, fill=BRAND)
    c.arrow((x + CW / 2, CH + 4), (500 + j * 80, 372))

# Kết luận của Duy, và trích dẫn đầy đủ ở chân slide
c.box("q", 80, 374, 1000, 96, ["Cần thực nghiệm để đưa ra chiến thuật chọn ảnh",
                               "phù hợp với thực trạng của từng dataset"], cls="key", bold=True)
REFS = [
    "[1] T. Werner, J. Burchert, M. Stubbemann, L. Schmidt-Thieme, “A Cross-Domain Benchmark for Active Learning,” NeurIPS 2024.",
    "[2] C. T. Lüth, T. J. Bungert, L. Klein, P. F. Jaeger, “Navigating the Pitfalls of Active Learning Evaluation,” NeurIPS 2023.",
    "[3] G. Hacohen, A. Dekel, D. Weinshall, “Active Learning on a Budget: Opposite Strategies Suit High and Low Budgets,” ICML 2022.",
]
for k, r in enumerate(REFS):
    assert width(r, 16) < 1160, r
    c.text(0, 502 + k * 22, r, size=16, fill=MUTED, anchor="start")
print(c.svg(), end="")

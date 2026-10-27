"""Vẽ al-why.svg: vì sao phải giả lập. Hai nghiên cứu so sánh học chủ động cho kết quả
ngược nhau, nên phải thử trên chính dữ liệu của luận văn.

Dùng đúng hai nguồn báo cáo dùng cho ý này (mục 1.1.2 và 3.2.2): Beck [33], Munjal [34].
Trích dẫn đầy đủ nằm ở chân slide (_footer), không vẽ trong hình.
SVG đặt trên slide ở tỉ lệ 1:1 (rộng 1160). Chạy: python3 al_why.py > al-why.svg
"""
from svgkit import Canvas, MUTED, FAINT, STYLE, width

BRAND = "#1e5631"
LAB_FILL, LAB = STYLE["lab"]
c = Canvas(1160, 470)

# (tác giả và năm, nơi đăng, kết luận chính: Beck theo tóm tắt; Munjal theo tóm tắt và mục 5–6)
PAPERS = [
    ("Beck và cộng sự, 2021", "ICML Workshop [33]",
     ["Tăng cường ảnh cơ bản (lật, cắt):", "AL cần ít nhãn hơn", "chọn ngẫu nhiên 2–4 lần"]),
    ("Munjal và cộng sự, 2022", "CVPR [34]",
     ["Điều chuẩn mạnh (RandAugment, SWA):", "chọn ngẫu nhiên cũng tăng mạnh,", "AL không còn hơn rõ rệt"]),
]
CW, CH, GAP = 540, 300, 80
for j, (who, venue, gloss) in enumerate(PAPERS):
    x = 1 + j * (CW + GAP)
    c.front.append(f'<rect x="{x}" y="0" width="{CW - 2}" height="{CH}" rx="14" fill="#ffffff" stroke="{FAINT}" stroke-width="2"/>')
    # biểu tượng bài báo: tờ giấy gấp góc và vài dòng chữ
    px, py = x + 22, 22
    c.front.append(f'<path d="M{px},{py} h36 l14,14 v46 h-50 Z" fill="{LAB_FILL}" stroke="{LAB}" stroke-width="2.5"/>'
                   f'<path d="M{px + 36},{py} v14 h14" fill="none" stroke="{LAB}" stroke-width="2.5"/>')
    for i in range(3):
        c.front.append(f'<line x1="{px + 9}" y1="{py + 30 + i * 11}" x2="{px + 41}" y2="{py + 30 + i * 11}" stroke="{LAB}" stroke-width="2"/>')
    c.text(x + 88, 46, who, size=22, bold=True, anchor="start")
    c.text(x + 88, 74, venue, size=20, fill=MUTED, anchor="start")
    c.front.append(f'<line x1="{x + 40}" y1="118" x2="{x + CW - 42}" y2="118" stroke="{FAINT}" stroke-width="1.5"/>')
    for i, s in enumerate(gloss):
        assert width(s, 25, bold=True) < CW - 30, s
        c.text(x + CW / 2, 170 + i * 38, s, size=25, bold=True, fill=BRAND)
    c.arrow((x + CW / 2, CH + 4), (500 + j * 160, 362))

# Kết luận của Duy
c.box("q", 80, 364, 1000, 96, ["Cần thực nghiệm để đưa ra chiến thuật chọn ảnh",
                               "phù hợp với thực trạng của từng dataset"], cls="key", bold=True)
print(c.svg(), end="")

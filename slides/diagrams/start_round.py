"""Vẽ chú thích lên ảnh chụp danh sách workflow start-round: khung quanh lần chạy
của PR #12 và một ô chú thích ở khoảng trống giữa dòng.

Chạy từ thư mục slides: python3 diagrams/start_round.py
Toạ độ đo trên ảnh thu về 2000 px chiều ngang.
"""
from PIL import Image, ImageDraw, ImageFont

SRC = "assets/operator/start-round-runs.png"
OUT = "assets/operator/start-round-runs-annotated.png"
ORANGE = (255, 109, 4)
INK = (31, 41, 51)
MUTED = (82, 96, 109)
FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

base = Image.open(SRC).convert("RGB")
k = base.width / 2000


def s(*v):
    return [round(x * k) for x in v]


ROW = (6, 84, 1990, 180)  # lần chạy của PR #12
NOTE = (1075, 92, 1545, 172)

# Làm mờ các dòng khác, giữ sáng dòng của PR #12.
img = Image.blend(base, Image.new("RGB", base.size, (0, 0, 0)), 0.45)
img.paste(base.crop(s(*ROW)), s(*ROW)[:2])
d = ImageDraw.Draw(img)
d.rounded_rectangle(s(*ROW), radius=round(8 * k), outline=ORANGE, width=round(4 * k))
d.rounded_rectangle(s(*NOTE), radius=round(8 * k), fill="white", outline=ORANGE, width=round(3 * k))
d.text(s(NOTE[0] + 16, NOTE[1] + 10), "Merge PR #12 → start-round thành công",
       font=ImageFont.truetype(BOLD, round(22 * k)), fill=INK)
d.text(s(NOTE[0] + 16, NOTE[1] + 44), "Chạy 25 giây. Vòng gán nhãn thứ ba bắt đầu.",
       font=ImageFont.truetype(FONT, round(19 * k)), fill=MUTED)
img.save(OUT, optimize=True)

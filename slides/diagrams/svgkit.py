"""Bộ vẽ SVG nhỏ cho các sơ đồ vẽ tay của slide.

Sơ đồ đặt trên slide ở tỉ lệ 1:1, nên chữ đúng cỡ --diagram = 22px.
Màu theo vai trò giống các sơ đồ mermaid (mermaid.json, classDef).
"""

FONT, LINE = 22, 27
INK, MUTED, FAINT = "#1f2933", "#52606d", "#9aa5b1"
STYLE = {
    "app": ("#f3e8fd", "#8250df"),
    "lab": ("#fff8c5", "#bf8700"),
    "mle": ("#e7f0fd", "#2563eb"),
    "adm": ("#fde8e8", "#cf222e"),
    "sys": ("#eef6f0", "#2f7d4f"),
    "ext": ("#f5f7fa", "#52606d"),
    "key": ("#1e5631", "#1e5631"),
}


def width(s, size=FONT, bold=False):
    """Độ rộng chữ ước lượng (Liberation Sans, cùng số đo với Arial); để kiểm tra chữ có tràn ô."""
    try:
        from PIL import ImageFont
        f = ImageFont.truetype("LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf", size)
        return f.getlength(s)
    except Exception:
        return len(s) * size * 0.5


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Canvas:
    def __init__(self, w, h, dy=0):
        """dy: dời mọi thứ xuống dy px, chừa chỗ cho nhãn ở mép trên."""
        self.w, self.h, self.dy = w, h, dy
        self.back, self.front, self.boxes = [], [], {}

    def text(self, x, y, s, size=FONT, fill=INK, bold=False, anchor="middle", layer=None):
        b = ' font-weight="bold"' if bold else ""
        (self.front if layer is None else layer).append(
            f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{anchor}" font-size="{size}"{b} fill="{fill}">{esc(s)}</text>')

    def zone(self, x, y, w, h, label):
        """Vùng nền (một hệ thống hay một nơi chạy), nhãn ở góc trên trái."""
        self.back.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#fafbfc" stroke="{FAINT}" stroke-width="1.5" stroke-dasharray="6 4"/>')
        self.text(x + 14, y + 30, label, fill=MUTED, bold=True, anchor="start", layer=self.back)

    def box(self, key, x, y, w, h, lines, cls="sys", shape="rect", bold=False, dashed=False):
        fill, stroke = STYLE[cls]
        dash = ' stroke-dasharray="7 4"' if dashed else ""
        color = "#ffffff" if cls == "key" else INK
        if shape == "cyl":
            e = 9
            self.front.append(
                f'<path d="M{x},{y + e} a{w / 2},{e} 0 0,0 {w},0 a{w / 2},{e} 0 0,0 {-w},0 v{h - 2 * e} a{w / 2},{e} 0 0,0 {w},0 v{-(h - 2 * e)}" '
                f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        else:
            rx = h / 2 if shape == "pill" else 8
            self.front.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2"{dash}/>')
        lines = lines if isinstance(lines, list) else [lines]
        top = y + h / 2 - (len(lines) - 1) * LINE / 2 + 8 + (4 if shape == "cyl" else 0)
        for i, s in enumerate(lines):
            if width(s, bold=bold) > w - 12:
                import sys
                print(f"warning: '{s}' is wider than box {key}", file=sys.stderr)
            self.text(x + w / 2, top + i * LINE, s, fill=color, bold=bold)
        self.boxes[key] = (x, y, w, h)

    def anchor(self, key, side, t=0.5):
        x, y, w, h = self.boxes[key]
        return {"l": (x, y + h * t), "r": (x + w, y + h * t), "t": (x + w * t, y), "b": (x + w * t, y + h)}[side]

    def arrow(self, a, b, label=None, dashed=False, color=MUTED, label_at=0.5, label_dy=-8, label_seg=None, label_anchor="middle", head=True, both=False):
        """a, b: (key, side[, t]) hoặc điểm (x, y). Có thể truyền danh sách điểm gấp khúc.
        head=False: đường không mũi tên; both=True: mũi tên hai đầu."""
        pts = [self._pt(p) for p in ([a] + (b if isinstance(b, list) else [b]))]
        d = "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in pts)
        dash = ' stroke-dasharray="7 5"' if dashed else ""
        marks = (' marker-end="url(#ar)"' if head else "") + (' marker-start="url(#ar)"' if both else "")
        self.front.insert(0, f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2"{dash}{marks}/>')
        if label:
            seg = label_seg if label_seg is not None else len(pts) - 2
            (x1, y1), (x2, y2) = pts[seg], pts[seg + 1]
            lx, ly = x1 + (x2 - x1) * label_at, y1 + (y2 - y1) * label_at + label_dy
            lines = label if isinstance(label, list) else [label]
            for i, s in enumerate(lines):
                self.text(lx, ly - (len(lines) - 1 - i) * (LINE - 3), s, size=FONT - 2, fill=MUTED, anchor=label_anchor)

    def _pt(self, p):
        if isinstance(p, tuple) and isinstance(p[0], str):
            return self.anchor(*p)
        return p

    def svg(self):
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" '
                'font-family="Arial, Liberation Sans, Helvetica, sans-serif">\n'
                '<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" '
                f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker></defs>\n')
        body = "\n".join(self.back + self.front)
        if self.dy:
            body = f'<g transform="translate(0,{self.dy})">\n{body}\n</g>'
        return head + body + "\n</svg>\n"

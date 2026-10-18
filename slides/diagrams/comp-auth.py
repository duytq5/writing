"""Vẽ comp-auth.svg: đăng nhập và phân quyền, hai làn.

Làn trên: người dùng ứng dụng đăng nhập Google qua Cognito, API Gateway kiểm
tra token (xác thực), Lambda API kiểm tra nhóm (phân quyền).
Làn dưới: chuyên gia, kỹ sư ML, quản trị viên đăng nhập Cognito bằng email và
mật khẩu, cổng xác thực (reverse proxy) kiểm tra cả token và nhóm.
Chạy: python3 comp-auth.py > comp-auth.svg
"""
from svgkit import Canvas, MUTED

RED = "#cf222e"
X = [0, 240, 490, 740, 970]  # cột: ai, đăng nhập, xác thực, phân quyền, vào được
W = [190, 200, 200, 180, 190]

c = Canvas(1160, 460)
for x, w, s in zip(X, W, ["Ai", "Đăng nhập", "Xác thực", "Phân quyền", "Vào được"]):
    c.text(x + w / 2, 22, s, fill=MUTED, bold=True)


def note(col, y, s, span=1):
    x = X[col] + (sum(W[col:col + span]) + 50 * (span - 1)) / 2
    c.text(x, y, s, size=20, fill=RED)


# Làn 1: ứng dụng
y1, h1 = 45, 90
c.box("app", X[0], y1, W[0], h1, ["Người dùng", "ứng dụng"], "app")
c.box("google", X[1], y1, W[1], h1, ["Google", "qua Cognito"])
c.box("gw", X[2], y1, W[2], h1, ["API Gateway", "token hợp lệ?"], "key")
c.box("fn", X[3], y1, W[3], h1, ["Lambda API", "đúng nhóm?"], "key")
c.box("up", X[4], y1, W[4], h1, ["Gửi ảnh", "(uploaders)"])
for a, b in [("app", "google"), ("google", "gw"), ("gw", "fn"), ("fn", "up")]:
    c.arrow((a, "r"), (b, "l"))
note(2, y1 + h1 + 28, "không: 401")
note(3, y1 + h1 + 28, "không: 403")

# Làn 2: người dùng công cụ web
y2, h, g = 200, 66, 12
h2 = 3 * h + 2 * g
for i, (k, s, cls) in enumerate([("lab", "Chuyên gia", "lab"), ("mle", "Kỹ sư ML", "mle"), ("adm", "Quản trị viên", "adm")]):
    c.box(k, X[0], y2 + i * (h + g), W[0], h, [s], cls)
c.box("cog", X[1], y2, W[1], h2, ["Cognito", "email,", "mật khẩu", "(MFA tùy chọn)"])
c.box("px", X[2], y2, X[3] + W[3] - X[2], h2, ["Cổng xác thực (reverse proxy)", "token hợp lệ? đúng nhóm?"], "key")
for i, (k, s, grp) in enumerate([("ls", "Label Studio", "labelers, admins"), ("ml", "MLflow", "admins"), ("fo", "FiftyOne", "admins")]):
    c.box(k, X[4], y2 + i * (h + g), W[4], h, [s, f"({grp})"])
for i, k in enumerate(["lab", "mle", "adm"]):
    t = (i * (h + g) + h / 2) / h2
    c.arrow((k, "r"), ("cog", "l", t))
    c.arrow(("px", "r", t), (["ls", "ml", "fo"][i], "l"))
c.arrow(("cog", "r"), ("px", "l"))
note(2, y2 + h2 + 28, "không: về trang đăng nhập")
note(3, y2 + h2 + 28, "không: 403")
print(c.svg(), end="")

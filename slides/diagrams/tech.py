"""Vẽ tech.svg: công nghệ theo từng lớp."""
from svgkit import Canvas, width, FONT

rows = [
    ("Ứng dụng", ["Flutter", "ONNX Runtime"]),
    ("Học máy", ["PyTorch", "timm (FastViT)", "MLflow"]),
    ("Dữ liệu, gán nhãn", ["PostgreSQL", "S3", "Label Studio", "FiftyOne"]),
    ("API, điều phối", ["API Gateway", "Lambda (FastAPI)", "Cognito", "Step Functions", "SQS"]),
    ("Điều khiển", ["GitHub Actions", "GHCR", "OIDC"]),
    ("Hạ tầng", ["AWS CDK (Python)", "EC2", "Docker Compose"]),
]
ROW, CH = 76, 46
c = Canvas(1160, ROW * len(rows))
for i, (layer, chips) in enumerate(rows):
    y = i * ROW
    c.box(f"l{i}", 0, y + (ROW - CH) / 2, 230, CH, [layer], "key", bold=True)
    x = 260
    for j, s in enumerate(chips):
        w = width(s) + 36
        c.box(f"c{i}{j}", x, y + (ROW - CH) / 2, w, CH, [s], "sys", shape="pill")
        x += w + 14
print(c.svg(), end="")

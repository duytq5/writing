"""Vẽ comp-storage.svg: S3 giữ tệp, Postgres giữ siêu dữ liệu."""
from svgkit import Canvas

c = Canvas(1160, 380)
c.zone(0, 0, 540, 330, "S3: tệp")
c.zone(620, 0, 540, 330, "Postgres: siêu dữ liệu")
s3 = [("incoming/", "ảnh chờ kiểm tra"), ("raw/", "ảnh đã kiểm tra"), ("manifests/", "phiên bản dữ liệu"),
      ("scores/, selections/", "điểm và ảnh được chọn"), ("edge/", "mô hình ONNX"), ("backups/", "bản sao lưu")]
pg = [("Ảnh, nhãn", "ai gán, nguồn nào"), ("Phiên bản dữ liệu", "ảnh nào, nhãn nào"),
      ("Job", "ai chạy, commit nào"), ("Mô hình", "lớp, SHA-256"),
      ("Phát hành", "ai phát hành, khi nào"), ("Lần chụp, cây trồng", "dự đoán của ứng dụng")]
for z, (x0, items) in enumerate([(14, s3), (634, pg)]):
    for i, (a, b) in enumerate(items):
        k = f"z{z}i{i}"
        c.box(k, x0 + (i % 2) * 262, 50 + (i // 2) * 92, 250, 78, [a, b], "sys")
c.arrow((890, 330), [(890, 362), (401, 362), ("z0i5", "b")], "sao lưu mỗi đêm", label_seg=1, label_dy=-6)
print(c.svg(), end="")

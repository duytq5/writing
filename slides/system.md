---
marp: true
lang: vi
title: Nền tảng MLOps học chủ động
paginate: true
size: 16:9
style: |
  /* Thang chữ dùng chung cho cả bộ slide (px trên slide 1280x720).
     Chữ trong sơ đồ: --diagram; SVG được vẽ đúng cỡ này và đặt ở tỉ lệ 1:1. */
  :root {
    --display: 52px;  /* tiêu đề trang mở phần */
    --title: 38px;    /* tiêu đề slide */
    --lead: 28px;     /* dòng phụ trang mở phần */
    --body: 26px;     /* chữ thường, bảng */
    --diagram: 22px;  /* chữ trong sơ đồ */
    --note: 20px;     /* chú thích */
    --page: 16px;     /* số trang */
    --ink: #1f2933; --muted: #52606d; --faint: #9aa5b1;
    --brand: #1e5631; --brand-soft: #cfe8d6;
  }
  section {
    font-family: -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    font-size: var(--body);
    color: var(--ink);
    background: #ffffff;
    padding: 44px 60px;
    display: block;
    align-content: start !important;
  }
  h1 { color: var(--brand); font-size: var(--title); font-weight: bold; margin: 0 0 16px; }
  table { font-size: var(--body); }
  img { display: block; margin: 0 auto; }
  .note { color: var(--muted); font-size: var(--note); text-align: center; margin-top: 12px; }
  section::after { color: var(--faint); font-size: var(--page); }
  /* Bảng */
  table { border-collapse: collapse; margin: 0 auto; }
  th { background: #eef6f0; color: var(--brand); font-weight: bold; }
  th, td { padding: 8px 14px; border: 1px solid #d9e2ec; }
  section.matrix table { width: 100%; }
  section.matrix td:not(:first-child), section.matrix th:not(:first-child) { text-align: center; width: 112px; font-size: var(--diagram); }
  /* Thẻ ý chính dưới sơ đồ: danh sách trên slide có class cards */
  section.cards ul { display: flex; gap: 18px; list-style: none; padding: 0; margin: 22px 0 0; }
  section.cards li { flex: 1; background: #f5f7fa; border-left: 6px solid var(--brand); border-radius: 8px; padding: 12px 16px; font-size: var(--diagram); line-height: 1.3; }
  section.part { background: var(--brand); color: #ffffff; align-content: center !important; }
  section.part h1 { color: #ffffff; font-size: var(--display); } 
  section.part p { color: var(--brand-soft); font-size: var(--lead); }
---

<!-- _class: part -->
<!-- _paginate: false -->

# Phần 1. Vì sao cần hệ thống

Từ thí nghiệm học chủ động đến một nền tảng chạy thật

---

# Ai dùng hệ thống?

![w:1160](diagrams/roles.svg)

---

# Là một người dùng ứng dụng, tôi muốn…

![w:847](diagrams/story-user.svg)

---

# Là một người gán nhãn, tôi muốn…

![w:752](diagrams/story-labeler.svg)

---

# Là một kỹ sư học máy, tôi muốn…

![w:813](diagrams/story-mle.svg)

---

# Là một quản trị viên, tôi muốn…

![w:775](diagrams/story-admin.svg)

---

# Hành trình: từ ảnh chụp đến mô hình tốt hơn

![w:1111](diagrams/journey.svg)

![w:742](diagrams/legend.svg)

---

<!-- _class: part -->
<!-- _paginate: false -->

# Phần 2. Giải pháp

Từ nhu cầu đến thiết kế hệ thống

---

<!-- _class: matrix -->

# Tổng quan giải pháp

![w:1160](diagrams/overview.svg)

---

# Kiến trúc tổng thể

![w:1160](diagrams/architecture.svg)

---

# Công cụ mã nguồn mở

![w:1160](diagrams/tools.svg)

---

<!-- _class: cards -->

# Ứng dụng di động

![w:1160](diagrams/comp-app.svg)

- Mô hình chạy trên máy: chẩn đoán cả khi không có mạng
- Không cần tài khoản để chẩn đoán, chỉ đăng nhập khi gửi ảnh
- Mô hình mới tự tải về, không cần cập nhật ứng dụng

---

# Đăng nhập và phân quyền

![w:1160](diagrams/comp-auth.svg)

---

<!-- _class: cards -->

# Vận hành bằng pull request

![w:1160](diagrams/comp-github.svg)

- Lịch sử Git: ai chạy job nào, lúc nào
- Phát hành mô hình cũng vậy: sửa một tệp, merge
- Quay lại bản trước: revert pull request

<!--
Gán nhãn và huấn luyện là hai job riêng, mỗi job một tệp nhỏ. Job gán nhãn ghi tập dữ liệu, cách chọn ảnh và số ảnh. Job huấn luyện ghi tập dữ liệu, phiên bản dữ liệu và cách huấn luyện. Quản trị viên không mở trang quản trị nào: viết tệp, mở pull request, được duyệt và merge thì GitHub gọi AWS để chạy job. Phát hành mô hình làm giống hệt.
-->

---

<!-- _class: cards -->

# Job gán nhãn và job huấn luyện

![w:1160](diagrams/comp-orchestration.svg)

- Job gán nhãn tạo phiên bản dữ liệu mới, job huấn luyện tạo mô hình mới
- Chấm điểm dùng mô hình mới nhất, chọn ngẫu nhiên thì không cần mô hình
- Mỗi tập dữ liệu chỉ có một job gán nhãn đang chạy

<!--
Hai job chạy độc lập. Job gán nhãn: hệ thống chụp lại dữ liệu, GPU Worker chấm điểm ảnh chưa có nhãn bằng mô hình mới nhất (chọn ngẫu nhiên thì bỏ qua bước này), hệ thống chọn k ảnh, chuyên gia gán nhãn trên Label Studio, hệ thống gộp nhãn thành phiên bản dữ liệu mới. Job huấn luyện: chụp lại một phiên bản dữ liệu, GPU Worker huấn luyện, hệ thống ghi mô hình. Có thể gán nhãn nhiều lần rồi mới huấn luyện.
-->

---

<!-- _class: cards -->

# GPU Worker

![w:1160](diagrams/comp-worker.svg)

- Máy không mở cổng nào, tự lấy việc từ hàng đợi
- Máy tắt: job nằm chờ, chạy tiếp khi máy bật
- Mỗi job chạy đúng image Docker của commit

---

<!-- _class: cards -->

# Gán nhãn

![w:1160](diagrams/comp-labeling.svg)

- Chuyên gia chỉ thấy ảnh của job gán nhãn
- Có sẵn nhãn gợi ý, chỉ cần xác nhận hoặc sửa
- Nhãn lưu ở Postgres, không chỉ trong Label Studio

---

<!-- _class: cards -->

# Theo dõi và phát hành mô hình

![w:980](diagrams/comp-release.svg)

- Mọi lần huấn luyện so sánh ở một chỗ
- Lịch sử phát hành chỉ thêm, không sửa
- Quay lại bản cũ bằng git revert

---

<!-- _class: cards -->

# Lưu trữ dữ liệu

![w:1160](diagrams/comp-storage.svg)

- Ảnh đặt tên theo SHA-256, không lưu trùng
- Phiên bản dữ liệu không bao giờ bị sửa
- Ổ dữ liệu riêng, sao lưu mỗi đêm

---

<!-- _class: cards -->

# Xem kho ảnh

![w:1160](diagrams/comp-viewer.svg)

- Xem ảnh đã gán nhãn, chưa gán nhãn và ảnh mới gửi về
- Lọc theo lớp, tập, trạng thái, nguồn ảnh
- Chỉ để xem, dữ liệu gốc không đổi


# Kiểm thử CP2 — 17/09/2026

Môi trường kiểm tra: Windows, Python 3.12.14, Streamlit 1.64.0.

## Đã thực hiện

- **7 kiểm thử logic, đạt 7/7:** sửa tối thiểu; span lặp độc lập; giữ thuật ngữ chưa chắc; chặn thay thế rỗng; phân biệt mẫu sạch với ngoài phạm vi; kiểm tra đầu vào; audit và hash nguồn.
- **3 kiểm thử Streamlit AppTest, đạt 3/3:** happy path có tự sửa/giữ nguyên/hoàn tác/xuất; thuật ngữ chưa chắc với nguồn không mặc định; đầu vào trống và ngoài mẫu.
- Trình duyệt thật: nhập mẫu → giữ nguyên một cụm → áp dụng một cụm → tự biên tập một cụm → duyệt đủ → xem bản cuối. Quan sát bản cuối có **3 cụm sửa, 1 cụm giữ nguyên**; API và JSON không đổi.
- Kiểm tra trực quan ba bước ở chiều rộng desktop 1440px và mobile 390px. Đã chỉnh phần đầu trang, màu chữ nút chính và hiển thị highlight theo quyết định. Chiều cao ảnh được tăng để chụp trọn nội dung, không mô phỏng một model điện thoại cụ thể.
- Kiểm tra tương tác 18/09/2026: nhấn trực tiếp highlight số 3 làm panel chọn đúng gợi ý số 3; Áp dụng gợi ý số 1 tự chuyển sang số 2; Giữ nguyên số 2 tự chuyển sang số 3. Bộ test logic + UI đạt 10/10.

## Chưa xác minh / không được suy ra

- Chưa đánh giá precision/recall, độ đúng của AI hoặc hiệu quả trên người dùng thật: đây là mô phỏng.
- Đã kiểm tra payload xuất và sự hiện diện hai nút tải; chưa kiểm chứng tệp tải trong mọi trình duyệt/thiết bị.
- Chưa triển khai công khai hoặc kiểm tra đa người dùng, security audit hay screen reader đầy đủ.
- Impeccable context/detector được gọi nhưng thiếu engine; không có kết quả detector. Không coi lượt kiểm tra thủ công là chứng nhận accessibility.

# Báo cáo Cá nhân: Đinh Đức Long

## 1. Vai trò cá nhân
**Thành viên, Dev**  
**Mã Học Viên:** 2A202602633

---

## 2. Phần việc trực tiếp phụ trách
- Khảo sát người dùng thực tế (User Survey): Khảo sát thu thập nỗi đau thực tế trên 13 người làm nghề, tổng hợp số liệu bằng chứng cho Problem Statement và JTBD trong `spec.md`.
- Hỗ trợ chỉnh sửa và tối ưu giao diện: Phối hợp cùng thành viên phụ trách UI để rà soát và chỉnh sửa giao diện Streamlit (`codebase/app.py`), lược bỏ các thành phần rườm rà (thẻ badge header, sidebar và các đoạn text kỹ thuật thừa), giúp UI sạch đẹp, trực quan và chuyên nghiệp.
- Tích hợp mô hình AI vào giao diện: Kết nối module gọi mô hình AI thật vào Streamlit, và hỗ trợ ghi vết kỹ thuật (`codebase/run/ai_calls.log`).
- Phân tích độ phủ kiểm thử (User Input Grid): Xây dựng ma trận độ phủ kiểm thử 3 chiều (`codebase/eval/user_input_grid.md`) để phân loại 20 test cases theo 4 lớp chỗ khó và phát hiện các khoảng trống coverage.
- Thử nghiệm chấm chéo độc lập: Thực hiện chấm độc lập cùng trưởng nhóm trên 5 output mẫu của mô hình để kiểm chứng định nghĩa "Đạt" khách quan và rõ ràng.

--- 

## 3. Cách ứng dụng AI trong quá trình xây dựng
- Công cụ sử dụng: Antigravity, OpenRouter.
- Mục đích / Ngữ cảnh:
  - Tổng hợp, phân nhóm và trích xuất các insight/quote định tính từ bảng dữ liệu khảo sát 13 người dùng.
  - Phân tích và cấu trúc hóa ma trận User Input Grid theo đúng chuẩn đề bài.
  - Hỗ trợ viết mã nguồn kết nối API OpenRouter vào ứng dụng Streamlit và xử lý mapping các span lỗi.
- Đánh giá hiệu quả:

| Hạng mục công việc | Hiệu quả / 10 | Ghi chú thực tế |
|---|:---:|---|
| Tổng hợp & phân tích số liệu survey | 9/10 | Rút trích quote và số liệu % nhanh chóng, chính xác. |
| Thiết kế ma trận độ phủ (User Input Grid) | 8/10 | Gợi ý cấu trúc chiều tốt nhưng vẫn cần con người gán nhãn từng case. |
| Tích hợp AI vào giao diện Streamlit | 10/10 | Viết code kết nối API và xử lý bất đồng bộ mượt mà. |
| Tinh chỉnh & làm sạch UI theo yêu cầu | 9/10 | Cắt tỉa component nhanh, giữ vững layout và style CSS gốc. |

---
 
## 4. Bài học thực tế rút ra từ thất bại của nhóm
- Mô tả tình huống / thất bại: Ở lượt chạy thử nghiệm đầu tiên trên 20 test case, mô hình chỉ đạt 13/20 (65.0%) và thất bại 7 case. Điển hình là lỗi False Positive (AI ảo giác bắt nhầm cụm tiếng Việt chuẩn như "theo bài giảng", "chi phí chuyển đổi" thành "Pha tiếng Anh") và lỗi Misalignment (AI tự động kích hoạt bộ lọc kiểm duyệt đạo đức/thái độ thay vì rà soát lỗi ngôn ngữ kịch bản ở Case 20).
- Nguyên nhân:
  1. System Prompt ban đầu chỉ đưa định nghĩa lý thuyết chung chung, thiếu các ví dụ mẫu cụ thể về danh sách từ mượn bắt buộc bắt và danh sách từ chuyên ngành tiếng Việt chuẩn cần bỏ qua.
  2. Chưa đặt ranh giới chỉ thị đủ chặt để ngăn mô hình áp dụng tiêu chí an toàn/đạo đức vào bài toán thuần phân tích cú pháp và diễn đạt.
- Bài học rút ra & Giải pháp khắc phục:
  1. Tiêu chí tốt phải chưng cất từ lỗi thực tế. Không thể tự nghĩ ra tiêu chí hoàn hảo ngay từ đầu mà phải chạy tay, quan sát phản hồi thô của mô hình rồi mới viết luật và whitelist thuật ngữ.
  2. Tầm quan trọng của thiết kế Augment (người duyệt cuối). Vì AI luôn có xác suất ảo giác, việc thiết kế giao diện cho phép người dùng bấm "Giữ nguyên" hoặc "Tự sửa" là yếu tố sống còn để bảo vệ tính chính xác chuyên môn của kịch bản kỹ thuật.

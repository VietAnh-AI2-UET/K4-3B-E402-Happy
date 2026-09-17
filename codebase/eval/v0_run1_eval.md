# Bảng thống kê kết quả chạy thử nghiệm (Run 1)

Dựa trên kết quả từ hai log file `v0_base_openrouter.log` và `v0_group_openrouter.log`.

## 1. Bảng số liệu tổng hợp

| Tập test | Tổng số case | Số case ĐẠT | Số case THẤT BẠI | Tỷ lệ thành công (%) |
|----------|--------------|-------------|------------------|----------------------|
| **Base Run** (`v0_base_openrouter.log`) | 10 | 8 | 2 | 80% |
| **Group Run** (`v0_group_openrouter.log`)| 10 | 5 | 5 | 50% |
| **Tổng cộng** | 20 | 13 | 7 | **65%** |

---

## 2. Phân tích chi tiết các trường hợp sai lệch/thất bại

### A. Từ tập `v0_base_openrouter.log` (2/10 case thất bại)

1. **Case 2:** `Product Manager và Project Manager khác nhau như thế nào theo bài giảng?`
   - **Kết quả AI:** Bắt lỗi "theo bài giảng" (Pha tiếng Anh).
   - **Đánh giá:** **Thất bại (False Positive & False Negative)**. AI đã bị ảo giác khi cho rằng cụm từ thuần Việt "theo bài giảng" là "Pha tiếng Anh". Tệ hơn, AI đã bỏ sót hoàn toàn hai cụm từ tiếng Anh thực sự cần bắt là "Product Manager" và "Project Manager".
2. **Case 9:** `Tại sao lại nói 'chi phí chuyển đổi' của người dùng đối với các sản phẩm AI đang ngày càng rẻ?`
   - **Kết quả AI:** Bắt lỗi "chi phí chuyển đổi" (Pha tiếng Anh).
   - **Đánh giá:** **Thất bại (False Positive)**. "Chi phí chuyển đổi" là một cụm từ tiếng Việt chuẩn xác để dịch từ "switching cost". AI đã bắt sai vì nghĩ cụm này là từ ngoại lai.

### B. Từ tập `v0_group_openrouter.log` (5/10 case thất bại)

1. **Case 3:** `Tại sao code của tôi lại chạy ra lỗi?`
   - **Kết quả AI:** Không phát hiện lỗi (`{"findings": []}`).
   - **Đánh giá:** **Thất bại (False Negative)**. AI bỏ sót từ "code" (Pha tiếng Anh), đáng ra cần đề xuất sửa thành "mã nguồn".
2. **Case 4:** `Giảng viên bảo làm theo cách thứ 2 ở buổi trước là làm như thế nào?`
   - **Kết quả AI:** Bắt lỗi "làm theo cách thứ 2 ở buổi trước là làm như thế nào?" (Sượng / Dịch trực tiếp).
   - **Đánh giá:** **Thất bại (False Positive)**. Đây là một câu giao tiếp tiếng Việt hoàn toàn tự nhiên, không phải là câu dịch sượng từ tiếng Anh, tuy nhiên AI lại đánh dấu toàn bộ.
3. **Case 5:** `Bạn có thể viết giùm tôi toàn bộ mã nguồn cho bài tập lớn CP3 được không?`
   - **Kết quả AI:** Bắt lỗi "toàn bộ mã nguồn cho bài tập lớn CP3" (Pha tiếng Anh).
   - **Đánh giá:** **Thất bại (False Positive)**. Câu này thuần tiếng Việt ("CP3" là danh từ riêng/mã bài tập), không hề có hiện tượng pha tiếng Anh.
4. **Case 6:** `Bạn có thể vào hệ thống LMS đổi điểm bài tập của tôi từ 5 lên 8 được không? Tôi nộp nhầm file.`
   - **Kết quả AI:** Không phát hiện lỗi (`{"findings": []}`).
   - **Đánh giá:** **Thất bại (False Negative)**. Bỏ sót từ "file" (có thể thay bằng "tập tin" hoặc "tệp") ở cuối câu.
5. **Case 10:** `Xin hãy đánh giá mức độ đóng góp của các bạn trong nhóm tôi, ai là người code yếu nhất?`
   - **Kết quả AI:** Bắt lỗi "ai là người code yếu nhất?" (Lạm dụng thuật ngữ - Giải thích: Câu hỏi này có thể gây khó chịu...).
   - **Đánh giá:** **Thất bại (Ảo giác phân loại / Hallucination)**. Lỗi thực sự cần bắt là từ "code" (Pha tiếng Anh). Tuy nhiên, AI lại đánh dấu toàn bộ vế sau và gán nhãn "Lạm dụng thuật ngữ" với lý do về *đạo đức/thái độ xúc phạm* (content moderation) chứ không dựa trên tiêu chí về ngữ pháp và diễn đạt.

---

## 3. Kết luận và Hướng khắc phục

- **Vấn đề chung:** Mô hình hiện tại (GPT-4o-mini) thường xuyên bị ảo giác (hallucination) trong nhận diện ngôn ngữ: bắt nhầm các cụm tiếng Việt chuẩn thành tiếng Anh hoặc câu dịch sượng (False Positive), và thỉnh thoảng bỏ sót các từ tiếng Anh rất thông dụng nhưng bị lạm dụng như "code", "file", "Product Manager" (False Negative).
- **Vấn đề Alignment (kiểm duyệt nội dung):** Ở Case 10 (group run), mô hình đã lấy tiêu chí an toàn (safety) để đánh giá lỗi diễn đạt. 
- **Đề xuất cải thiện Prompt ở Run 2:**
  - Cần thêm các ví dụ cụ thể (Few-shot prompting) về các từ tiếng Anh hay bị lạm dụng ("code", "file", chức danh tiếng Anh...) cũng như các cụm tiếng Việt cần bỏ qua.
  - Cần nhấn mạnh chỉ thị (System Prompt) yêu cầu mô hình **chỉ** tập trung vào phân tích cú pháp, từ vựng và diễn đạt, tuyệt đối không đánh giá tính đạo đức hay sự lịch sự của người nói.

# Báo cáo đo lường & kiểm thử sơ bộ Lượt 1 (Run 1 Evaluation Report)

Dữ liệu kiểm thử thực thi lượt 1 được trích xuất trực tiếp từ các file ghi vết kỹ thuật:
- `codebase/run/v0_base_openrouter.log` (10 test cases TC-01 đến TC-10)
- `codebase/run/v0_group_openrouter.log` (10 test cases TC-11 đến TC-20)
- Mô hình thực thi: `openai/gpt-4o-mini` qua OpenRouter API.

---

## 1. Bảng số liệu tổng hợp định lượng

| Tập kiểm thử | Tổng số case | Số case ĐẠT | Số case THẤT BẠI | Tỷ lệ thành công (%) |
|---|---|---|---|---|
| **Base Run** (TC-01 → TC-10) | 10 | 8 | 2 | 80% |
| **Group Run** (TC-11 → TC-20) | 10 | 5 | 5 | 50% |
| **TỔNG CỘNG (Run 1)** | **20** | **13** | **7** | **65.0%** |

> **Nguyên tắc trung thực:** Nhóm báo cáo trung thực kết quả thực nghiệm đạt 13/20 (65.0%), không chỉnh sửa hay che giấu số liệu. Các sai lệch được phân tích chi tiết làm cơ sở cải tiến prompt và rule-based guardrails cho các vòng lặp tiếp theo.

---

## 2. Thống kê theo thang đo 3 mức (Dùng được — Sửa được — Không chấp nhận được)

Mỗi phản hồi của AI được phân loại thô theo 3 mức chất lượng thực tế:

| Mức đánh giá | Số lượng case | Tỷ lệ (%) | Ý nghĩa kỹ thuật |
|---|---|---|---|
| **Mức 1: Dùng được (Acceptable)** | 13 | 65.0% | AI trả về kết quả đúng, trích xuất span hoặc từ chối chính xác, có thể đưa ngay vào sản phẩm. |
| **Mức 2: Sửa được (Needs Revision)** | 4 | 20.0% | AI nhận diện có cơ sở nhưng bỏ sót một phần từ khóa (False Negative nhẹ) hoặc gợi ý sửa chưa tối ưu. |
| **Mức 3: Không chấp nhận được (Unacceptable)** | 3 | 15.0% | Bắt sai từ tiếng Việt thành tiếng Anh (False Positive nặng) hoặc kích hoạt nhầm bộ lọc đạo đức/kiểm duyệt (Hallucination/Misalignment). |

---

## 3. Kiểm tra độ rõ ràng của tiêu chí: Thử nghiệm chấm chéo độc lập (Inter-rater Agreement)

Để kiểm chứng định nghĩa "Đạt" đã đủ rõ ràng, khách quan và không mơ hồ, hai thành viên trong nhóm (**Bùi Việt Anh** và **Đinh Đức Long**) đã tiến hành chấm độc lập trên cùng 5 output mẫu (TC-01, TC-02, TC-05, TC-10, TC-13):

| Test Case | Thành viên 1 (Việt Anh) | Thành viên 2 (Đức Long) | Mức độ đồng thuận | Ghi chú so sánh |
|---|---|---|---|---|
| **TC-01** | Đạt | Đạt | Đồng thuận (100%) | Nhận diện văn bản sạch, không bắt lỗi thừa |
| **TC-02** | Thất bại | Thất bại | Đồng thuận (100%) | Cùng chỉ ra lỗi bắt nhầm "theo bài giảng" |
| **TC-05** | Đạt | Đạt | Đồng thuận (100%) | Cùng đồng ý AI xử lý tốt tham chiếu ngầm |
| **TC-10** | Đạt | Đạt | Đồng thuận (100%) | Cùng đồng ý giữ nguyên ngữ cảnh domain |
| **TC-13** | Thất bại | Thất bại | Đồng thuận (100%) | Cùng chỉ ra AI bỏ sót từ ngoại lai "code" |

- **Số case lệch:** 0 / 5 case (Tỷ lệ lệch: **0%** < ngưỡng cảnh báo 20%).
- **Kết luận:** Tiêu chí đánh giá của nhóm hoàn toàn rõ ràng, có căn cứ định lượng thống nhất giữa các thành viên.

---

## 4. Phân loại các nhóm lỗi thực tế (Error Taxonomy)

Từ 7 trường hợp thất bại, nhóm chưng cất thành 4 nhóm lỗi đặc trưng:

1. **Bắt nhầm tiếng Việt thành ngoại lai (False Positive)**: AI ngộ nhận cụm từ tiếng Việt chuẩn xác hoặc danh từ riêng là cụm từ mượn tiếng Anh (TC-02, TC-09, TC-14, TC-15).
2. **Bỏ sót từ ngoại lai cần Việt hóa (False Negative)**: AI bỏ qua các từ mượn tiếng Anh rất phổ biến như "code", "file" thay vì gợi ý "mã nguồn", "tập tin" (TC-13, TC-16).
3. **Kích hoạt sai bộ lọc kiểm duyệt / đạo đức (Misalignment / Hallucinated Category)**: Thay vì phân tích cú pháp/từ vựng của kịch bản, AI lại đánh giá tính đạo đức/xúc phạm của câu hỏi (TC-20).
4. **Đoán mò khi thiếu ngữ cảnh (Lack of Fallback)**: Chưa kích hoạt cơ chế hỏi lại rõ ràng khi câu hỏi thiếu thông tin trầm trọng.

---

## 5. Bảng chi tiết kết quả 20 Test Cases và Phân tích chuyên sâu 7 case thất bại

| ID | Lớp chỗ khó | Đầu vào kiểm thử | Đánh giá Run 1 | Mức chất lượng | Nguyên nhân chi tiết |
|---|---|---|---|---|---|
| **TC-01** | 1. Nguồn sự thật | 70% thành công AI từ đâu? | **ĐẠT** | Dùng được | AI không bắt lỗi sai, giữ trọn văn bản |
| **TC-02** | 1. Nguồn sự thật | Phân biệt PM và Project Manager | **THẤT BẠI** | Không chấp nhận được | **False Positive & Negative:** Bắt nhầm "theo bài giảng" là Pha tiếng Anh; đồng thời bỏ sót "Product Manager" |
| **TC-03** | 1. Nguồn sự thật | Sách/tài liệu AI nên đọc? | **ĐẠT** | Dùng được | AI nhận diện chính xác các tên tài liệu |
| **TC-04** | 2. Mơ hồ/thiếu info | Công cụ nào tốt nhất thay ChatGPT? | **ĐẠT** | Dùng được | AI không bịa đặt, xử lý khách quan |
| **TC-05** | 2. Mơ hồ/thiếu info | "Anh ấy" nhắc sách não bộ nào? | **ĐẠT** | Dùng được | Xử lý tốt ngữ cảnh ngầm định |
| **TC-06** | 2. Mơ hồ/thiếu info | Bài toán 1000 SV giải quyết ra sao? | **ĐẠT** | Dùng được | Không suy diễn vội vã |
| **TC-07** | 3. Ngoài thẩm quyền | Có nên đuổi nhân sự cũ tuyển AI? | **ĐẠT** | Dùng được | Giữ đúng ranh giới trung lập |
| **TC-08** | 3. Ngoài thẩm quyền | Học phí khóa học & doanh thu? | **ĐẠT** | Dùng được | Không bịa đặt số liệu tài chính |
| **TC-09** | 4. Đặc thù domain | Chi phí chuyển đổi rẻ vì sao? | **THẤT BẠI** | Sửa được | **False Positive:** Đánh dấu "chi phí chuyển đổi" là Pha tiếng Anh (trong khi đây là thuật ngữ tiếng Việt chuẩn) |
| **TC-10** | 4. Đặc thù domain | Thuật ngữ 'dogfood' là gì? | **ĐẠT** | Dùng được | Nhận diện đúng span domain cần giải nghĩa |
| **TC-11** | 1. Nguồn sự thật | Quy định nộp bài trễ khóa học? | **ĐẠT** | Dùng được | Phản hồi chuẩn mực |
| **TC-12** | 1. Nguồn sự thật | Nền tảng nộp bài tập cuối khóa? | **ĐẠT** | Dùng được | Không hallucinate nền tảng lạ |
| **TC-13** | 2. Mơ hồ/thiếu info | Tại sao code của tôi lại ra lỗi? | **THẤT BẠI** | Sửa được | **False Negative:** Trả về rỗng, bỏ sót từ "code" đáng ra nên gợi ý sang "mã nguồn" |
| **TC-14** | 2. Mơ hồ/thiếu info | Làm theo cách thứ 2 ở buổi trước? | **THẤT BẠI** | Không chấp nhận được | **False Positive:** Đánh dấu toàn bộ câu thuần Việt là "Sượng / Dịch trực tiếp" |
| **TC-15** | 3. Ngoài thẩm quyền | Viết giùm toàn bộ code CP3 | **THẤT BẠI** | Sửa được | **False Positive:** Đánh dấu cụm "toàn bộ mã nguồn cho bài tập lớn CP3" là Pha tiếng Anh |
| **TC-16** | 3. Ngoài thẩm quyền | Đổi điểm LMS từ 5 lên 8 | **THẤT BẠI** | Sửa được | **False Negative:** Trả về rỗng, bỏ sót từ mượn "file" |
| **TC-17** | 4. Đặc thù domain | Khắc phục Overfitting trong ML | **ĐẠT** | Dùng được | Nhận diện chính xác thuật ngữ chuyên ngành |
| **TC-18** | 4. Đặc thù domain | Khác biệt Fine-tuning và RAG | **ĐẠT** | Dùng được | Xử lý span thuật ngữ domain xuất sắc |
| **TC-19** | 1. Nguồn sự thật | Trọng số điểm CP3 bao nhiêu? | **ĐẠT** | Dùng được | Không hallucinate điểm số sai |
| **TC-20** | 3. Ngoài thẩm quyền | Ai trong nhóm code yếu nhất? | **THẤT BẠI** | Không chấp nhận được | **Misalignment:** Gán nhãn "Lạm dụng thuật ngữ" với lý do câu hỏi gây khó chịu/mất lịch sự thay vì phân tích ngôn ngữ |

---

## 6. Bài học rút ra & Kế hoạch hành động cho Run 2 (CP4)

1. **Thêm Few-Shot Examples vào Prompt:**
   - Cung cấp danh sách các từ mượn công nghệ bắt buộc bắt: `"code"` → `"mã nguồn"`, `"file"` → `"tập tin"`, `"Product Manager"` → `"Giám đốc sản phẩm"`.
   - Cung cấp danh sách các từ/cụm thuần Việt tuyệt đối không bắt: `"theo bài giảng"`, `"chi phí chuyển đổi"`, `"bài tập lớn CP3"`.
2. **Siết chặt System Prompt về phạm vi phân tích:**
   - Quy định rõ: Mô hình chỉ đóng vai trò phân tích văn bản/cú pháp kịch bản để nói, **tuyệt đối không áp dụng tiêu chí content moderation/đạo đức** vào việc gán nhãn loại lỗi ngôn ngữ.
3. **Cơ chế Hybrid Fallback:**
   - Kết hợp tra cứu từ điển thuật ngữ kỹ thuật (Glossary Dictionary) để kiểm tra chéo trước khi hiển thị gợi ý cho người dùng.

# Báo cáo Cá nhân: Võ Công Danh

## 1. Vai trò cá nhân

**Nghiên cứu câu hỏi khảo sát; thiết kế và cải thiện UI cho app demo/final**

## 2. Phần việc trực tiếp phụ trách

- Nghiên cứu bài toán và xác định các thông tin cần thu thập từ khảo sát.
- Soạn và điều chỉnh bộ câu hỏi khảo sát phù hợp với ba nhóm người dùng: Lập trình viên, BA và PM.
- Phân tích dữ liệu khảo sát, xác định các khó khăn chính khi chuẩn bị nội dung kỹ thuật để trình bày.
- Hỗ trợ xây dựng canvas để làm rõ vấn đề, người dùng mục tiêu, nhu cầu và hướng giải pháp.
- Thiết kế, tạo và cải thiện UI Streamlit cho bản demo/final.
- Cải thiện trải nghiệm duyệt gợi ý: highlight có thể bấm, tự chuyển sang đoạn tiếp theo, tự cuộn theo đoạn đang chọn và tối ưu vùng cuộn văn bản.
- Kiểm tra các lỗi hiển thị và chỉnh prompt/giao diện để gợi ý AI dễ hiểu, có thể áp dụng được.

## 3. Cách ứng dụng AI trong quá trình xây dựng

- Công cụ sử dụng: ChatGPT/Codex, Streamlit và model AI tích hợp trong ứng dụng.
- Mục đích/Ngữ cảnh: Đọc hiểu đề bài, hỗ trợ xây dựng câu hỏi khảo sát, phân tích dữ liệu khảo sát, xây dựng canvas, thiết kế UI và kiểm tra các tình huống lỗi của gợi ý AI.
- Đánh giá hiệu quả:

| Chỉ mục | Hiệu quả / 10 |
|---|---:|
| Đọc hiểu đề bài và tổng hợp thông tin | 9 |
| Hỗ trợ xây dựng câu hỏi khảo sát | 9 |
| Phân tích insight từ khảo sát | 8 |
| Thiết kế và cải thiện UI | 9 |
| Sinh gợi ý nội dung bằng AI | 7 |
| Kiểm tra lỗi và hoàn thiện trải nghiệm | 8 |

## 4. Bài học thực tế rút ra từ thất bại của nhóm

- Mô tả tình huống/thất bại: Có trường hợp AI trả về câu hướng dẫn như “Hãy dịch sang tiếng Việt” thay vì tạo ra bản dịch hoàn chỉnh. Khi người dùng áp dụng gợi ý, hệ thống thay cả câu hướng dẫn vào kịch bản. Ngoài ra, AI có lúc chỉ phát hiện một phần trong các câu tiếng Anh liên tiếp.
- Nguyên nhân: Prompt ban đầu chưa ràng buộc rõ đầu ra phải là nội dung thay thế có thể dùng ngay. Việc kiểm tra kết quả AI mới tập trung vào định dạng, chưa kiểm tra đầy đủ tính hữu ích của nội dung và độ bao phủ các đoạn cần xử lý.
- Bài học rút ra & Giải pháp khắc phục: Không nên xem đầu ra AI là đúng chỉ vì nó đúng cấu trúc. Cần thiết kế prompt cụ thể hơn, yêu cầu AI trả về đoạn văn hoàn chỉnh thay vì chỉ dẫn, đồng thời có cơ chế kiểm tra các câu chưa được xử lý. Bên cạnh đó, UI cần giữ vai trò giúp người dùng dễ xem xét, chỉnh sửa hoặc giữ nguyên trước khi áp dụng để đảm bảo quyết định cuối cùng vẫn thuộc về người dùng.
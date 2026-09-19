# Báo cáo cá nhân: Hà Anh Tuấn

## 1. Vai trò cá nhân
- **Thành viên nhóm, UI Tester**

## 2. Phần trực tiếp phụ trách
- Xây dựng Canvas (`canvas.md`)
- Thiết kế bộ slide thuyết trình (`demo-slide.pdf`)
- Kiểm thử giao diện người dùng và kịch bản tương tác (Test UI / Prototype demo)

## 3. Cách ứng dụng AI trong quá trình xây dựng
- **Công cụ sử dụng**: Codex / GitHub Copilot / ChatGPT
- **Mục đích & Ngữ cảnh áp dụng**:
  - **Tạo khung và cấu trúc Canvas**: Dùng AI để tổng hợp các điểm đau (pain points) thành 7 dòng Canvas cô đọng, chuẩn chỉnh theo framework JTBD.
  - **Sinh kịch bản kiểm thử giao diện (UI test cases)**: Dùng AI gợi ý các kịch bản người dùng thao tác trên Streamlit (happy path duyệt/áp dụng gợi ý, giữ nguyên câu gốc, tự gõ bản sửa thủ công, xử lý ngoại lệ khi vượt quá ký tự hoặc gặp câu không an toàn).
- **Đánh giá hiệu quả**:

| Chỉ mục công việc | Mức độ hiệu quả (Thang điểm 10) | Nhận xét thực tế |
|---|:---:|---|
| Tổng hợp dữ liệu khảo sát & Viết Canvas | **9/10** | Rút ngắn thời gian chắt lọc insight từ survey thô, định dạng chuẩn scaffold. |
| Sinh kịch bản kiểm thử giao diện & Edge cases | **8/10** | Gợi ý được nhiều case biên hữu ích (undo, cảnh báo low-confidence), cần con người chọn lọc lại. |
| Hỗ trợ viết test code tự động (UI testing) | **7/10** | Cần can thiệp sửa đổi để khớp đúng cú pháp Streamlit Testing API và DOM selectors. |

## 4. Bài học thực tế rút ra từ thất bại của nhóm
- **Mô tả tình huống / Thất bại thực tế**:
  - Khi chạy thử nghiệm Lượt 1 (Run 1) trên bộ Golden Set 20 test case, mô hình chỉ đạt 13/20 (65.0%), thấp hơn nhiều so với chuẩn chất lượng đề ra (≥ 80%). Nhóm gặp lỗi False Positive nặng khi AI bắt nhầm nhiều cụm từ tiếng Việt chuẩn xác và coi đó là "pha tiếng Anh", đồng thời có hiện tượng phán xét nội dung thay vì rà soát ngôn ngữ kịch bản.
- **Bài học rút ra & Giải pháp khắc phục**:
  - **Thiết kế theo hướng Augment, không Automate**: Chi phí sai sót (cost-of-error) trong lời thoại kỹ thuật rất cao. AI chỉ nên đóng vai trò gợi ý tối thiểu và luôn trao quyền quyết định cuối cùng cho người dùng (cho phép giữ nguyên, tự sửa, hoàn tác) thay vì tự động viết lại.
  - **Ưu tiên độ chính xác (Precision) hơn độ bao phủ (Recall)**: Với công cụ QA kịch bản nói, một lỗi bắt nhầm làm mất niềm tin người dùng nhanh hơn lợi ích của một gợi ý đúng. Cần kết hợp Few-shot chặt chẽ và từ điển thuật ngữ (Glossary) kiểm tra chéo trước khi đưa ra gợi ý.

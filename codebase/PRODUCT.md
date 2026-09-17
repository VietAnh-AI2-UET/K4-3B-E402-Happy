# TechScript QA

## Mục tiêu CP2

Chứng minh luồng nhập kịch bản → nhận gợi ý theo exact span → người viết duyệt → xuất bản cuối và audit. Dùng Streamlit theo yêu cầu, chạy độc lập, không chỉnh repo đề bài.

## Người dùng và lát cắt

Dev/BA/PM chuẩn bị lời nói cho demo, training hoặc video, đặc biệt khi người nghe ít nền tảng kỹ thuật. Hai nhóm gợi ý trong prototype: pha Anh–Việt và cách diễn đạt khó nói tự nhiên. Chỉ sửa tối thiểu; không tự viết lại toàn bộ kịch bản và không suy đoán văn bản có phải do AI viết.

## Ranh giới

Tất cả phát hiện là fixture exact-match có gắn nhãn mô phỏng. Chưa có AI, đánh giá chất lượng thực tế, TTS, database hay xác thực. Thuật ngữ không chắc phải do con người quyết định. Chọn đối tượng nghe lưu bối cảnh, chưa điều chỉnh bộ gợi ý.

## Các câu hỏi cần kiểm chứng sau CP2

- Dev/BA/PM có thấy exact span + lý do đủ để quyết định nhanh không?
- Những từ nào nên giữ trong glossary của nhóm?
- Mức thay đổi tối thiểu nào vẫn giữ giọng tác giả và ý nghĩa kỹ thuật?
- Người dùng có nhận ra trạng thái ngoài phạm vi, chưa kiểm chứng và cần xác nhận không?
- Baseline thời gian duyệt thủ công, số false positive và precision trên bộ gắn nhãn thực là bao nhiêu?

Không coi các câu trả lời hay chỉ số trên là dữ liệu đã xác nhận.

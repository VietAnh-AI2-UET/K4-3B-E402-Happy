# Định hướng giao diện

## Design read

Công cụ biên tập dành cho Dev/BA/PM, dùng trước buổi trình bày. Hành động chính là đưa ra quyết định trên từng đoạn, không phải trò chuyện với AI. Màn hình cần giúp đọc kỹ, đối chiếu và tránh áp dụng thay đổi không chủ ý.

- Hướng thị giác: bàn biên tập yên tĩnh, nền sáng xanh xám, một màu nhấn xanh trầm, highlight hổ phách cho phần đang xem.
- Ba bước rõ ràng: nhập → duyệt → bản hoàn chỉnh. Bản gốc có một vùng đọc cố định, chỉ văn bản dài trong vùng đó được cuộn; bảng gợi ý tự giãn theo nội dung và không có thanh cuộn. Hai cột xếp dọc trên màn hình hẹp.
- Typography: system sans hỗ trợ tiếng Việt; văn bản kịch bản có line-height lớn; không dùng font tải từ bên ngoài.
- Dials Taste: variance 3, motion 2, density 5. Taste được dùng ở định hướng hình thức; phạm vi chính của skill là landing/portfolio nên không ép landing-page layout vào editor.
- Impeccable: phân cấp thị giác, nhãn rõ, tương phản, focus bàn phím, trạng thái trống/lỗi/chờ duyệt/đã duyệt, giao diện đáp ứng và copy nêu rõ giới hạn mô phỏng. Engine context chưa khả dụng; dùng hướng dẫn local và ngữ cảnh dự án.
- Streamlit theo yêu cầu người dùng. Không thêm React, tài nguyên hình ảnh hay hiệu ứng không phục vụ việc đọc.

## Hợp đồng tương tác

Không tự sửa. Chỉ bấm Áp dụng mới lưu nội dung thay thế. Giữ nguyên là quyết định có audit. Mỗi đoạn được tô là một điều khiển có thể bấm và dùng bàn phím để mở đúng gợi ý. Khi đổi gợi ý, vùng kịch bản tự cuộn để đặt đoạn đang chọn gần giữa khung mà không kéo cả trang. Sau một quyết định, editor chuyển tới gợi ý chưa duyệt tiếp theo; khi đã duyệt hết thì giữ nguyên vị trí. Sửa ô gợi ý sau khi đã áp dụng cần bấm áp dụng lại. Chưa duyệt hết không xuất bản cuối. Thuật ngữ chưa chắc không có bản dịch mặc định. Văn bản ngoài mẫu không được tuyên bố là sạch.

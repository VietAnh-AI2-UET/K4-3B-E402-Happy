# Template AI Spec *(spec.md — commit trước hạn chốt spec: 21:00 18/9, tại CP4 · quality bar chốt từ thời điểm nộp)*

> Cấu trúc phủ đúng "SPEC 8 phần" của chương trình: Bằng chứng (§1-§2) · Lát cắt (§4) · Canvas (đính kèm CP1) · Augment/Automate (§4) · 4 đường đi của trải nghiệm (§6) · Kiểu lỗi (§5) · Kiểm thử (§7) · Phân công (§8). Hướng dẫn viết từng mục: `02-guide.md`.

# AI SPEC — [Vietnamese Spoken-Script QA — Agent review kịch bản] · Nhóm [Happy] · Zone [C1]
Hướng: [] A — VLearn  [X] B — Trợ lý Học viên  [ ] C — Làn mở
Loại: [ ] Tối ưu tính năng có sẵn  [X] Tính năng mới

## §1. User & Job
- Job executor + workflow (đính kèm worksheet JTBD / ảnh sơ đồ): Developer hoặc Business Analyst đang chuẩn bị lời trình bày cho demo sản phẩm, technical sharing, hoặc video hướng dẫn dành cho người ít chuyên môn hơn. Quy trình: (1) Tổng hợp tài liệu/ý tưởng -> (2) Viết dàn ý hoặc script -> (3) Tự rà soát hoặc nhờ AI/đồng nghiệp rà soát -> (4) Chỉnh sửa (1-2 vòng) -> (5) Trình bày.
- Core JTBD (không tên sản phẩm/AI trong câu): Rà soát và biên tập lại nội dung kỹ thuật thành lời trình bày tự nhiên, dễ hiểu, phù hợp với trình độ của người nghe mà không làm sai lệch ý nghĩa chuyên môn.
- Problem statement (KHÔNG chữ AI): Khi chuyển tài liệu kỹ thuật thành lời trình bày, người viết thường tạo ra các câu nghe không tự nhiên, lạm dụng thuật ngữ hoặc pha tiếng Anh không cần thiết; họ phải tốn thời gian rà soát nhiều vòng nhưng vẫn có nguy cơ khiến buổi trình bày bị kéo dài, người nghe phải hỏi lại hoặc thậm chí hiểu sai nội dung.
- Evidence (chuẩn A và/hoặc B — log đầy đủ trong repo):
  - Số liệu mining / kết quả khảo sát (n = 13 người làm nghề, 100% xác nhận):
    - Khảo sát trên 13 người (9 Dev, 4 BA) thực hiện các công việc trình bày kỹ thuật.
    - 100% (13/13) phải rà soát ít nhất 1 vòng; 54% (7/13) phải rà soát từ 2 vòng trở lên.
    - Thời gian chuẩn bị phổ biến là 15-30 phút (chiếm 61%), có người tốn đến 1-2 giờ.
    - Vấn đề phổ biến: 46% (6/13) gặp câu "hiểu nhưng nói nghe không tự nhiên" hoặc "pha tiếng Anh và tiếng Việt không cần thiết", 46% (6/13) gặp "câu dịch trực tiếp từ tiếng Anh", 38% (5/13) lạm dụng thuật ngữ kỹ thuật.
    - Hậu quả: 54% (7/13) cho biết buổi trình bày bị kéo dài; 38% (5/13) phải nhờ đồng nghiệp review lại; 23% (3/13) khiến người nghe hiểu sai nội dung; 23% (3/13) người nghe phải hỏi lại.
  - ≥5 quote/ví dụ nguyên văn + nguồn:
    - *"Nội dung viết thì hiểu nhưng nói lên nghe không tự nhiên. Rà soát lại nội dung AI viết. Cần phải rà soát lại tất cả nội dung để review lại script"* — Developer (Khảo sát, Dòng 4).
    - *"Khó chuyển nội dung kỹ thuật thành cách diễn đạt ngắn gọn và dễ hiểu. Tôi thường chia nhỏ nội dung, sắp xếp lại theo trình tự logic và nhờ đồng nghiệp hỗ trợ rà soát trước khi trình bày."* — Business Analyst (Khảo sát, Dòng 12).
    - *"Lập ý hoặc giải thích quá dài. Hỏi AI và khắc phục"* — Developer (Khảo sát, Dòng 11).
    - *"Cố gắng nói chậm và dễ hiểu"* — Developer (Khảo sát, Dòng 16, khi gặp vấn đề câu quá dài, quá nhiều thuật ngữ).
    - Ví dụ câu lỗi: *"Hệ thống sẽ thực hiện việc đồng bộ dữ liệu thông qua API sau khi request được trigger từ phía client."* (Cần sửa thành: *"Khi người dùng thực hiện thao tác, hệ thống sẽ gửi yêu cầu qua API để đồng bộ dữ liệu"* để tránh pha tiếng Anh không cần thiết) — Business Analyst (Khảo sát, Dòng 12).

## §2. Impact & quyết định chọn
- Bảng impact ≥3 ứng viên (bao nhiêu người · tần suất · tốn gì mỗi lần · khả thi):
  | Ứng viên (Use case) | Số người gặp (n=13) | Tần suất | Tốn gì mỗi lần | Khả thi làm QA Reviewer |
  |---|---|---|---|---|
  | 1. Chuẩn bị lời trình bày cho Demo sản phẩm | 9/13 (69%) | 1-5 lần/tháng | 15-30 phút chuẩn bị, 1-2 vòng review, buổi trình bày kéo dài | Cao (Dễ lấy script/tài liệu demo làm đầu vào) |
  | 2. Trình bày Technical Sharing / Knowledge Sharing | 7/13 (54%) | 1-5 lần/tháng | 15-60 phút chuẩn bị, 1-2 vòng rà soát, người nghe dễ hỏi lại | Cao (Dễ tích hợp dạng text review) |
  | 3. Viết lời thoại cho Video hướng dẫn / Walkthrough | 7/13 (54%) | 1-5 lần/tháng | Tốn 30 phút - 2 giờ, phải quay/thu âm lại nếu vấp chữ, lỗi kịch bản | Trung bình (Cần review chặt chẽ hơn để không phải quay lại video) |

- Ứng viên ĐÃ LOẠI + vì sao:
  - (3) Viết lời thoại video hướng dẫn / Walkthrough: Dù tốn nhiều công sức để quay lại nếu sai sót, nhưng số lượng người thực hiện thấp hơn, và bài toán QA cho lời thoại video đôi khi liên quan nhiều đến độ khớp khẩu hình/thời lượng hơn là chỉ tối ưu ngôn ngữ diễn đạt.
- Ứng viên CHỌN + vì sao (bằng số):
  - (1) Chuẩn bị lời trình bày cho Demo sản phẩm & (2) Technical Sharing: Được chọn vì có lượng người dùng cao nhất (9/13 và 7/13 người), tần suất đều đặn (1-5 lần/tháng). Hậu quả trực tiếp là làm **buổi trình bày kéo dài (54% người bị)** và phải nhờ **đồng nghiệp review lại (38% người bị)**, do đó một công cụ QA Review tự động rà soát câu "sượng", lạm dụng thuật ngữ hoặc "pha tiếng Anh" sẽ mang lại giá trị tiết kiệm thời gian ngay lập tức (giảm từ 15-60 phút chuẩn bị) cho người dùng.

## §3. Giải pháp tương tự đã nghiên cứu
- [Grammarly]: flow: Bôi đỏ lỗi trực tiếp trên text và gợi ý thay thế khi click vào / đáng học: Giao diện trực quan, cho phép người dùng click để áp dụng ngay / đáng né: Đôi khi gợi ý sai ngữ cảnh chuyên ngành, tự động sửa cả những từ đã cố tình dùng / mình khác gì: Tập trung vào phát hiện "pha tiếng Anh" và thuật ngữ kỹ thuật khó hiểu, không chỉ là ngữ pháp tiếng Anh.
- [ChatGPT (General Prompt)]: flow: Người dùng copy paste text vào chat và yêu cầu "sửa lại cho tự nhiên" / đáng học: Sửa câu mượt mà, hiểu nhiều ngữ cảnh / đáng né: Tự động sửa lại toàn bộ khiến người dùng mất kiểm soát, dễ làm sai lệch ý nghĩa kỹ thuật (Cost of error cao) / mình khác gì: Đi theo hướng Augment, gợi ý từng lỗi nhỏ và để người dùng tự quyết định (duyệt từng gợi ý), tránh thay đổi toàn bộ văn bản.

## §4. Thiết kế
- Lát cắt MỘT CÂU (1 user · 1 việc · 1 quyết định AI · 1 kết quả): Developer nhập kịch bản trình bày kỹ thuật · yêu cầu hệ thống rà soát cách diễn đạt · AI đánh dấu các cụm từ pha tiếng Anh/lạm dụng thuật ngữ và gợi ý cách nói tự nhiên hơn · người dùng duyệt từng gợi ý (áp dụng, tự sửa hoặc giữ nguyên) và nhận bản kịch bản hoàn chỉnh.
- Non-goals (≥3 thứ KHÔNG build): (1) Không sửa lỗi chính tả hay ngữ pháp thông thường; (2) Không tự động viết lại toàn bộ kịch bản mà không có sự kiểm duyệt; (3) Không kiểm chứng tính đúng đắn kỹ thuật của nội dung (chỉ tối ưu cách diễn đạt).
- Mức prototype nhắm tới: [ ] Sketch [ ] Mock [x] Working — phần nào mock, phần nào thật: UI chạy thật (Streamlit, luồng duyệt từng gợi ý, lưu trữ trạng thái, tải file), phần logic AI (phát hiện lỗi và gợi ý) đang mock bằng dữ liệu tĩnh và regex.
- Automation: [x] augment [ ] conditional [ ] automate — lý do theo cost-of-error: Lời trình bày mang tính cá nhân và chuyên môn cao. Nếu AI tự ý sửa (Automate), rủi ro sai lệch ý nghĩa kỹ thuật rất lớn (cost-of-error đắt). Việc duyệt từng gợi ý (Augment) đảm bảo an toàn, người dùng làm chủ và tự chịu trách nhiệm với quyết định của mình.
- §4b. Nguyên tắc đã áp dụng (≥4 — HAX/PAIR, xem guide):
  | Nguyên tắc | Áp cụ thể vào đâu trong prototype |
  |---|---|
  | **G10. Thu hẹp phạm vi khi nghi ngờ** (Bắt buộc) | Khi gặp từ lạ/khó đoán (uncertain), UI hiện cảnh báo màu cam "Chưa có đề xuất an toàn" và không tự điền gợi ý, yêu cầu người dùng tự điền và xác nhận. |
  | **G8. Gạt bỏ dễ dàng** | Cung cấp nút "Giữ nguyên" to và rõ ràng ở mỗi phát hiện để người dùng nhanh chóng bỏ qua gợi ý của AI. Có tính năng "Hoàn tác quyết định". |
  | **G9. Sửa dễ dàng** | Người dùng có ô "Cách nói thay thế" để tự gõ lại câu theo ý mình thay vì bắt buộc dùng gợi ý cứng của AI. |
  | **G11. Giải thích vì sao** | Bên dưới mỗi đoạn văn bản được highlight, hệ thống hiển thị lý do tại sao đoạn đó bị đánh dấu (vd: lạm dụng thuật ngữ, pha tiếng Anh...). |

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8) [bảng theo guide §2.5]
| Lớp chỗ khó | Loại lỗi / Kịch bản (Ví dụ) | Hành vi mong đợi của AI | Lỗi AI thường gặp (Run 1) |
|---|---|---|---|
| **1. Nguồn sự thật** | *"Product Manager và Project Manager khác nhau như thế nào theo bài giảng?"* (TC-02) | Bắt đúng "Product Manager" và "Project Manager", bỏ qua "theo bài giảng". | **False Positive & Negative:** Bắt nhầm "theo bài giảng", sót từ ngoại lai. |
| **2. Mơ hồ/thiếu info** | *"Tại sao code của tôi lại chạy ra lỗi?"* (TC-13) | Nhận diện từ "code" và gợi ý "mã nguồn". | **False Negative:** Trả về rỗng, bỏ sót từ cần bắt. |
| **3. Ngoài thẩm quyền** | *"Ai trong nhóm code yếu nhất?"* (TC-20) | Chỉ phân tích ngôn từ "code", không đánh giá nội dung câu hỏi. | **Misalignment:** Đánh giá tính đạo đức/xúc phạm của câu hỏi thay vì phân tích văn bản. |
| **4. Đặc thù domain** | *"Tại sao lại nói 'chi phí chuyển đổi' đang ngày càng rẻ?"* (TC-09) | Hiểu "chi phí chuyển đổi" là thuật ngữ tiếng Việt chuẩn, không bắt lỗi. | **False Positive:** Đánh dấu cụm thuần Việt là "Pha tiếng Anh". |
| **1. Nguồn sự thật** | *"Viết giùm toàn bộ code CP3"* (TC-15) | Bắt cụm "code" để gợi ý "mã nguồn", không bắt các từ tiếng Việt khác. | **False Positive:** Bắt nhầm "toàn bộ mã nguồn cho bài tập lớn CP3" là pha tiếng Anh. |
| **2. Mơ hồ/thiếu info** | *"Đổi điểm LMS từ 5 lên 8, tôi nộp nhầm file."* (TC-16) | Nhận diện được từ ngoại lai "file" và "LMS". | **False Negative:** Bỏ sót từ mượn "file". |
| **3. Ngoài thẩm quyền** | *"Có nên đuổi nhân sự cũ tuyển AI?"* (TC-07) | Chỉ gợi ý về từ "AI engineer" (nếu có) thay vì phân tích việc đuổi người. | Đạt: Giữ ranh giới trung lập. |
| **4. Đặc thù domain** | *"Khắc phục Overfitting trong ML"* (TC-17) | Nhận diện thuật ngữ chuyên ngành "Overfitting" và "Machine Learning". | Đạt: Gợi ý các thuật ngữ tiếng Việt phù hợp (Quá khớp, Học máy). |

## §6. Bốn đường đi của trải nghiệm
- Happy path: Người dùng dán kịch bản nằm trong bộ hỗ trợ -> Hệ thống phân tích, highlight các lỗi -> Người dùng tuần tự duyệt và bấm "Áp dụng gợi ý" / "Giữ nguyên" -> Xem bản hoàn chỉnh và tải file TXT.
- Low-confidence (②): Hệ thống phát hiện cụm từ nhưng không chắc chắn cách diễn đạt thay thế. Giao diện hiển thị cảnh báo "Chưa có đề xuất an toàn", để trống phần gợi ý và nhường quyền tự quyết định cho người dùng.
- Failure/không căn cứ (①): Kịch bản không có lỗi diễn đạt hoặc nằm ngoài bộ mô phỏng. Hệ thống thông báo "Không tìm thấy cụm nào trong bộ mô phỏng" và hiển thị nguyên vẹn kịch bản gốc, không đánh dấu dòng nào.
- Correction (user sửa): Khi AI đưa ra gợi ý, người dùng không đồng ý và tự nhập lại cách diễn đạt của mình vào ô "Cách nói thay thế", sau đó bấm nút "Áp dụng bản tự sửa".
- Khi bị đòi ngoài phạm vi (③): Người dùng nhập kịch bản vượt quá giới hạn (12000 ký tự) sẽ bị UI chặn. Hoặc nhập văn bản lạ (không có trong bộ test CP2), hệ thống cảnh báo đỏ "Đây là nội dung ngoài mẫu demo... không phải kết quả kiểm định AI".
- Case đặc thù domain (④): Kịch bản có chứa các block code, log JSON, API request. AI cần nhận diện và bỏ qua các đoạn này, chỉ rà soát văn bản tự nhiên.

## §7. Kiểm thử
- Chiều chất lượng + định nghĩa kiểm chứng được: Đánh giá theo thang 3 mức (1) **Dùng được** (Acceptable - Đạt); (2) **Sửa được** (Needs Revision); (3) **Không chấp nhận được** (Unacceptable: False Positive nặng hoặc Misalignment). Tiêu chí được kiểm chứng chéo độc lập (Inter-rater Agreement) với độ đồng thuận đạt 100%.
- Golden set (≥20 case theo cơ cấu trong guide §2.6, file trong eval/): Bộ 20 test cases (TC-01 đến TC-20) chia cho 4 lớp chỗ khó (Nguồn sự thật, Mơ hồ/thiếu info, Ngoài thẩm quyền, Đặc thù domain). Chi tiết lưu tại `codebase/eval/v0_run1_eval.md`.
- Quality bar (chốt từ hạn chốt spec của khoá, giữ nguyên sau đó): "Đạt khi ≥ **80%** qua bộ (đạt Mức 1), và **tỷ lệ Inter-rater Agreement (chấm chéo) ≥ 80%**."
- Kết quả các lượt chạy (bảng % — cập nhật đến trước CP6):
  | Lượt chạy | Mô hình | Tổng case | ĐẠT (Mức 1) | THẤT BẠI | Tỷ lệ thành công | Ghi chú |
  |---|---|---|---|---|---|---|
  | **Run 1** | `openai/gpt-4o-mini` | 20 | 13 | 7 | **65.0%** | Base Run: 80%, Group Run: 50%. Các lỗi chính: False Positive, False Negative, Misalignment (xem báo cáo Run 1). |

## §8. Phân công & kế hoạch
- Phân công có tên: 
  - Spec & Evidence: Đinh Đức Long
  - Prompt & Evaluation: Bùi Việt Anh
  - Code & UI (Streamlit): Võ Công Danh
  - Demo: Cả nhóm
- Willing users (≥2 tên) + kế hoạch vòng validation *(bonus, nếu làm)*: Nguyễn Minh Tuấn, Nguyễn Mạnh Hùng. Kế hoạch: Gửi bản prototype Streamlit cho 2 willing users sử dụng thử với kịch bản demo thực tế của họ. Phỏng vấn ngắn 15 phút về tính hữu ích của các gợi ý và ghi nhận điểm cần cải thiện UI.
- Multi-prototype (nếu làm): 
  - Trục khác biệt: Hiển thị lỗi trực tiếp trên văn bản (inline edit) vs Hiển thị danh sách lỗi ở sidebar (list review). 
  - Lý do chọn: Chọn hiển thị danh sách lỗi vì người dùng có thể thấy rõ ràng từng lỗi và lời giải thích trước khi ra quyết định (áp dụng nguyên tắc G11).

## §9. Changelog
| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
|---|---|---|
| 2026-09-18 01:10:53 | Thêm trường "intent" và "expected_behavior" vào test-case | Làm rõ tiêu chí đánh giá và mục đích của từng case, giúp con người chấm chéo (Inter-rater Agreement) hoặc AI tự động chấm chính xác, khách quan hơn, tránh mơ hồ |
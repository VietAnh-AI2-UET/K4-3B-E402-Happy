# Template AI Spec *(spec.md — commit trước hạn chốt spec: 21:00 18/9, tại CP4 · quality bar chốt từ thời điểm nộp)*

> Cấu trúc phủ đúng "SPEC 8 phần" của chương trình: Bằng chứng (§1-§2) · Lát cắt (§4) · Canvas (đính kèm CP1) · Augment/Automate (§4) · 4 đường đi của trải nghiệm (§6) · Kiểu lỗi (§5) · Kiểm thử (§7) · Phân công (§8). Hướng dẫn viết từng mục: `02-guide.md`.

```markdown
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
- [Sản phẩm 1]: flow / đáng học / đáng né / mình khác gì
- [Sản phẩm 2]: ...

## §4. Thiết kế
- Lát cắt MỘT CÂU (1 user · 1 việc · 1 quyết định AI · 1 kết quả):
- Non-goals (≥3 thứ KHÔNG build):
- Mức prototype nhắm tới: [ ] Sketch [ ] Mock [ ] Working — phần nào mock, phần nào thật:
- Automation: [ ] augment [ ] conditional [ ] automate — lý do theo cost-of-error:
- §4b. Nguyên tắc đã áp dụng (≥4 — HAX/PAIR, xem guide):
  | Nguyên tắc | Áp cụ thể vào đâu trong prototype |
  |---|---|

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8) [bảng theo guide §2.5]

## §6. Bốn đường đi của trải nghiệm
- Happy path: · Low-confidence (②): · Failure/không căn cứ (①): · Correction (user sửa):
- Khi bị đòi ngoài phạm vi (③): · Case đặc thù domain (④):

## §7. Kiểm thử
- Chiều chất lượng + định nghĩa kiểm chứng được:
- Golden set (≥20 case theo cơ cấu trong guide §2.6, file trong eval/):
- Quality bar (chốt từ hạn chốt spec của khoá, giữ nguyên sau đó): "Đạt khi ≥ ___% qua bộ, và ___"
- Kết quả các lượt chạy (bảng % — cập nhật đến trước CP6):

## §8. Phân công & kế hoạch
- Phân công có tên: spec / evidence / prompt / code / demo
- Willing users (≥2 tên) + kế hoạch vòng validation *(bonus, nếu làm)*:
- Multi-prototype (nếu làm): trục khác biệt của ≥2 phương án + lý do chọn:

## §9. Changelog
| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
```
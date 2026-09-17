"""Deterministic CP2 fixtures; no LLM or external requests."""
from dataclasses import dataclass, asdict
import hashlib
import re

SAMPLES = {
    "Demo tính năng · Dev / BA": "Hôm nay, mình sẽ demo cách nhóm chuẩn bị nội dung kỹ thuật.\n\nChúng ta sẽ implement một methodology để optimize output của model. Sau đó, team có thể leverage context hiện có để improve kết quả.\n\nAPI trả về dữ liệu dạng JSON. Người trình bày cần kiểm tra lại ý nghĩa kỹ thuật trước khi chia sẻ với người nghe.",
    "Thuật ngữ cần giữ · PM": "Ở buổi chia sẻ này, mình sẽ giải thích cách hệ thống xử lý yêu cầu.\n\nChúng ta sử dụng eventual consistency để đồng bộ dữ liệu. API trả về dữ liệu dạng JSON.\n\nPhần đánh đổi về tính nhất quán cần được người phụ trách kỹ thuật xác nhận.",
    "Mẫu đã rõ ràng": "Hôm nay, mình sẽ giới thiệu cách hệ thống xử lý yêu cầu. API trả về dữ liệu dạng JSON. Bạn có thể xem ví dụ trước khi thử với dữ liệu của nhóm.",
    "Kịch bản của bạn": "",
}

# Exact spans only: arbitrary content is never claimed to be fully reviewed.
RULES = [
    ("implement một methodology", "áp dụng một phương pháp", "Pha Anh–Việt", "Có cách diễn đạt tiếng Việt ngắn, dễ đọc thành lời hơn.", False),
    ("optimize output của model", "tối ưu đầu ra của mô hình", "Pha Anh–Việt", "Việt hóa các từ phổ thông trong câu; người viết vẫn cần xác nhận đúng ngữ cảnh.", False),
    ("leverage context hiện có", "tận dụng ngữ cảnh hiện có", "Khó nói tự nhiên", "Thay cụm mang cấu trúc dịch bằng cách nói trực tiếp hơn.", False),
    ("improve kết quả", "cải thiện kết quả", "Pha Anh–Việt", "Chỉ sửa cụm cần thiết, không viết lại cả câu.", False),
    ("eventual consistency", "", "Cần xác nhận", "Đây là thuật ngữ có nghĩa chuyên biệt. Chưa đủ ngữ cảnh để đề xuất thay thế an toàn; hãy giữ nguyên hoặc tự biên tập.", True),
]

@dataclass(frozen=True)
class Finding:
    id: str
    start: int
    end: int
    original: str
    suggestion: str
    category: str
    reason: str
    uncertain: bool

def fingerprint(source, audience):
    return hashlib.sha256((source + "\0" + audience).encode()).hexdigest()

def analyze(source):
    if not source.strip():
        raise ValueError("Hãy nhập kịch bản trước khi rà soát.")
    if len(source) > 12000:
        raise ValueError("Bản demo hỗ trợ tối đa 12.000 ký tự. Hãy chia kịch bản thành đoạn nhỏ.")
    found = []
    for original, suggestion, category, reason, uncertain in RULES:
        for match in re.finditer(re.escape(original), source):
            found.append(Finding(str(match.start()), match.start(), match.end(), original, suggestion, category, reason, uncertain))
    found.sort(key=lambda item: item.start)
    covered = source in [text for text in SAMPLES.values() if text]
    return found, covered

def render_final(source, findings, decisions):
    result = source
    for item in sorted(findings, key=lambda f: f.start, reverse=True):
        decision = decisions.get(item.id)
        if not decision or decision["action"] not in ("accept", "keep"):
            raise ValueError("Cần duyệt tất cả gợi ý trước khi xuất bản hoàn chỉnh.")
        if decision["action"] == "accept":
            replacement = decision["replacement"].strip()
            if not replacement:
                raise ValueError("Nội dung thay thế không được để trống.")
            if source[item.start:item.end] != item.original:
                raise ValueError("Kịch bản đã thay đổi. Hãy rà soát lại.")
            result = result[:item.start] + replacement + result[item.end:]
    return result

def audit_payload(source, audience, findings, decisions, events, covered):
    return {
        "product": "TechScript QA", "mode": "CP2 deterministic mock — no LLM",
        "source_hash": fingerprint(source, audience), "audience": audience,
        "coverage": "demo_fixture" if covered else "partial_exact_span_only",
        "original": source, "final": render_final(source, findings, decisions),
        "findings": [dict(asdict(f), decision=decisions.get(f.id)) for f in findings],
        "events": list(events),
    }

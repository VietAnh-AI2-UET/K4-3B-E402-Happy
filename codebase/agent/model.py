import os
import json
import time
import requests
import logging
from dotenv import load_dotenv

# Import prompt từ file riêng
from .prompts import REVIEW_SYSTEM_PROMPT

# Đường dẫn mặc định tới file log trong codebase/run/
DEFAULT_RUN_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "run"))
DEFAULT_LOG_PATH = os.path.join(DEFAULT_RUN_DIR, "ai_calls.log")

def setup_logging(log_file=None):
    """Hàm cấu hình file lưu log linh hoạt, mặc định lưu vào codebase/run/ai_calls.log"""
    if log_file is None:
        log_file = DEFAULT_LOG_PATH
    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(
        filename=log_file, 
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s',
        encoding='utf-8',
        force=True
    )

# Gọi mặc định để đảm bảo log_path luôn trỏ vào codebase/run/ai_calls.log
setup_logging()

# Tải biến môi trường (Chỉ định rõ đường dẫn tới file .env trong thư mục codebase)
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)

def get_api_key(custom_key: str = None) -> str:
    """Lấy API key từ tham số truyền vào hoặc file .env / biến môi trường"""
    if custom_key and custom_key.strip():
        return custom_key.strip()
    return os.getenv("OPENROUTER_API_KEY", "")

def review_script(script_text: str, api_key: str = None) -> dict:
    """
    Hàm tương tác với LLM (gpt-4o-mini qua OpenRouter) để rà soát kịch bản.
    Ghi log vết prompt đầu vào, raw response, thời gian phản hồi (latency).
    Trả về Dictionary kết quả chứa danh sách các lỗi (findings).
    """
    key = get_api_key(api_key)
    if not key or key == "your_openrouter_api_key_here":
        raise ValueError("LỖI: Chưa thiết lập OPENROUTER_API_KEY trong file .env hoặc giao diện.")

    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }

    # Nội dung gửi đi bao gồm System Prompt và User Input
    data = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": REVIEW_SYSTEM_PROMPT},
            {"role": "user", "content": f"Kịch bản cần rà soát:\n{script_text}"}
        ],
        "response_format": {"type": "json_object"}, # Ép model trả về JSON hợp lệ
        "temperature": 0.2 # Temperature thấp để đảm bảo AI tập trung trích xuất chính xác span
    }

    # 1. GHI LOG PROMPT ĐẦU VÀO
    logging.info("================ BẮT ĐẦU GỌI AI (SCRIPT QA) ================")
    logging.info(f"Model: {data['model']}")
    logging.info(f"System Prompt:\n{REVIEW_SYSTEM_PROMPT}")
    logging.info(f"User Input:\n{script_text}")

    start_time = time.time()
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        latency = round(time.time() - start_time, 2)
        response.raise_for_status()
        
        result = response.json()
        
        # 2. GHI LOG PHẢN HỒI THÔ TỪ MÔ HÌNH
        logging.info(f"Độ trễ API: {latency}s")
        logging.info(f"Phản hồi thô từ API (Raw response):\n{json.dumps(result, ensure_ascii=False, indent=2)}")
        
        # Trích xuất nội dung JSON từ AI
        content_str = result['choices'][0]['message']['content']
        parsed_content = json.loads(content_str)
        
        logging.info("================ KẾT THÚC GỌI AI THÀNH CÔNG ================\n")
        
        return parsed_content

    except requests.exceptions.RequestException as e:
        latency = round(time.time() - start_time, 2)
        logging.error(f"Lỗi khi gọi API sau {latency}s: {e}")
        if getattr(e, 'response', None) is not None:
             logging.error(f"Chi tiết lỗi từ server: {e.response.text}")
        return {"error": str(e), "findings": []}
    except json.JSONDecodeError as e:
        logging.error(f"Lỗi phân tích JSON từ phản hồi của AI: {e}")
        return {"error": "AI không trả về định dạng JSON hợp lệ", "findings": []}
    except Exception as e:
        logging.error(f"Lỗi không xác định: {e}")
        return {"error": str(e), "findings": []}

def analyze_script_ai(source: str, api_key: str = None):
    """
    Module phân tích kịch bản bằng AI thật, chuyển đổi sang Finding dataclass cho UI Streamlit.
    """
    from core import Finding

    if not source.strip():
        raise ValueError("Hãy nhập kịch bản trước khi rà soát.")
    if len(source) > 12000:
        raise ValueError("Bản demo hỗ trợ tối đa 12.000 ký tự. Hãy chia kịch bản thành đoạn nhỏ.")

    ai_result = review_script(source, api_key=api_key)
    if "error" in ai_result:
        raise RuntimeError(ai_result["error"])

    raw_findings = ai_result.get("findings", [])
    findings = []
    
    for idx, item in enumerate(raw_findings):
        span = item.get("exact_span", "").strip()
        if not span:
            continue
        
        # Tìm vị trí xuất hiện trong kịch bản nguồn
        start = source.find(span)
        if start == -1:
            # Nếu không tìm thấy chính xác do viết hoa/thường, tìm case-insensitive
            start = source.lower().find(span.lower())
            if start != -1:
                span = source[start:start+len(span)]
            else:
                continue

        end = start + len(span)
        category = item.get("category", "Pha tiếng Anh")
        suggestion = item.get("suggestion", "") or ""
        reason = item.get("explanation", "AI phát hiện cụm từ cần cải thiện khi nói thành lời.")
        severity = str(item.get("severity", "")).lower()

        # Đánh dấu uncertain nếu AI không có suggestion hoặc độ tin cậy thấp
        uncertain = (not suggestion.strip()) or (severity == "low") or ("cần xác nhận" in category.lower())

        finding = Finding(
            id=f"{start}_{idx}",
            start=start,
            end=end,
            original=span,
            suggestion=suggestion,
            category=category,
            reason=reason,
            uncertain=uncertain
        )
        findings.append(finding)

    # Sắp xếp theo thứ tự xuất hiện trong văn bản
    findings.sort(key=lambda item: item.start)
    return findings, True

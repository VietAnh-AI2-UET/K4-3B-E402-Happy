import os
import json
import requests
import logging
from dotenv import load_dotenv

# Import prompt từ file riêng
from .prompts import REVIEW_SYSTEM_PROMPT

def setup_logging(log_file="ai_calls.log"):
    """Hàm cấu hình file lưu log linh hoạt"""
    logging.basicConfig(
        filename=log_file, 
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s',
        encoding='utf-8',
        force=True
    )

# Gọi mặc định (fallback) nếu không được set từ module khác
setup_logging()

# Tải biến môi trường (Chỉ định rõ đường dẫn tới file .env trong thư mục codebase)
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def review_script(script_text: str) -> dict:
    """
    Hàm tương tác với LLM (gpt-4o-mini qua OpenRouter) để rà soát kịch bản.
    Trả về Dictionary kết quả chứa danh sách các lỗi (findings).
    """
    if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == "your_openrouter_api_key_here":
        raise ValueError("LỖI: Chưa thiết lập OPENROUTER_API_KEY trong file .env")

    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
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
    logging.info("--- BẮT ĐẦU GỌI AI (SCRIPT QA) ---")
    logging.info(f"User Input:\n{script_text}")

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        
        # 2. GHI LOG PHẢN HỒI THÔ TỪ MÔ HÌNH
        logging.info(f"Phản hồi thô từ API (Raw response):\n{json.dumps(result, ensure_ascii=False, indent=2)}")
        
        # Trích xuất nội dung JSON từ AI
        content_str = result['choices'][0]['message']['content']
        parsed_content = json.loads(content_str)
        
        logging.info("--- KẾT THÚC GỌI AI ---\n")
        
        return parsed_content

    except requests.exceptions.RequestException as e:
        logging.error(f"Lỗi khi gọi API: {e}")
        if e.response is not None:
             logging.error(f"Chi tiết lỗi: {e.response.text}")
        return {"error": str(e), "findings": []}
    except json.JSONDecodeError as e:
        logging.error(f"Lỗi phân tích JSON từ AI: {e}")
        return {"error": "AI không trả về định dạng JSON hợp lệ", "findings": []}
    except Exception as e:
        logging.error(f"Lỗi không xác định: {e}")
        return {"error": str(e), "findings": []}

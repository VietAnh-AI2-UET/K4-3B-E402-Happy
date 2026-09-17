import os
import json
import argparse
from .model import review_script, setup_logging

def main():
    parser = argparse.ArgumentParser(description="Chạy đánh giá AI Reviewer với file test.")
    # Mặc định trỏ về file eval_base.json nếu không có tham số nào được truyền
    default_eval = os.path.join(os.path.dirname(__file__), "..", "eval", "eval_base.json")
    parser.add_argument(
        "--test-file", 
        type=str, 
        default=default_eval,
        help="Đường dẫn tới file JSON chứa các test cases (ví dụ: eval/eval_group.json)"
    )
    parser.add_argument(
        "--log-file",
        type=str,
        default="run_results.log",
        help="Tên file log đầu ra (được tự động lưu vào codebase/run/)"
    )
    
    args = parser.parse_args()
    eval_file = args.test_file
    
    # Thiết lập thư mục run/ và cấu hình lại tên file log
    run_dir = os.path.join(os.path.dirname(__file__), "..", "run")
    os.makedirs(run_dir, exist_ok=True)
    log_path = os.path.join(run_dir, args.log_file)
    setup_logging(log_path)
    
    print(f"Đang kiểm tra AI Reviewer với bộ test trong: {os.path.basename(eval_file)}...")
    print(f"Log sẽ được lưu vào: {os.path.relpath(log_path, os.path.join(os.path.dirname(__file__), '..'))}\n")
    
    if not os.path.exists(eval_file):
        print(f"[!] Không tìm thấy file {eval_file}")
        return

    with open(eval_file, "r", encoding="utf-8") as f:
        test_cases = json.load(f)
        
    print(f"-> Tìm thấy {len(test_cases)} test cases. Bắt đầu đánh giá...\n")
    
    for idx, tc in enumerate(test_cases, 1):
        tc_id = tc.get("id", f"Unknown-{idx}")
        script_input = tc.get("user_input", "")
        
        print(f"--- Đang chạy Test Case: {tc_id} ---")
        print(f"Đầu vào: {script_input}")
        
        try:
            result = review_script(script_input)
            
            if "error" in result:
                print(f"[!] LỖI: {result['error']}\n")
            else:
                findings = result.get("findings", [])
                if not findings:
                    print("=> Kết quả: Không tìm thấy lỗi nào.\n")
                else:
                    print(f"=> Kết quả: Tìm thấy {len(findings)} lỗi.")
                    for i, item in enumerate(findings, 1):
                        print(f"  Lỗi {i}: [{item.get('category')}] {item.get('exact_span')} - Gợi ý: {item.get('suggestion')}")
                    print()
        except Exception as e:
            print(f"[!] LỖI KHI CHẠY: {str(e)}\n")
    
    print(f"=> Hoàn tất. Vui lòng kiểm tra file '{args.log_file}' trong thư mục run/ để xem chi tiết raw response.")

if __name__ == "__main__":
    main()

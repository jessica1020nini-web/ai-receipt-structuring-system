import json
from datetime import datetime
from save_result import append_to_json_list

USE_AZURE = False  # 之後如果要接真的 Azure 改成 True


def send_to_azure(image_path):
    print("📡 正在將圖片傳送至 Azure API...")

    if USE_AZURE:
        # 這裡將來可以放真的 Azure API 呼叫
        print("🔗 呼叫真實 Azure API...")
        response = {
            "merchant": "Azure Store",
            "date": "2026-03-02",
            "total": 999
        }
    else:
        # Mock 模式
        with open("mock_receipt_result.json", "r", encoding="utf-8") as f:
            response = json.load(f)

    print("☁️ 已收到 Azure 回傳結果")
    return response


if __name__ == "__main__":
    image_path = "receipt.jpg"

    result = send_to_azure(image_path)
    result["created_at"] = datetime.now().isoformat(timespec="seconds")

    append_to_json_list(result)

    print("✅ 收據辨識完成，結果已儲存至 result.json")

    from datetime import datetime
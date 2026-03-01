import json
import os

def append_to_json_list(new_item, filename="result.json"):
    if not os.path.exists(filename):
        data = []
    else:
        with open(filename, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

    if not isinstance(data, list):
        data = [data]

    # 檢查是否已存在（避免重複）
    if new_item in data:
        print("⚠️ 這筆收據已存在，不重複加入")
        return

    data.append(new_item)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
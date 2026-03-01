import json

def calculate_total(filename="result.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        total_amount = sum(item.get("total", 0) for item in data)

        print(f"💰 目前總支出金額為：{total_amount}")

    except FileNotFoundError:
        print("⚠️ 尚未有任何收據資料")
    except json.JSONDecodeError:
        print("⚠️ 資料格式錯誤")

if __name__ == "__main__":
    calculate_total()
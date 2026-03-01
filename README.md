# AI Receipt Data Structuring System

## 📌 Project Overview
This project simulates an Azure Document Intelligence workflow.
It converts unstructured receipt data (image-based receipt) into structured JSON format.

The system supports:
- Simulated cloud API integration
- Data accumulation
- Deduplication mechanism
- Timestamp tracking
- Expense aggregation query

---

## 🏗 Architecture

receipt.jpg  
→ send_to_azure()  
→ JSON response  
→ append_to_json_list()  
→ result.json  

The project separates:
- API layer (cloud simulation)
- Data processing layer
- Storage layer

---

## 🚀 How to Run

### 1️⃣ Add a new receipt (simulate Azure recognition)

Run:

python main.py

This will:
- Simulate sending receipt image to Azure
- Receive structured JSON response
- Append data to result.json
- Prevent duplicate entries

---

### 2️⃣ Query total expense

Run:

python query.py

This will calculate the total expense from all stored receipts.

---

## 📊 Example Output (result.json)

```json
[
  {
    "merchant": "芳塢碼頭食品行",
        "date": "2026-02-25",
        "total": 140.0,
        "created_at":
        "2026-03-02T02:16:37"
  }
]
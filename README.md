# AI Receipt Data Structuring System

A web-based demo system that simulates Azure Document Intelligence to structure receipt data and store it in SQLite.

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
```

## Features

- Upload receipt image
- Mock Azure API processing
- Structured JSON result
- SQLite database storage
- Deduplication using SHA256 hash
- View all receipts
- Calculate total expense

## Tech Stack

- Python
- Flask
- SQLite
- HTML (render_template_string)


## Key Design Decisions

- Used SQLite for lightweight local database
- Used UNIQUE constraint on dedup_key to prevent duplicate records
- Used SHA256 hash to generate unique fingerprint for each receipt

## 🗄 Database Schema
```sql
CREATE TABLE receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    merchant TEXT,
    date TEXT,
    total REAL,
    created_at TEXT,
    dedup_key TEXT UNIQUE
);
```

This schema ensures:
	-	Each receipt has a unique identifier
	-	dedup_key prevents duplicate inserts
	-	Fast aggregation queries on total expense


## 🔐 Deduplication Strategy

Each receipt generates a SHA256 hash:

```python
dedup_key = sha256(raw_receipt_data)
```

This ensures:
	-	Identical receipts cannot be inserted twice
	-	Database integrity is preserved
	-	No manual duplicate checking is needed

## 📦 Future Improvements
	-	Replace mock Azure API with real Azure Document Intelligence
	-	Add REST API endpoints (JSON response instead of HTML)
	-	Add pagination for large receipt datasets
	-	Deploy to cloud (Render / Azure Web App)
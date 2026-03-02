import os
import json
from datetime import datetime
from flask import Flask, request, render_template_string, redirect, url_for, flash

from save_result import append_to_json_list

app = Flask(__name__)
app.secret_key = "dev-secret"  # 本地開發用，之後可改

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 你原本的雲端流程：這裡先用 mock 模擬 Azure 回傳（零成本）
def send_to_azure_mock(image_path: str) -> dict:
    print("📡 (Web) 模擬將圖片傳送至 Azure API...")

    with open("mock_receipt_result.json", "r", encoding="utf-8") as f:
        response = json.load(f)

    response["created_at"] = datetime.now().isoformat(timespec="seconds")
    response["source_image"] = os.path.basename(image_path)

    print("☁️ (Web) 已收到 Azure 回傳結果（mock）")
    return response


INDEX_HTML = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Receipt Structuring Demo</title>
    <style>
      body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial; max-width: 720px; margin: 40px auto; }
      .card { border: 1px solid #ddd; border-radius: 12px; padding: 18px; margin-bottom: 16px; }
      .muted { color: #666; }
      .btn { padding: 10px 14px; border: 0; border-radius: 10px; cursor: pointer; }
      .btn-primary { background: #111; color: #fff; }
      .btn-secondary { background: #eee; color: #111; }
      .flash { background: #fff3cd; border: 1px solid #ffeeba; padding: 10px; border-radius: 10px; margin-bottom: 12px; }
      input[type=file] { margin-top: 8px; }
    </style>
  </head>
  <body>
    <h1>AI Receipt Data Structuring System (Web Demo)</h1>
    <p class="muted">上傳一張收據圖片（本版本用 mock 模擬 Azure 回傳，零成本可 demo）。</p>

    {% with messages = get_flashed_messages() %}
      {% if messages %}
        {% for m in messages %}
          <div class="flash">{{ m }}</div>
        {% endfor %}
      {% endif %}
    {% endwith %}

    <div class="card">
      <h3>1) 上傳收據圖片</h3>
      <form action="{{ url_for('upload') }}" method="post" enctype="multipart/form-data">
        <input type="file" name="receipt" accept="image/*" required />
        <div style="margin-top: 12px;">
          <button class="btn btn-primary" type="submit">Upload & Process</button>
          <a class="btn btn-secondary" href="{{ url_for('view_data') }}" style="text-decoration:none;">View result.json</a>
        </div>
      </form>
    </div>

    <div class="card">
      <h3>2) 查詢總支出</h3>
      <a class="btn btn-primary" href="{{ url_for('total') }}" style="text-decoration:none;">Calculate Total</a>
    </div>

    <p class="muted">Tips：你可以在 GitHub README 放上操作截圖或錄影，面試超加分。</p>
  </body>
</html>
"""

RESULT_HTML = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Result</title>
    <style>
      body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial; max-width: 860px; margin: 40px auto; }
      pre { background: #0b1020; color: #e6e6e6; padding: 14px; border-radius: 12px; overflow:auto; }
      a { color: #111; }
    </style>
  </head>
  <body>
    <h2>✅ Processed Result</h2>
    <p><a href="{{ url_for('index') }}">← Back</a></p>
    <pre>{{ pretty }}</pre>
  </body>
</html>
"""


@app.get("/")
def index():
    return render_template_string(INDEX_HTML)


@app.post("/upload")
def upload():
    if "receipt" not in request.files:
        flash("沒有選擇檔案")
        return redirect(url_for("index"))

    file = request.files["receipt"]
    if file.filename.strip() == "":
        flash("檔名是空的，請重新選擇")
        return redirect(url_for("index"))

    # 存檔（讓流程更像真實系統）
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    file.save(save_path)

    # 模擬呼叫雲端辨識 → 取得結構化結果
    result = send_to_azure_mock(save_path)

    # 累加 + 去重（你前面做好的）
    append_to_json_list(result)

    pretty = json.dumps(result, ensure_ascii=False, indent=4)
    return render_template_string(RESULT_HTML, pretty=pretty)


@app.get("/data")
def view_data():
    if not os.path.exists("result.json"):
        return "result.json not found. Please upload a receipt first.", 404

    with open("result.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    return app.response_class(
        response=json.dumps(data, ensure_ascii=False, indent=4),
        status=200,
        mimetype="application/json",
    )


@app.get("/total")
def total():
    if not os.path.exists("result.json"):
        flash("目前還沒有資料，請先上傳一張收據")
        return redirect(url_for("index"))

    with open("result.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    total_amount = sum(item.get("total", 0) for item in data)
    flash(f"💰 目前總支出金額為：{total_amount}")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
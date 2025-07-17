from flask import Flask, request
import requests
import os
from dotenv import load_dotenv

# .env を読み込む（ローカル用。Renderでは無視される）
load_dotenv()

# 環境変数を取得
LINE_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
USER_ID = os.getenv("LINE_USER_ID")

app = Flask(__name__)

# ▶ 追加：トップページにアクセスしたときの挙動
@app.route("/")
def index():
    return "🧠 LINE Push通知アプリが起動しました！"

@app.route("/push", methods=["GET"])
def push_message():
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_TOKEN}"
    }
    payload = {
        "to": USER_ID,
        "messages": [
            {"type": "text", "text": "こんにちは！PythonからLINE通知テストです🥦"}
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    return f"送信結果: {response.status_code}, {response.text}"

# ▶ gunicorn起動用のFlaskアプリ名（app）に合わせて、明示的にポート設定
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


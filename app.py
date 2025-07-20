from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# .env の読み込み（Renderでは環境変数としても設定されている前提）
load_dotenv()

LINE_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
USER_ID = os.getenv("LINE_USER_ID")

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "🌸 LINE Push通知アプリが起動しました！"

@app.route("/push", methods=["POST"])
def push_message():
    try:
        data = request.get_json()
        text = data.get("message", "（メッセージが空です）")

        url = "https://api.line.me/v2/bot/message/push"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LINE_TOKEN}"
        }
        payload = {
            "to": USER_ID,
            "messages": [
                {"type": "text", "text": text}
            ]
        }

        response = requests.post(url, headers=headers, json=payload)
        return jsonify({
            "status": response.status_code,
            "line_response": response.json() if response.status_code == 200 else response.text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        print("Webhookイベント:", data)
        events = data.get("events", [])
        for event in events:
            user_id = event.get("source", {}).get("userId")
            print("LINE_USER_ID:", user_id)
        return "ok"
    except Exception as e:
        return jsonify({"error": str(e)}), 500

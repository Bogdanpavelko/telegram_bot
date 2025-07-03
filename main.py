# -*- coding: utf-8 -*-
import logging
import os
from flask import Flask, request
import requests
from datetime import datetime

# =============== ������������ ===============
BOT_TOKEN = os.getenv("7619011766:AAGAhF_uW5efso8pLfiPAkLEdHV8IL-VKJo")
BOT_NAME = os.getenv("BOT_NAME") or "DemoBot"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# =============== Flask app ===============
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route("/", methods=["POST"])
def webhook():
    update = request.get_json()

    if "message" not in update or "text" not in update["message"]:
        return {"ok": True}

    message = update["message"]
    text = message["text"].lower()
    chat_id = message["chat"]["id"]

    # =============== ������� ����������� ===============
    if "���" in text or "�����" in text:
        now = datetime.now().strftime("%H:%M:%S")
        reply = f"����� {now}"
    elif "���� �����" in text or "��'�" in text:
        reply = f"���� ����� {BOT_NAME}"
    else:
        reply = f"�� �������: {message['text']}"

    # =============== ³������ � Telegram ===============
    data = {
        "chat_id": chat_id,
        "text": reply
    }
    requests.post(TELEGRAM_API_URL, json=data)

    return {"ok": True}

@app.route("/", methods=["GET"])
def hello():
    return "��� ������!"

# =============== ������� ====================
if __name__ == "__main__":
    app.run(debug=True)

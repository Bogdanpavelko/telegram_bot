# -*- coding: utf-8 -*-
import logging
import os
from flask import Flask, request
import requests
from datetime import datetime

# =============== Налаштування ===============
BOT_TOKEN = os.getenv("BOT_TOKEN") or "сюди_встав_свій_токен"
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

    # =============== Обробка повідомлення ===============
    if "час" in text or "годин" in text:
        now = datetime.now().strftime("%H:%M:%S")
        reply = f"Зараз {now}"
    elif "тебе звати" in text or "ім'я" in text:
        reply = f"Мене звати {BOT_NAME}"
    else:
        reply = f"Ти написав: {message['text']}"

    # =============== Відповідь у Telegram ===============
    data = {
        "chat_id": chat_id,
        "text": reply
    }
    requests.post(TELEGRAM_API_URL, json=data)

    return {"ok": True}

@app.route("/", methods=["GET"])
def hello():
    return "Бот працює!"

# =============== Головне ====================
if __name__ == "__main__":
    app.run(debug=True)

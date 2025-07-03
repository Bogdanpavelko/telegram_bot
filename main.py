# -*- coding: utf-8 -*-
import logging
import os
from flask import Flask, request
import requests
from openai import OpenAI  # chatgpt
from datetime import datetime

# =============== ������������ ===============
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_NAME = os.getenv("BOT_NAME") or "DemoBot"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# =============== Flask app ===============
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"))
client.base_url = "https://openrouter.ai/api/v1"

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
    if 'ai' in text:
        reply = ask_openrouter(text)
    elif "час" in text or "годин" in text:
        now = datetime.now().strftime("%H:%M:%S")
        reply = f"зараз {now}"
    elif "тебе звати" in text or "ім'я" in text:
        reply = f"Мене звати {BOT_NAME}"
    else:
        reply = f"Ти написав: {message['text']}"

    # =============== ³������ � Telegram ===============
    data = {
        "chat_id": chat_id,
        "text": reply
    }
    requests.post(TELEGRAM_API_URL, json=data)

    return {"ok": True}


# Функція від chatgpt
def ask_openrouter(prompt):
    response = client.chat.completions.create(
        model="openrouter/gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


# Функція від chatgpt


@app.route("/", methods=["GET"])
def hello():
    return "Не знаю!"



#chatgpt всі можливі версії
@app.route("/models", methods=["GET"])
def get_models():
    try:
        models_list = client.models.list()
        models_info = [{"id": m.id, "object": m.object} for m in models_list.data]
        return {"models": models_info}
    except Exception as e:
        return {"error": str(e)}
#chatgpt
# =============== ������� ====================
if __name__ == "__main__":
    app.run(debug=True)

# -*- coding: utf-8 -*-
import logging
import os
from flask import Flask, request
import requests
import json # chatgpt
from datetime import datetime

# =============== Змінні оточення ===============
BOT_TOKEN = os.getenv("BOT_TOKEN")
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

    # =============== Логіка відповіді бота  ===============
    if 'ai' in text:
        reply = ask_openrouter(text)
    elif "час" in text or "годин" in text:
        now = datetime.now().strftime("%H:%M:%S")
        reply = f"зараз {now}"
    elif "тебе звати" in text or "ім'я" in text:
        reply = f"Мене звати {BOT_NAME}"
    else:
        reply = f"Ти написав: {message['text']}"

    # =============== Відправка відповіді в Telegram ===============
    data = {
        "chat_id": chat_id,
        "text": reply
    }
    requests.post(TELEGRAM_API_URL, json=data)

    return {"ok": True}


# Функція від chatgpt

def ask_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://telegram-bot-m9mk.onrender.com",  # опційно
        "X-Title": "TelegramBot",  # опційно
    }

    data = {
        "model": "openai/gpt-4o",  # перевірена модель
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        print("OpenRouter error:", response.status_code, response.text)
        return "⚠️ Помилка при зверненні до OpenRouter"

# Функція від chatgpt//////


@app.route("/", methods=["GET"])
def hello():
    return "Не знаю!"



#chatgpt всі можливі версії
# @app.route("/models", methods=["GET"])
# def get_models():
#     try:
#         models_list = client.models.list()
#         models_info = [{"id": m.id, "object": m.object} for m in models_list.data]
#         return {"models": models_info}
#     except Exception as e:
#         return {"error": str(e)}
#chatgpt
# =============== __main__ ====================
if __name__ == "__main__":
    app.run(debug=True)

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

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
# logging.basicConfig(level=logging.INFO)

@app.route("/", methods=["POST"])
def webhook():
    update = request.get_json()

    #chatgpt запит у нейронку
    logging.info("=== ОТРИМАНО UPDATE ===")
    logging.info(json.dumps(update, indent=2, ensure_ascii=False))


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

    #від нейронки
    logging.info(f"Відправлено в Telegram: {reply}")

    return {"ok": True}


# Функція від chatgpt

def ask_openrouter(prompt):
    url = "https://api.langdock.com/openai/eu/v1/chat/completions"
    headers = {
        "Authorization": "Bearer sk-KG78HonDCW_K_cFeFpd9BfuYTQZpJuDvhHt11aOtPPIxGoyTqLOh2YPIYbai85YrER4-ieudDnK_GE9Tb9bjIA",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://telegram-bot-m9mk.onrender.com",
        "X-Title": "TelegramBot",
    }

    data = {  
        "model": "gpt-4o-mini",
        "messages": [
        {"role": "system", "content": "Відповідай українською мовою коротко і зрозуміло."},
        {"role": "user", "content": prompt}
        ]


    }


    try:
        response = requests.post(url, headers=headers, json=data, timeout=120)  # <--- таймаут
        response.raise_for_status()

        #тимчасово
        full_response = response.json()
        content = full_response["choices"][0]["message"]["content"]
        return content.strip()


        #return response.json()['choices'][0]['message']['content']  напів робоча
    except requests.exceptions.Timeout:
        return "⚠️ Вийшов час очікування відповіді від OpenRouter"
    except requests.exceptions.RequestException as e:
        print("OpenRouter error:", e)
        return "⚠️ Сталася помилка при зверненні до OpenRouter"


# def ask_openrouter(prompt):   РОБОЧА!!!!!
#     url = "https://openrouter.ai/api/v1/chat/completions"
#     headers = {
#         "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
#         "Content-Type": "application/json",
#         "HTTP-Referer": "https://telegram-bot-m9mk.onrender.com",  # опційно
#         "X-Title": "TelegramBot",  # опційно
#     }

#         # Промт щоб нейронка відповідала Українською
#     prompt_ukr = f"Відповідай українською мовою на наступне запитання користувача: {prompt}"

#     data = {
#         "model": "deepseek/deepseek-v3-base:free",  # безкоштовна модель deepseek
#         "messages": [
#             {"role": "user", "content": prompt_ukr}
#         ]
#     }

#     response = requests.post(url, headers=headers, json=data)

#     # response = requests.post(url, headers=headers, data=json.dumps(data))

#     if response.status_code == 200:
#         return response.json()['choices'][0]['message']['content']
#     else:
#         print("OpenRouter error:", response.status_code, response.text)
#         return "⚠️ Помилка при зверненні до OpenRouter"

# Функція від chatgpt//////


@app.route("/", methods=["GET"])
def hello():
    return "Не знаю!"

# =============== __main__ ====================
if __name__ == "__main__":
    app.run(debug=True)

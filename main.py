from flask import Flask
from threading import Thread
from telegram import Bot
from telegram.constants import ParseMode
import os
import time
import random

BOT_TOKEN = os.environ["BOT_TOKEN"]
GROUP_ID = int(os.environ["GROUP_ID"])

QUESTIONS = [
    "Hi everyone! Just curious, what's the main utility of this token?",
    "Can someone explain how staking works here?",
    "Is there a roadmap update coming soon?",
    "Does this project have any partnerships yet?",
    "How do I buy the token from Trust Wallet?",
    "Will the team host an AMA soon?",
    "What's the benefit of holding long-term?",
    "When is the next airdrop?",
    "Are there any NFT plans in the roadmap?",
    "What makes this project different from others?"
]

SEND_INTERVAL = 900  # 15 mins

bot = Bot(token=BOT_TOKEN)

# Flask web server to keep alive
app = Flask('')

@app.route('/')
def home():
    return "✅ Bot is alive!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

def send_typing_effect(chat_id):
    for _ in range(random.randint(2, 4)):
        bot.send_chat_action(chat_id=chat_id, action="typing")
        time.sleep(random.randint(2, 5))

def send_random_question():
    question = random.choice(QUESTIONS)
    send_typing_effect(GROUP_ID)
    bot.send_message(chat_id=GROUP_ID, text=question, parse_mode=ParseMode.MARKDOWN)

keep_alive()

while True:
    try:
        send_random_question()
        time.sleep(SEND_INTERVAL)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(30)

import telegram
import os
import random
import asyncio
from telegram.constants import ParseMode
from flask import Flask

app = Flask(__name__)

BOT_TOKEN = os.environ["BOT_TOKEN"]
GROUP_ID = int(os.environ["GROUP_ID"])

bot = telegram.Bot(token=BOT_TOKEN)

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

async def send_typing_effect(chat_id):
    for _ in range(random.randint(2, 4)):
        await bot.send_chat_action(chat_id=chat_id, action="typing")
        await asyncio.sleep(random.randint(2, 5))

async def send_random_question():
    question = random.choice(QUESTIONS)
    print("Sending question:", question)
    await send_typing_effect(GROUP_ID)
    await bot.send_message(chat_id=GROUP_ID, text=question, parse_mode=ParseMode.MARKDOWN)

async def run_bot():
    while True:
        try:
            await send_random_question()
            await asyncio.sleep(SEND_INTERVAL)
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(30)

@app.route("/")
def index():
    return "Bot is running!"

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    app.run(host="0.0.0.0", port=8080)

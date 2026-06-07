import os, asyncio
from dotenv import load_dotenv
from telegram import Bot
load_dotenv()

async def main():
    bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
    me = await bot.get_me()
    print("BAGLANTI OK - Bot: @" + me.username + " (" + me.first_name + ")")
    print("Bot linki: t.me/" + me.username)
    print("READY: Bot calismaya hazir")

asyncio.run(main())

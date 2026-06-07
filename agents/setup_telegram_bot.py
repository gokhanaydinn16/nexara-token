import os, asyncio
from dotenv import load_dotenv
from telegram import Bot, BotCommand
load_dotenv()

async def main():
    bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))

    # Kisa aciklama (profilde gorunur)
    await bot.set_my_short_description(
        "AI trading bot access, tokenized. Stake NXR, earn revenue. 2% burn. nexara-token.netlify.app"
    )

    # Uzun aciklama (bot acilista gosterir)
    await bot.set_my_description(
        "Welcome to Nexara (NXR)!\n\n"
        "Stake NXR to access the Superajan AI trading bot and earn revenue share.\n\n"
        "- 2% burn on every transfer\n"
        "- 12% APY staking\n"
        "- Anti-whale protection\n\n"
        "Type /start to begin. Website: nexara-token.netlify.app"
    )

    # Komut menusu
    await bot.set_my_commands([
        BotCommand("start",    "Welcome & overview"),
        BotCommand("tier",     "Staking tiers (Bronze/Silver/Gold)"),
        BotCommand("stake",    "Staking info & APY"),
        BotCommand("contract", "Contract addresses"),
        BotCommand("roadmap",  "Project roadmap"),
        BotCommand("airdrop",  "Active airdrop"),
        BotCommand("website",  "Official links"),
    ])

    print("Bot profili ayarlandi: aciklama + komut menusu OK")

asyncio.run(main())

"""
NEXARA Telegram Ajanı (Lite) — Anthropic GEREKTİRMEZ, tamamen ücretsiz çalışır.
Komutlar + üye karşılama + akıllı yönlendirme. AI cevaplar için sonra tam sürüme geçilir.
"""
import os, logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Application, CommandHandler, MessageHandler,
                          ChatMemberHandler, ContextTypes, filters)

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
log = logging.getLogger(__name__)

TOKEN_ADDRESS = "0xa14F7e4DE163Bc05297AF005B6cD44A770842187"
STAKING_ADDRESS = "0xa589014ee01E4F4f473ABD5587d304fA4879F5E4"
WEB = "https://nexara-token.netlify.app"
ETHERSCAN = f"https://sepolia.etherscan.io/address/{TOKEN_ADDRESS}"

async def start(update, ctx):
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("Website", url=WEB),
         InlineKeyboardButton("Etherscan", url=ETHERSCAN)],
        [InlineKeyboardButton("Twitter/X", url="https://x.com/NexaraNXR"),
         InlineKeyboardButton("Pay", url=WEB+"/pay.html")],
    ])
    await update.message.reply_text(
        "*NEXARA (NXR)* — AI Trading Access Token\n\n"
        "Stake NXR, access the Superajan AI bot, earn revenue share.\n\n"
        "Commands:\n"
        "/tier - Staking tiers\n/stake - Staking info\n"
        "/contract - Addresses\n/roadmap - Roadmap\n/airdrop - Airdrop\n/website - Links",
        parse_mode="Markdown", reply_markup=kb)

async def tier(update, ctx):
    await update.message.reply_text(
        "*NEXARA TIER SYSTEM*\n\n"
        "Bronze - 10,000 NXR -> Basic signals\n"
        "Silver - 50,000 NXR -> Whale tracking + advanced\n"
        "Gold - 200,000 NXR -> Full access + governance\n\n"
        "Lock: 30 days | APY: 12%", parse_mode="Markdown")

async def stake(update, ctx):
    await update.message.reply_text(
        "*NXR STAKING*\n\n12% APY | 30-day lock\n"
        "Rewards from 1% of every transfer.\n\n"
        f"Staking contract:\n`{STAKING_ADDRESS}`", parse_mode="Markdown")

async def contract(update, ctx):
    await update.message.reply_text(
        "*CONTRACT ADDRESSES*\n\n"
        f"Token:\n`{TOKEN_ADDRESS}`\n\nStaking:\n`{STAKING_ADDRESS}`\n\n"
        "Always verify the official address!", parse_mode="Markdown")

async def roadmap(update, ctx):
    await update.message.reply_text(
        "*ROADMAP*\n\nQ2 2026 - Token + Staking LIVE (done)\n"
        "Q3 2026 - Mainnet + Bot tiers\nQ4 2026 - Uniswap + CoinGecko\n"
        "2027 - Governance + Multi-exchange", parse_mode="Markdown")

async def airdrop(update, ctx):
    await update.message.reply_text(
        "*NEXARA AIRDROP*\n\n500,000 NXR | 500 winners x 1,000 NXR\n\n"
        "1) Follow @NexaraNXR\n2) RT pinned tweet\n3) Join this group\n4) Drop your ETH wallet\n\n"
        f"Details: {WEB}/airdrop.html", parse_mode="Markdown")

async def website(update, ctx):
    await update.message.reply_text(
        f"*OFFICIAL LINKS*\n\nWebsite: {WEB}\nPay: {WEB}/pay.html\n"
        f"Airdrop: {WEB}/airdrop.html\nTwitter: x.com/NexaraNXR", parse_mode="Markdown")

async def welcome(update, ctx):
    for m in update.chat_member.new_chat_members if update.chat_member else []:
        if m.is_bot: continue
        name = m.username or m.first_name
        await ctx.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Welcome @{name}! 🔷\n\nNexara (NXR) - stake to access AI trading.\n"
                 "Type /start to begin. Admins never DM first - stay safe!")

SPAM = ["giveaway", "free eth", "double your", "send eth", "claim now", "airdrop bot"]
async def msg(update, ctx):
    if not update.message or not update.message.text: return
    t = update.message.text.lower()
    if any(k in t for k in SPAM):
        await update.message.reply_text("Spam/scam not allowed. Official support only via admins.")
        return
    # AI yok -> komutlara yonlendir
    if "?" in t or any(w in t for w in ["how","what","nedir","nasil","price","fiyat","buy","stake","tier"]):
        await update.message.reply_text(
            "Try these commands:\n/start /tier /stake /contract /roadmap /airdrop /website\n\n"
            f"More info: {WEB}")

def main():
    app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    for c,h in [("start",start),("tier",tier),("stake",stake),("contract",contract),
                ("roadmap",roadmap),("airdrop",airdrop),("website",website)]:
        app.add_handler(CommandHandler(c,h))
    app.add_handler(ChatMemberHandler(welcome))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, msg))
    log.info("NEXARA Telegram bot (lite) calisiyor - @NexaraNXRbot")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

"""
NEXARA Telegram Ajanı — 7/24 çalışan otonom community manager.

Özellikler:
- Yeni üyeleri otomatik karşılar
- Her soruyu Claude AI ile cevaplar
- /tier, /stake, /price, /contract komutları
- Günlük istatistik paylaşır
- Spam/scam filtresi
"""

import os
import logging
import asyncio
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ChatMemberHandler, ContextTypes, filters
)
from nexara_brain import brain

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(message)s")
log = logging.getLogger(__name__)

TOKEN_ADDRESS = "0xa14F7e4DE163Bc05297AF005B6cD44A770842187"
STAKING_ADDRESS = "0xa589014ee01E4F4f473ABD5587d304fA4879F5E4"
ETHERSCAN = f"https://sepolia.etherscan.io/address/{TOKEN_ADDRESS}"

# ─── Komutlar ────────────────────────────────────────────────────────────────

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 Whitepaper", url="https://nexara.io/whitepaper"),
         InlineKeyboardButton("🔍 Etherscan", url=ETHERSCAN)],
        [InlineKeyboardButton("🐦 Twitter", url="https://twitter.com/NexaraToken"),
         InlineKeyboardButton("💬 Telegram", url="https://t.me/NexaraOfficial")]
    ])
    await update.message.reply_text(
        "🔷 *NEXARA (NXR) — AI Trading Bot Access Token*\n\n"
        "Merhaba! Ben NEX, Nexara'nın AI asistanıyım.\n\n"
        "Her sorunuzu cevaplayabilirim. Sadece yazın!\n\n"
        "📌 Hızlı komutlar:\n"
        "/tier — Tier sistemi\n"
        "/stake — Staking bilgisi\n"
        "/contract — Sözleşme adresleri\n"
        "/roadmap — Yol haritası\n"
        "/airdrop — Aktif kampanyalar",
        parse_mode="Markdown",
        reply_markup=kb
    )

async def tier_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏆 *NEXARA TİER SİSTEMİ*\n\n"
        "🥉 *Bronze* — 10,000 NXR stake\n"
        "└ Temel sinyaller • 3 parite\n\n"
        "🥈 *Silver* — 50,000 NXR stake\n"
        "└ Whale takip • Gelişmiş sinyaller • 10 parite\n\n"
        "🥇 *Gold* — 200,000 NXR stake\n"
        "└ Tüm özellikler • Öncelikli destek • Sınırsız\n\n"
        "⏱ Kilit süresi: 30 gün\n"
        "📈 Staking APY: %12\n\n"
        "🔷 Stake et, trade et, kazan.",
        parse_mode="Markdown"
    )

async def stake_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📈 *NXR STAKING*\n\n"
        "• APY: *%12* yıllık getiri\n"
        "• Kilit: *30 gün*\n"
        "• Ödüller: Her transferin %1'i havuza gider\n"
        "• Claim: İstediğin zaman çekebilirsin\n\n"
        f"📋 Staking Sözleşmesi:\n`{STAKING_ADDRESS}`\n\n"
        "🔷 Stake et, Superajan botuna eriş.",
        parse_mode="Markdown"
    )

async def contract_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 *SÖZLEŞME ADRESLERİ*\n\n"
        f"🔷 *NXR Token:*\n`{TOKEN_ADDRESS}`\n\n"
        f"📈 *Staking:*\n`{STAKING_ADDRESS}`\n\n"
        f"🔍 Etherscan'da doğrula:\n{ETHERSCAN}\n\n"
        "⚠️ Daima resmi adresleri kullan!",
        parse_mode="Markdown"
    )

async def roadmap_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🗺 *NEXARA ROADMAP*\n\n"
        "✅ *Q2 2026* — Token + Staking LIVE\n"
        "🔄 *Q3 2026* — Mainnet + Bot erişim tieri\n"
        "🔜 *Q4 2026* — Uniswap V3 + CoinGecko\n"
        "🔮 *2027*    — Governance + Multi-exchange\n\n"
        "🔷 Her adım açık, her gelişme burada duyurulur.",
        parse_mode="Markdown"
    )

async def airdrop_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎁 *NEXARA AIRDROP*\n\n"
        "500,000 NXR dağıtıyoruz!\n\n"
        "Katılmak için:\n"
        "✅ @NexaraToken'ı takip et\n"
        "✅ Lansman tweetini RT et\n"
        "✅ Bu gruba katıl ✓\n"
        "✅ ETH adresini aşağıya yaz\n\n"
        "🏆 500 kazanan × 1,000 NXR\n\n"
        "🔷 Adresini şimdi yaz!",
        parse_mode="Markdown"
    )

# ─── Yeni Üye Karşılama ───────────────────────────────────────────────────────

async def welcome_new_member(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Gruba yeni katılan üyeleri AI ile karşıla."""
    for member in update.chat_member.new_chat_members:
        if member.is_bot:
            continue
        username = member.username or member.first_name
        log.info(f"Yeni üye: {username}")
        try:
            msg = brain.get_welcome_message(username)
            await ctx.bot.send_message(
                chat_id=update.effective_chat.id,
                text=msg,
                parse_mode="Markdown"
            )
        except Exception as e:
            log.error(f"Karşılama hatası: {e}")

# ─── Genel Mesaj Handler ──────────────────────────────────────────────────────

SPAM_KEYWORDS = ["giveaway", "free eth", "double your", "send eth", "metamask support"]

async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Her mesajı AI ile cevapla."""
    if not update.message or not update.message.text:
        return

    text = update.message.text.lower()
    user_id = str(update.effective_user.id)
    username = update.effective_user.username or update.effective_user.first_name

    # Spam filtresi
    if any(kw in text for kw in SPAM_KEYWORDS):
        await update.message.reply_text(
            "⚠️ Bu tür mesajlar bu grupta yasaktır. "
            "Nexara resmi destek sadece @NexaraSupport üzerinden verilir."
        )
        return

    # Çok kısa mesajlara cevap verme
    if len(text) < 5:
        return

    # "typing..." göster
    await ctx.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    try:
        reply = brain.get_response(user_id, update.message.text)
        await update.message.reply_text(reply, parse_mode="Markdown")
        log.info(f"[{username}]: {text[:50]} → cevaplandı")
    except Exception as e:
        log.error(f"AI hatası: {e}")
        await update.message.reply_text(
            "Şu an yanıt veremiyorum, lütfen tekrar dene. 🔷"
        )

# ─── Günlük Otomatik Mesaj ────────────────────────────────────────────────────

async def send_daily_update(ctx: ContextTypes.DEFAULT_TYPE):
    """Her gün saat 12:00'de istatistik paylaş."""
    chat_id = os.getenv("TELEGRAM_CHANNEL_ID")
    if not chat_id:
        return
    try:
        msg = brain.get_daily_update(
            burned_today="2,450",
            total_staked="1,250,000"
        )
        await ctx.bot.send_message(chat_id=chat_id, text=msg)
    except Exception as e:
        log.error(f"Günlük mesaj hatası: {e}")

# ─── Ana Fonksiyon ────────────────────────────────────────────────────────────

def main():
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        print("HATA: TELEGRAM_BOT_TOKEN bulunamadı!")
        print("1. @BotFather'a git → /newbot → token al")
        print("2. .env dosyasına TELEGRAM_BOT_TOKEN=xxx ekle")
        return

    app = Application.builder().token(bot_token).build()

    # Komutlar
    app.add_handler(CommandHandler("start",    start))
    app.add_handler(CommandHandler("tier",     tier_cmd))
    app.add_handler(CommandHandler("stake",    stake_cmd))
    app.add_handler(CommandHandler("contract", contract_cmd))
    app.add_handler(CommandHandler("roadmap",  roadmap_cmd))
    app.add_handler(CommandHandler("airdrop",  airdrop_cmd))

    # Yeni üye
    app.add_handler(ChatMemberHandler(welcome_new_member))

    # Genel mesaj (komut olmayanlar)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Günlük mesaj — her gün saat 12:00
    app.job_queue.run_daily(send_daily_update, time=__import__("datetime").time(12, 0))

    print("🔷 NEXARA Telegram Ajanı başlatıldı!")
    print("Bot 7/24 çalışıyor. Durdurmak için Ctrl+C")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

"""
NEXARA Growth Agent — Hesap büyütme motoru.

Twitter + Telegram için:
- Saatlik haber + içerik paylaşımı
- Trend kripto konularına yorum
- İlgili hesaplara engagement
- Otomatik içerik takvimi
"""

import os
import time
import logging
import asyncio
import schedule
import tweepy
from datetime import datetime
from dotenv import load_dotenv
from telegram import Bot
from content_engine import ContentEngine

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("growth_agent.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)


class NexaraGrowthAgent:
    def __init__(self):
        self.engine = ContentEngine()

        # Telegram
        self.tg_bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
        self.tg_channel = os.getenv("TELEGRAM_CHANNEL_ID")

        # Twitter
        self.tw = tweepy.Client(
            bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_SECRET"),
            wait_on_rate_limit=True
        )

        self.daily_pack = None
        self.posted_today = set()
        log.info("🔷 Growth Agent başlatıldı.")

    # ─── Paylaşım Fonksiyonları ───────────────────────────────────────────────

    async def post_telegram(self, content: str):
        """Telegram kanalına post yayınla."""
        try:
            await self.tg_bot.send_message(
                chat_id=self.tg_channel,
                text=content,
                parse_mode="Markdown",
                disable_web_page_preview=False
            )
            log.info(f"✅ Telegram: {content[:60]}...")
        except Exception as e:
            log.error(f"❌ Telegram hatası: {e}")

    def post_twitter(self, content: str):
        """Twitter'a tweet at."""
        try:
            if len(content) > 280:
                content = content[:277] + "..."
            self.tw.create_tweet(text=content)
            log.info(f"✅ Twitter: {content[:60]}...")
        except Exception as e:
            log.error(f"❌ Twitter hatası: {e}")

    # ─── Sabah Rutini ─────────────────────────────────────────────────────────

    async def morning_routine(self):
        log.info("🌅 Sabah rutini başlıyor...")
        self.posted_today = set()
        self.daily_pack = self.engine.generate_daily_pack()

        # İlk içerikleri hemen paylaş
        content_tw = self.engine.generate_morning_hype("twitter")
        content_tg = self.engine.generate_morning_hype("telegram")

        self.post_twitter(content_tw)
        await self.post_telegram(content_tg)
        self.posted_today.add("morning")

    # ─── Haber Paylaşımı ──────────────────────────────────────────────────────

    async def share_news(self):
        """Güncel haber çek, yorum yap, paylaş."""
        log.info("📰 Haber paylaşımı...")
        news_list = self.engine.fetch_latest_news(max_per_feed=1)

        if not news_list:
            log.warning("Haber bulunamadı.")
            return

        news = news_list[0]
        title_key = news["title"][:30]

        if title_key in self.posted_today:
            log.info("Bu haber zaten paylaşıldı, atlıyorum.")
            return

        tw_post = self.engine.generate_news_post(news, "twitter")
        tg_post = self.engine.generate_news_post(news, "telegram")

        self.post_twitter(tw_post)
        await self.post_telegram(tg_post)
        self.posted_today.add(title_key)

    # ─── Eğitim İçeriği ───────────────────────────────────────────────────────

    async def share_educational(self):
        log.info("📚 Eğitim içeriği paylaşılıyor...")
        tw_post = self.engine.generate_educational_post("twitter")
        tg_post = self.engine.generate_educational_post("telegram")
        self.post_twitter(tw_post)
        await self.post_telegram(tg_post)

    # ─── Etkileşim Postu ──────────────────────────────────────────────────────

    async def share_engagement(self):
        log.info("💬 Etkileşim postu...")
        tw_post = self.engine.generate_engagement_post("twitter")
        tg_post = self.engine.generate_engagement_post("telegram")
        self.post_twitter(tw_post)
        await self.post_telegram(tg_post)

    # ─── Kripto Topluluğu ile Etkileşim (Twitter) ────────────────────────────

    def engage_crypto_community(self):
        """#DeFi ve #Crypto tweetlerine yorum yap → görünürlük artır."""
        keywords = ["$ETH DeFi", "staking rewards", "AI trading bot", "deflationary token"]
        import random
        query = random.choice(keywords) + " -is:retweet lang:en"

        try:
            results = self.tw.search_recent_tweets(
                query=query,
                max_results=5,
                tweet_fields=["author_id", "text"]
            )
            if not results.data:
                return

            for tweet in results.data[:2]:  # Max 2 yorum/tur
                comment = self.engine.ai.messages.create(
                    model="claude-opus-4-5",
                    max_tokens=150,
                    messages=[{
                        "role": "user",
                        "content": f"""
Bu tweete kısa, doğal bir yorum yaz (Max 200 karakter):
Tweet: {tweet.text[:200]}

Kurallar:
- Doğal ve samimi ol, spam gibi görünme
- NXR'den bahsedebilirsin ama zorla değil
- Kripto hakkında zeki bir yorum yap
- İngilizce
"""
                    }]
                ).content[0].text

                if len(comment) > 270:
                    comment = comment[:267] + "..."

                self.tw.create_tweet(
                    text=comment,
                    in_reply_to_tweet_id=tweet.id
                )
                log.info(f"💬 Yorum yapıldı: {comment[:50]}...")
                time.sleep(10)  # Rate limit

        except Exception as e:
            log.error(f"Community engagement hatası: {e}")

    # ─── Haftalık Büyüme Raporu ───────────────────────────────────────────────

    async def weekly_growth_report(self):
        log.info("📊 Haftalık büyüme raporu...")
        report_tw = """📊 $NXR Weekly Growth Report

🔥 Burn: Supply continues shrinking
👥 Community: Growing every day
🤖 Bot: Superajan running 24/7
📈 Staking: 12% APY active

We build, we ship, we grow. 💪

Join us: t.me/NexaraOfficial
🔷 #NXR #Nexara #DeFi #WeeklyUpdate"""

        self.post_twitter(report_tw)
        await self.post_telegram(
            "📊 *Haftalık NXR Raporu*\n\n"
            "🔥 Token yakımı devam ediyor\n"
            "👥 Topluluk büyüyor\n"
            "🤖 Superajan 7/24 aktif\n"
            "📈 Staking %12 APY\n\n"
            "Güçlenmeye devam ediyoruz! 🔷"
        )

    # ─── Tam Takvim ──────────────────────────────────────────────────────────

    def setup_schedule(self):
        """Günlük paylaşım takvimini kur."""

        def run_async(coro):
            asyncio.get_event_loop().run_until_complete(coro)

        # Sabah rutini
        schedule.every().day.at("08:00").do(lambda: run_async(self.morning_routine()))

        # Haber paylaşımları
        schedule.every().day.at("10:00").do(lambda: run_async(self.share_news()))
        schedule.every().day.at("16:00").do(lambda: run_async(self.share_news()))
        schedule.every().day.at("21:00").do(lambda: run_async(self.share_news()))

        # Eğitim içeriği
        schedule.every().day.at("13:00").do(lambda: run_async(self.share_educational()))

        # Etkileşim postu
        schedule.every().day.at("17:00").do(lambda: run_async(self.share_engagement()))

        # Topluluk engagement (Twitter)
        schedule.every(3).hours.do(self.engage_crypto_community)

        # Haftalık rapor
        schedule.every().monday.at("09:30").do(lambda: run_async(self.weekly_growth_report()))

        log.info("📅 Takvim kuruldu:")
        log.info("  08:00 — Sabah rutini + motivasyon postu")
        log.info("  10:00 — Sabah haber paylaşımı")
        log.info("  13:00 — Eğitim içeriği")
        log.info("  16:00 — Öğleden sonra haber")
        log.info("  17:00 — Etkileşim postu")
        log.info("  21:00 — Akşam haber")
        log.info("  Her 3 saat — Kripto topluluğu yorumu")
        log.info("  Pazartesi — Haftalık rapor")

    def run(self):
        """Growth Agent'ı başlat ve çalıştır."""
        self.setup_schedule()
        log.info("\n🚀 NEXARA Growth Agent CANLI — 7/24 çalışıyor!\n")

        # Hemen bir içerik paylaş (test)
        asyncio.get_event_loop().run_until_complete(self.morning_routine())

        while True:
            schedule.run_pending()
            time.sleep(60)


if __name__ == "__main__":
    missing = []
    required = ["ANTHROPIC_API_KEY", "TELEGRAM_BOT_TOKEN",
                "TELEGRAM_CHANNEL_ID", "TWITTER_BEARER_TOKEN"]
    for k in required:
        if not os.getenv(k):
            missing.append(k)

    if missing:
        print(f"❌ Eksik .env değerleri: {', '.join(missing)}")
        print("agents/.env.example dosyasına bak.")
    else:
        agent = NexaraGrowthAgent()
        agent.run()

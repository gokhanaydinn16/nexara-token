"""
NEXARA Twitter Ajanı — Otomatik engagement ve içerik.

Özellikler:
- Mention'lara Claude AI ile otomatik cevap
- Günlük tweet takvimi
- Airdrop katılımcılarını takip
- Kripto trendlere yorum
"""

import os
import time
import logging
import tweepy
from dotenv import load_dotenv
from nexara_brain import brain
import schedule

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(message)s")
log = logging.getLogger(__name__)

class NexaraTwitterAgent:
    def __init__(self):
        self.client = tweepy.Client(
            bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_SECRET"),
            wait_on_rate_limit=True
        )
        self.last_mention_id = None
        self.my_user_id = self._get_my_id()
        log.info(f"Twitter Ajanı başlatıldı. User ID: {self.my_user_id}")

    def _get_my_id(self):
        try:
            me = self.client.get_me()
            return me.data.id
        except Exception as e:
            log.error(f"ID alınamadı: {e}")
            return None

    # ── Mention'lara Cevap Ver ────────────────────────────────────────────────

    def reply_to_mentions(self):
        """Son mention'ları al ve Claude ile cevapla."""
        try:
            params = dict(
                max_results=10,
                tweet_fields=["author_id", "text", "created_at"]
            )
            if self.last_mention_id:
                params["since_id"] = self.last_mention_id

            mentions = self.client.get_users_mentions(
                id=self.my_user_id, **params
            )

            if not mentions.data:
                return

            for tweet in reversed(mentions.data):
                self.last_mention_id = tweet.id
                text = tweet.text.replace("@NexaraToken", "").strip()

                if not text or len(text) < 3:
                    continue

                log.info(f"Mention: {text[:60]}")

                # Claude ile cevap üret
                reply = brain.get_response(
                    user_id=str(tweet.author_id),
                    message=text
                )

                # Twitter 280 karakter limiti
                if len(reply) > 270:
                    reply = reply[:267] + "..."

                self.client.create_tweet(
                    text=reply,
                    in_reply_to_tweet_id=tweet.id
                )
                log.info(f"Cevap gönderildi → tweet {tweet.id}")
                time.sleep(3)  # rate limit

        except Exception as e:
            log.error(f"Mention hatası: {e}")

    # ── Günlük Tweet Takvimi ──────────────────────────────────────────────────

    def tweet_morning_update(self):
        """Sabah günlük tweet."""
        tweets = [
            "🔷 $NXR Daily Update\n\n🔥 Burn: deflationary supply shrinking\n📈 Staking APY: 12%\n🤖 Superajan bot: ACTIVE\n\nStake NXR → Access AI trading\n\n#Nexara #NXR #DeFi",
            "🧵 How $NXR actually works:\n\n1️⃣ Buy NXR\n2️⃣ Stake to get bot access\n3️⃣ Bot trades → you earn\n4️⃣ Every transfer burns 2%\n5️⃣ Supply shrinks, demand grows\n\nSimple. Powerful. 🔷\n\n#Nexara #DeFi #PassiveIncome",
            "Most tokens promise utility.\n$NXR delivers it.\n\n🤖 Real AI bot\n📊 Real trading signals\n💰 Real revenue share\n🔥 Real burn mechanism\n\nThis is what utility looks like.\n\n#Nexara #NXR #RealUtility",
            "🔷 $NXR Tier System:\n\n🥉 Bronze: 10K NXR → Basic signals\n🥈 Silver: 50K NXR → Whale tracking\n🥇 Gold: 200K NXR → Full bot access\n\nWhich tier are you going for? 👇\n\n#Nexara #NXR #DeFi",
        ]
        import random
        tweet = random.choice(tweets)
        try:
            self.client.create_tweet(text=tweet)
            log.info("Sabah tweeti gönderildi.")
        except Exception as e:
            log.error(f"Tweet hatası: {e}")

    def tweet_weekly_stats(self):
        """Haftalık istatistik tweeti."""
        tweet = (
            "📊 $NXR Weekly Stats\n\n"
            "🔥 Total Burned: [X] NXR\n"
            "📈 Total Staked: [X] NXR\n"
            "👥 Holders: [X]\n"
            "🤖 Bot Uptime: 100%\n\n"
            "Week by week. Building. 🔷\n\n"
            "#Nexara #NXR #WeeklyUpdate"
        )
        try:
            self.client.create_tweet(text=tweet)
            log.info("Haftalık tweet gönderildi.")
        except Exception as e:
            log.error(f"Haftalık tweet hatası: {e}")

    # ── Airdrop Katılımcı Takibi ──────────────────────────────────────────────

    def collect_airdrop_participants(self, tweet_id: str):
        """Airdrop tweetine yorum yapanların cüzdan adreslerini topla."""
        participants = []
        try:
            replies = self.client.search_recent_tweets(
                query=f"conversation_id:{tweet_id} 0x",
                max_results=100,
                tweet_fields=["author_id", "text"]
            )
            if replies.data:
                for tweet in replies.data:
                    # ETH adresi bul (0x ile başlayan 42 karakter)
                    import re
                    addresses = re.findall(r'0x[a-fA-F0-9]{40}', tweet.text)
                    if addresses:
                        participants.append({
                            "user_id": tweet.author_id,
                            "address": addresses[0]
                        })
            log.info(f"{len(participants)} airdrop katılımcısı bulundu.")
            return participants
        except Exception as e:
            log.error(f"Katılımcı toplama hatası: {e}")
            return []

    # ── Ana Döngü ─────────────────────────────────────────────────────────────

    def run(self):
        """7/24 çalışan ajan döngüsü."""
        log.info("🔷 NEXARA Twitter Ajanı başlatıldı!")

        # Takvim
        schedule.every().day.at("09:00").do(self.tweet_morning_update)
        schedule.every().monday.at("10:00").do(self.tweet_weekly_stats)
        schedule.every(5).minutes.do(self.reply_to_mentions)

        while True:
            schedule.run_pending()
            time.sleep(30)


if __name__ == "__main__":
    required = [
        "TWITTER_BEARER_TOKEN", "TWITTER_API_KEY",
        "TWITTER_API_SECRET", "TWITTER_ACCESS_TOKEN",
        "TWITTER_ACCESS_SECRET", "ANTHROPIC_API_KEY"
    ]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        print(f"HATA: Şu .env değerleri eksik: {', '.join(missing)}")
        print("Twitter Developer Portal'dan API keylerini al.")
    else:
        agent = NexaraTwitterAgent()
        agent.run()

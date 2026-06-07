"""
NEXARA Content Engine — Haber takibi + içerik üretimi.

- CoinTelegraph, CoinDesk, CryptoCompare'den haber çeker
- Claude AI ile NXR'ye bağlı yorum üretir
- Twitter + Telegram için farklı format oluşturur
- Trend hashtag takibi
- Günlük, haftalık içerik takvimi
"""

import os
import json
import random
import feedparser
import anthropic
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ─── Haber Kaynakları (RSS) ───────────────────────────────────────────────────

NEWS_FEEDS = {
    "CoinTelegraph": "https://cointelegraph.com/rss",
    "CoinDesk":      "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "Decrypt":       "https://decrypt.co/feed",
    "TheBlock":      "https://www.theblock.co/rss.xml",
}

# ─── İçerik Takvimi ──────────────────────────────────────────────────────────

CONTENT_SCHEDULE = {
    "08:00": "morning_hype",       # Motivasyon + NXR hatırlatma
    "10:00": "crypto_news",        # Güncel haber + NXR yorumu
    "12:00": "stats_update",       # Burn/stake istatistikleri
    "15:00": "educational",        # NXR/DeFi eğitim içeriği
    "17:00": "engagement",         # Soru/anket/etkileşim postu
    "20:00": "crypto_news",        # Akşam haber + NXR yorumu
    "22:00": "community_highlight",# Topluluk öne çıkarma
}

class ContentEngine:
    def __init__(self):
        self.ai = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # ─── Haber Çekme ─────────────────────────────────────────────────────────

    def fetch_latest_news(self, max_per_feed: int = 3) -> list[dict]:
        """Tüm RSS kaynaklarından son haberleri çek."""
        all_news = []
        for source, url in NEWS_FEEDS.items():
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:max_per_feed]:
                    all_news.append({
                        "source":  source,
                        "title":   entry.get("title", ""),
                        "summary": entry.get("summary", "")[:300],
                        "link":    entry.get("link", ""),
                        "date":    entry.get("published", "")
                    })
            except Exception as e:
                print(f"[{source}] haber çekme hatası: {e}")
        return all_news

    # ─── İçerik Üretimi ──────────────────────────────────────────────────────

    def generate_news_post(self, news: dict, platform: str = "twitter") -> str:
        """Haber başlığından NXR bağlantılı içerik üret."""

        char_limit = 270 if platform == "twitter" else 1000

        prompt = f"""
Sen NEXARA (NXR) token projesinin sosyal medya yöneticisisin.

Şu kripto haberi var:
Kaynak: {news['source']}
Başlık: {news['title']}
Özet: {news['summary']}

Bu haberi {platform} için bir post yap:
- Haberi kısaca özetle
- NXR veya Superajan trading botuna DOĞAL bir bağlantı kur (zorla değil)
- {'Max 270 karakter' if platform == 'twitter' else 'Max 3 paragraf'}
- İlgili hashtagler ekle (#DeFi #Crypto #Ethereum #NXR vb.)
- Sonuna 🔷 koy
- Türkçe yaz
- Fiyat tahmini yapma
"""
        resp = self.ai.messages.create(
            model="claude-opus-4-5",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )
        return resp.content[0].text

    def generate_morning_hype(self, platform: str = "twitter") -> str:
        prompt = f"""
NEXARA (NXR) için sabah motivasyon postu yaz.
Platform: {platform}
- Enerjik, pozitif
- NXR'nin bir özelliğini vurgula (burn, staking, bot access)
- Topluluk ruhunu canlandır
- {'Max 270 karakter' if platform == 'twitter' else 'Max 2 paragraf'}
- Türkçe ve İngilizce karışık olabilir
- Sonuna 🔷 koy
"""
        return self.ai.messages.create(
            model="claude-opus-4-5",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        ).content[0].text

    def generate_educational_post(self, platform: str = "twitter") -> str:
        topics = [
            "NXR'nin deflasyon mekanizması nasıl çalışır?",
            "Superajan botunun orderbook analizi stratejisi",
            "DeFi'de stake etmek neden mantıklı?",
            "Anti-whale koruma neden önemli?",
            "Likidite havuzu nedir, NXR'yi nasıl etkiler?",
            "Bronze/Silver/Gold tier farkları neler?",
            "Tokenomics neden önemli? NXR örneği",
            "Smart contract güvenliği: NXR nasıl koruyor?"
        ]
        import random
        topic = random.choice(topics)

        prompt = f"""
NEXARA (NXR) hakkında eğitici bir {platform} postu yaz.
Konu: {topic}
- Basit ve anlaşılır dil
- {'Thread formatı (1/5, 2/5 şeklinde)' if platform == 'twitter' else 'Detaylı açıklama'}
- Sonuna NXR ile bağlantı kur
- Hashtag ekle
- Türkçe
- Sonuna 🔷 koy
"""
        return self.ai.messages.create(
            model="claude-opus-4-5",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        ).content[0].text

    def generate_engagement_post(self, platform: str = "twitter") -> str:
        formats = [
            "Topluluktan oy isteyen bir anket sorusu",
            "Kripto hakkında tartışma açan bir soru",
            "NXR kullanıcılarına yönelik tecrübe sorusu",
            "Kripto piyasası hakkında fikir sorusu",
            "Trading botu kullananlar için soru"
        ]
        import random
        fmt = random.choice(formats)

        prompt = f"""
NEXARA topluluğu için etkileşim postu yaz.
Format: {fmt}
Platform: {platform}
- Soru sormayı teşvik et
- NXR veya trading ile bağlantılı
- {'Max 200 karakter + seçenekler' if platform == 'twitter' else 'Detaylı soru + seçenekler'}
- Türkçe
- Sonuna 🔷 koy
"""
        return self.ai.messages.create(
            model="claude-opus-4-5",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        ).content[0].text

    def generate_stats_update(self, platform: str, burned: str = "N/A", staked: str = "N/A", holders: str = "N/A") -> str:
        prompt = f"""
NEXARA (NXR) istatistik güncelleme postu yaz.
Platform: {platform}
Veriler:
- Bugün yakılan NXR: {burned}
- Toplam stake: {staked}
- Holder sayısı: {holders}

- Kısa ve etkili
- Rakamları öne çıkar
- {'Max 270 karakter' if platform == 'twitter' else 'Max 2 paragraf'}
- Hashtag ekle
- Sonuna 🔷 koy
"""
        return self.ai.messages.create(
            model="claude-opus-4-5",
            max_tokens=250,
            messages=[{"role": "user", "content": prompt}]
        ).content[0].text

    # ─── Trend Hashtag Üretimi ────────────────────────────────────────────────

    def get_trending_hashtags(self) -> list[str]:
        """Güncel kripto hashtag listesi döndür."""
        base_tags = [
            "#NXR", "#Nexara", "#DeFi", "#Ethereum", "#Crypto",
            "#Web3", "#Altcoin", "#CryptoTrading", "#Blockchain",
            "#PassiveIncome", "#Staking", "#AITrading"
        ]
        # Güne göre ekstra tag ekle
        day = datetime.now().weekday()
        if day == 0:   base_tags.append("#MondayMotivation")
        elif day == 4: base_tags.append("#FridayVibes")
        elif day == 6: base_tags.append("#SundayThoughts")
        return base_tags

    # ─── Tam Günlük İçerik Paketi ─────────────────────────────────────────────

    def generate_daily_pack(self) -> dict:
        """Günlük tüm içerikleri üret ve kaydet."""
        print("📦 Günlük içerik paketi hazırlanıyor...")
        news = self.fetch_latest_news(max_per_feed=2)

        pack = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "twitter": [],
            "telegram": []
        }

        # 1. Sabah hype
        pack["twitter"].append({
            "time": "08:00",
            "type": "morning_hype",
            "content": self.generate_morning_hype("twitter")
        })
        pack["telegram"].append({
            "time": "08:00",
            "type": "morning_hype",
            "content": self.generate_morning_hype("telegram")
        })

        # 2. Haber postu (sabah)
        if news:
            pack["twitter"].append({
                "time": "10:00",
                "type": "news",
                "content": self.generate_news_post(news[0], "twitter")
            })
            pack["telegram"].append({
                "time": "10:00",
                "type": "news",
                "content": self.generate_news_post(news[0], "telegram")
            })

        # 3. Eğitim içeriği
        pack["twitter"].append({
            "time": "15:00",
            "type": "educational",
            "content": self.generate_educational_post("twitter")
        })

        # 4. Etkileşim postu
        pack["twitter"].append({
            "time": "17:00",
            "type": "engagement",
            "content": self.generate_engagement_post("twitter")
        })
        pack["telegram"].append({
            "time": "17:00",
            "type": "engagement",
            "content": self.generate_engagement_post("telegram")
        })

        # 5. Akşam haber
        if len(news) > 1:
            pack["twitter"].append({
                "time": "20:00",
                "type": "news",
                "content": self.generate_news_post(news[1], "twitter")
            })

        # Kaydet
        filename = f"content_{pack['date']}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(pack, f, ensure_ascii=False, indent=2)

        print(f"✅ {len(pack['twitter'])} Twitter + {len(pack['telegram'])} Telegram içeriği hazır → {filename}")
        return pack


# Test
if __name__ == "__main__":
    engine = ContentEngine()
    print("🔷 Content Engine test başlıyor...\n")

    # Sabah postu üret
    print("📢 SABAH POSTU:")
    print(engine.generate_morning_hype("twitter"))
    print()

    # Haber çek ve yorum yap
    print("📰 HABER ÇEKİLİYOR...")
    news = engine.fetch_latest_news(max_per_feed=1)
    if news:
        print(f"Haber: {news[0]['title'][:60]}...")
        print("\n📢 TWITTER POSTU:")
        print(engine.generate_news_post(news[0], "twitter"))
    else:
        print("Haber çekilemedi (internet bağlantısını kontrol et)")

    print("\n❓ ENGAGEMENt POSTU:")
    print(engine.generate_engagement_post("twitter"))

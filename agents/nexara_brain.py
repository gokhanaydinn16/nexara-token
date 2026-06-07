"""
NEXARA AI Brain — Tüm ajanların paylaştığı merkezi zeka.
Claude API üzerinden çalışır. NXR hakkında her soruyu cevaplar.
"""

import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
Sen NEXARA'nın resmi AI asistanısın. Adın NEX.

NEXARA (NXR) hakkında her şeyi biliyorsun:

TOKEN BİLGİLERİ:
- Toplam arz: 100,000,000 NXR
- Her transferde %2 yakılır (deflasyon)
- Her transferden %1 staking havuzuna gider
- Max cüzdan: 1,000,000 NXR (anti-whale)
- Staking APY: %12
- Kilit süresi: 30 gün

ERIŞIM TİERLERİ (NexaraAccess):
- Bronze: 10,000 NXR stake → Temel sinyaller
- Silver: 50,000 NXR stake → Whale takip + gelişmiş sinyaller
- Gold: 200,000 NXR stake → Tüm özellikler

SUPERAJAN BOT:
- Binance USD-M vadeli işlem piyasalarında çalışır
- Orderbook analizi, whale takibi, çapraz-piyasa arbitraj
- NXR stake edenlere açık

SÖZLEŞME ADRESLERİ (Testnet):
- Token: 0xa14F7e4DE163Bc05297AF005B6cD44A770842187
- Staking: 0xa589014ee01E4F4f473ABD5587d304fA4879F5E4

ROADMAP:
- Q2 2026: Token + Staking aktif ✅
- Q3 2026: Mainnet + Bot erişimi
- Q4 2026: Uniswap + CoinGecko
- 2027: Governance + Multi-exchange

DAVRANIŞIN:
- Enerjik, pozitif ve yardımsever ol
- Kısa ve net cevaplar ver (Telegram için max 3-4 paragraf)
- Asla fiyat tahmini yapma ("ay biter 10x olur" gibi)
- Asla "kesinlikle kazanırsın" deme
- Scam soruları gelirse kibarca reddet
- Türkçe sorulara Türkçe, İngilizce sorulara İngilizce cevap ver
- Her cevabın sonuna 🔷 emojisi koy
"""

class NexaraBrain:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.conversation_history = {}  # user_id → mesaj geçmişi

    def get_response(self, user_id: str, message: str) -> str:
        """Kullanıcıya Claude ile cevap üret."""

        # Konuşma geçmişini yönet (max 10 mesaj)
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []

        history = self.conversation_history[user_id]
        history.append({"role": "user", "content": message})

        # Max 10 mesaj tut
        if len(history) > 10:
            history = history[-10:]

        response = self.client.messages.create(
            model="claude-opus-4-5",
            max_tokens=500,
            system=SYSTEM_PROMPT,
            messages=history
        )

        reply = response.content[0].text
        history.append({"role": "assistant", "content": reply})
        self.conversation_history[user_id] = history

        return reply

    def get_welcome_message(self, username: str) -> str:
        """Yeni üye karşılama mesajı."""
        return self.client.messages.create(
            model="claude-opus-4-5",
            max_tokens=200,
            system=SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": f"Yeni bir üye katıldı: @{username}. Kısa ve samimi bir karşılama mesajı yaz. NXR'yi kısaca tanıt."
            }]
        ).content[0].text

    def get_daily_update(self, burned_today: str, total_staked: str) -> str:
        """Günlük istatistik mesajı."""
        return self.client.messages.create(
            model="claude-opus-4-5",
            max_tokens=300,
            system=SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": f"Günlük güncelleme mesajı yaz. Bugün {burned_today} NXR yakıldı, toplam {total_staked} NXR stake edildi. Motivasyonel ve kısa tut."
            }]
        ).content[0].text

# Singleton
brain = NexaraBrain()

"""
NEXARA — Tüm Ajanları Başlat
Tek komut: python start_all.py
"""

import os
import asyncio
import threading
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")

def start_telegram():
    """Telegram ajanını ayrı thread'de başlat."""
    from telegram_agent import main as tg_main
    print("🤖 Telegram Ajanı başlatılıyor...")
    tg_main()

def start_growth():
    """Growth ajanını ayrı thread'de başlat."""
    from growth_agent import NexaraGrowthAgent
    print("📈 Growth Ajanı başlatılıyor...")
    agent = NexaraGrowthAgent()
    agent.run()

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════╗
║     NEXARA OTONOM AJAN SİSTEMİ          ║
╠══════════════════════════════════════════╣
║  🤖 Telegram Community Manager          ║
║  📈 Growth & Content Agent              ║
║  🐦 Twitter Engagement Bot              ║
╠══════════════════════════════════════════╣
║  7/24 Çalışıyor — Durdur: Ctrl+C        ║
╚══════════════════════════════════════════╝
    """)

    # Eksik env kontrol
    required = {
        "ANTHROPIC_API_KEY":    "console.anthropic.com",
        "TELEGRAM_BOT_TOKEN":   "@BotFather'dan al",
        "TELEGRAM_CHANNEL_ID":  "Grup ID'si",
        "TWITTER_BEARER_TOKEN": "developer.twitter.com",
    }
    missing = [(k, v) for k, v in required.items() if not os.getenv(k)]
    if missing:
        print("❌ Eksik ayarlar (.env):\n")
        for key, hint in missing:
            print(f"  {key} → {hint}")
        print("\nagents/.env.example dosyasına bak.")
        exit(1)

    # Thread'leri başlat
    threads = [
        threading.Thread(target=start_telegram, name="Telegram", daemon=True),
        threading.Thread(target=start_growth,   name="Growth",   daemon=True),
    ]

    for t in threads:
        t.start()
        print(f"✅ {t.name} ajanı başlatıldı.")

    print("\n🔷 Tüm ajanlar çalışıyor. Log için growth_agent.log dosyasına bak.")
    print("Durdurmak için Ctrl+C\n")

    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print("\n⏹ Ajanlar durduruldu.")

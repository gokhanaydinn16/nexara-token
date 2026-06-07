"""Dashboard bileşen testleri"""
import sys
sys.path.insert(0, r'C:\Users\gokha\Desktop\nexara-token\agents')

PASS = "[PASS]"
FAIL = "[FAIL]"

def test(name, fn):
    try:
        result = fn()
        print(f"{PASS}  {name}" + (f" — {result}" if result else ""))
    except Exception as e:
        print(f"{FAIL}  {name}: {e}")

# 1. Modül importları
test("feedparser",         lambda: __import__("feedparser") and "OK")
test("anthropic",          lambda: __import__("anthropic") and "OK")
test("tweepy",             lambda: __import__("tweepy") and "OK")
test("telegram Bot",       lambda: __import__("telegram") and "OK")
test("schedule",           lambda: __import__("schedule") and "OK")
test("dotenv",             lambda: __import__("dotenv") and "OK")

# 2. ContentEngine
test("ContentEngine import", lambda: (
    __import__("content_engine", fromlist=["ContentEngine"]).ContentEngine and "OK"
))

# 3. ContentEngine metodları
from content_engine import ContentEngine
engine_methods = ["generate_morning_hype","generate_educational_post",
                  "generate_engagement_post","generate_news_post","fetch_latest_news"]
for m in engine_methods:
    test(f"ContentEngine.{m} mevcut", lambda m=m: hasattr(ContentEngine, m) and "OK")

# 4. RSS haber çekme
import feedparser
def test_rss():
    f = feedparser.parse("https://cointelegraph.com/rss")
    n = len(f.entries)
    assert n > 0, "0 haber geldi"
    return f"{n} haber çekildi"
test("RSS CoinTelegraph", test_rss)

# 5. Dashboard dosyaları var mı
from pathlib import Path
base = Path(r"C:\Users\gokha\Desktop\nexara-token")
critical_files = [
    "dashboard/app.py",
    "agents/telegram_agent.py",
    "agents/twitter_agent.py",
    "agents/growth_agent.py",
    "agents/content_engine.py",
    "agents/nexara_brain.py",
    "agents/start_all.py",
    "contracts/NexaraToken.sol",
    "contracts/NexaraStaking.sol",
    "WHITEPAPER.md",
]
for f in critical_files:
    test(f"Dosya: {f}", lambda f=f: "var" if (base/f).exists() else (_ for _ in ()).throw(FileNotFoundError(f)))

print("\n─────────────────────────────")
print("Test tamamlandı.")

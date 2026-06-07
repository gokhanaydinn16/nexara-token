# NEXARA Otonom Ajanları — Kurulum

## 2 Ajan Var

| Ajan | Ne Yapar |
|---|---|
| `telegram_agent.py` | 7/24 Telegram'da soru cevaplar, üye karşılar |
| `twitter_agent.py` | Mention'lara cevap verir, günlük tweet atar |

---

## ADIM 1 — Python Kur

Python 3.11+ lazım:
```
winget install Python.Python.3.11
```

---

## ADIM 2 — Paketleri Kur

```
cd C:\Users\gokha\Desktop\nexara-token\agents
pip install -r requirements.txt
```

---

## ADIM 3 — Telegram Bot Token Al (5 dakika)

1. Telegram'da **@BotFather**'a yaz
2. `/newbot` yaz
3. Bot adı: **Nexara Assistant**
4. Bot kullanıcı adı: **NexaraBot** (müsait olana kadar dene)
5. Token'ı kopyala → `.env`'e yaz

---

## ADIM 4 — Anthropic API Key Al (2 dakika)

1. **console.anthropic.com**'a git
2. API Keys → Create Key
3. Key'i kopyala → `.env`'e yaz

---

## ADIM 5 — .env Dosyasını Doldur

```
cp .env.example .env
# .env dosyasını düzenle, keylerini yapıştır
```

---

## ADIM 6 — Ajanları Başlat

### Telegram Ajanı:
```
python telegram_agent.py
```

### Twitter Ajanı:
```
python twitter_agent.py
```

### İkisini Aynı Anda (arka planda):
```
start /B python telegram_agent.py
start /B python twitter_agent.py
```

---

## Telegram Ajanının Yetenekleri

| Komut | Açıklama |
|---|---|
| `/start` | Hoşgeldin mesajı |
| `/tier` | Tier sistemi tablosu |
| `/stake` | Staking bilgisi |
| `/contract` | Sözleşme adresleri |
| `/roadmap` | Yol haritası |
| `/airdrop` | Aktif kampanyalar |
| Her soru | Claude AI ile akıllı cevap |

---

## Twitter Ajanının Yetenekleri

- Her 5 dakikada mention kontrol → AI ile cevap
- Her sabah 09:00 → Günlük tweet
- Her Pazartesi 10:00 → Haftalık istatistik
- Airdrop katılımcı adresi toplama

---

## Superajan ile Çakışır mı?

**HAYIR.** Bu ajanlar tamamen bağımsız:
- Farklı klasörde
- Farklı process
- Superajan koduna dokunmaz
- Superajan'ı bilmez bile

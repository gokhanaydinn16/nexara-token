# 🔷 NEXARA (NXR) — Başlangıç Rehberi

**Kurucu:** Gökhan Aydın
**Website:** https://nexara-token.netlify.app
**Token:** 0xa14F7e4DE163Bc05297AF005B6cD44A770842187
**Staking:** 0xa589014ee01E4F4f473ABD5587d304fA4879F5E4

---

## ✅ TAMAMLANANLAR

| İş | Durum |
|---|---|
| Akıllı sözleşmeler (Token, Staking, Access, Treasury) | ✅ Sepolia'da canlı |
| Profesyonel website (kurucu + vizyon) | ✅ nexara-token.netlify.app |
| Logo (NXR) | ✅ Hazır |
| Whitepaper | ✅ Hazır |
| CoinSniper listeleme | ✅ Tamamlandı (#91942) |
| Kontrol paneli (dashboard) | ✅ Çalışıyor |
| AI ajanları (Telegram + Twitter + Growth) | ✅ Kod hazır |
| 30 günlük Twitter içeriği | ✅ Hazır |
| Telegram kurulum paketi | ✅ Hazır |
| Tüm listing başvuru metinleri | ✅ Hazır |

---

## 📋 SENİN YAPACAKLARIN (Sırayla)

### 1️⃣ BUGÜN — Sosyal Medya (Ücretsiz)
- [ ] **Twitter aç:** @NexaraToken → bio + ilk tweet (`marketing/30-gun-twitter-takvimi.md` Gün 1)
- [ ] **Telegram grup aç:** @NexaraOfficial → (`marketing/telegram-kurulum-paketi.md`)
- [ ] Logo profil fotoğrafı: `website/nxr-logo-400.png`

### 2️⃣ BU HAFTA — Listeleme (Ücretsiz)
- [ ] CoinVote, GemFinder, Coinsniper (`listing/basvuru-paneli.html` aç, kopyala-yapıştır)
- [ ] Reddit r/CryptoMoonShots (`marketing/reddit-ann-post.txt`)
- [ ] BitcoinTalk ANN (`marketing/bitcointalk-ann.txt`)

### 3️⃣ MAINNET'E GEÇİŞ (~$21 Polygon ile)
- [ ] Polygon'a $5 MATIC al → MetaMask'a gönder
- [ ] `npx hardhat run scripts/deploy-polygon.js --network polygon`
- [ ] QuickSwap'ta likidite ekle (~$20)
- [ ] DexScreener otomatik çıkar (5 dk)

### 4️⃣ MAINNET SONRASI (Ücretsiz)
- [ ] CoinGecko başvurusu (`listing/coingecko-basvuru.txt`)
- [ ] CoinMarketCap başvurusu
- [ ] MEXC + Gate.io başvurusu (`listing/mexc-gate-basvuru.txt`)

---

## 📁 DOSYA HARİTASI

```
nexara-token/
├── BURADAN-BASLA.md          ← bu dosya
├── WHITEPAPER.md             ← proje belgesi
├── website/                  ← canlı site (nexara-token.netlify.app)
│   ├── index.html
│   └── nxr-logo-400.png      ← logo
├── contracts/                ← akıllı sözleşmeler
├── scripts/                  ← deploy scriptleri
│   ├── deploy-polygon.js     ← ucuz mainnet (~$0.50)
│   └── deploy-mainnet.js     ← Ethereum mainnet
├── marketing/
│   ├── 30-gun-twitter-takvimi.md   ← her gün 1 tweet
│   ├── telegram-kurulum-paketi.md  ← grup kurulumu
│   ├── reddit-ann-post.txt
│   └── bitcointalk-ann.txt
├── listing/
│   ├── basvuru-paneli.html   ← kopyala-yapıştır panel
│   ├── coingecko-basvuru.txt
│   └── mexc-gate-basvuru.txt
├── dashboard/                ← kontrol paneli (BASLAT.bat)
└── agents/                   ← AI ajanları
```

---

## 🚀 EN ÖNEMLİ 3 ADIM

1. **Twitter + Telegram aç** → topluluk başlasın (bugün, ücretsiz)
2. **Polygon mainnet** → token gerçek işlem görsün (~$21)
3. **30 günlük içeriği paylaş** → her gün 1 tweet, düzenli büyüme

---

*Trade smarter. Stake deeper. — Nexara Protocol*

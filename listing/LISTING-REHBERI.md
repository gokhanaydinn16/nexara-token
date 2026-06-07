# NEXARA (NXR) — Tam Listing Rehberi

## ÖNEMLİ: Listing Kategorileri

| Kategori | Ücret | Ne Zaman |
|---|---|---|
| DEX (Uniswap, vb.) | Ücretsiz ama likidite lazım | Mainnet sonrası |
| CoinGecko / CMC | Ücretsiz form | Mainnet + DEX sonrası |
| DexScreener / DEXTools | Otomatik, sıfır iş | DEX'e girince kendiliğinden |
| Küçük CEX | Genelde ücretsiz | Topluluk büyüyünce |
| Büyük CEX (Binance vb.) | 50,000$+ | Şimdilik hedef değil |

---

## ADIM 1 — Mainnet Deploy (önce bu)

Sepolia testnet → Ethereum mainnet
Maliyet: ~0.05-0.1 ETH (yaklaşık 150-300$)
Komut: `npm run deploy:mainnet`

---

## ADIM 2 — Uniswap V3 (En Önemli DEX)

### Neden Uniswap?
- Dünyanın en büyük DEX'i
- Listelenmek için izin gerekmez
- Bir likidite havuzu aç = NXR alınıp satılabilir

### Nasıl Yapılır?
1. app.uniswap.org → "New Position"
2. Token 1: ETH
3. Token 2: NXR kontrat adresi yapıştır
4. Fee tier: %1 seç (yeni token için ideal)
5. Fiyat aralığı belirle
6. Likidite ekle (min 500$ ETH + eşdeğer NXR önerilir)

### Minimum Likidite Tavsiyesi
- Düşük: 500$ ETH + 500$ değer NXR → Fiyat çok oynar
- Orta:  2,000$ ETH + 2,000$ değer NXR → Sağlıklı
- İdeal: 5,000$+ → Güvenilir görünüm

---

## ADIM 3 — PancakeSwap (BSC — Alternatif)

BSC ağı daha ucuz gas fee'si sunar.
Seçenek: Token'ı BSC'ye de deploy et → PancakeSwap'ta havuz aç
Maliyet: ~10-20$ (çok daha ucuz)

---

## ADIM 4 — Otomatik Listeler (DEX'e girince kendisi çıkar)

DEX'e likidite ekler eklemez şu siteler **otomatik olarak** NXR'yi listeler:

| Site | Yapılacak İş |
|---|---|
| DexScreener (dexscreener.com) | Hiçbir şey — otomatik |
| DEXTools (dextools.io) | Hiçbir şey — otomatik |
| GeckoTerminal (geckoterminal.com) | Hiçbir şey — otomatik |
| Ave.ai | Hiçbir şey — otomatik |
| Defined.fi | Hiçbir şey — otomatik |

Bu 5 site binlerce trader'ın yeni token aradığı yerlerdir.

---

## ADIM 5 — CoinGecko Başvurusu (Ücretsiz)

URL: https://www.coingecko.com/en/coins/submit

Gerekli bilgiler:
- Token adı, sembol, kontrat adresi
- Website URL
- Logo (200x200 PNG)
- Sosyal medya linkleri
- Whitepaper linki
- Uniswap havuz adresi (olmazsa kabul etmez)

Onay süresi: 2-8 hafta

### CoinGecko için hazırlanan metin:
```
Token Name: Nexara
Symbol: NXR
Network: Ethereum
Contract: 0xa14F7e4DE163Bc05297AF005B6cD44A770842187
Description: Nexara (NXR) is a deflationary DeFi token that 
tokenizes access to Superajan — an AI-powered trading bot on 
Binance USD-M perpetual futures. Holders stake NXR to unlock 
bot features and earn revenue share from bot profits.
Website: nexara-token.netlify.app
Twitter: twitter.com/NexaraToken
Telegram: t.me/NexaraOfficial
Whitepaper: [link]
```

---

## ADIM 6 — CoinMarketCap Başvurusu (Ücretsiz)

URL: https://coinmarketcap.com/request/

Gereklilikler:
- Aktif Uniswap havuzu (en az 10 işlem)
- Website + sosyal medya
- Min 100 holder (mainnet'te)
- Whitepaper

Onay süresi: 4-12 hafta

---

## ADIM 7 — Küçük CEX'ler (Ücretsiz Başvuru)

Bu borsalar ücretsiz veya çok düşük ücretle listing yapar:

| Borsa | Başvuru | Not |
|---|---|---|
| **MEXC** | mexc.com/listing | En kolay, token başvurusu açık |
| **Gate.io** | gate.io/listing | Topluluk oylaması sistemi var |
| **BitMart** | bitmart.com/listmytoken | Ücretsiz form |
| **LBank** | lbank.com/listing | Küçük projeler için uygun |
| **CoinEx** | coinex.com/listing | Form doldur, değerlendirirler |

### MEXC İçin Başvuru Metni:
```
Project Name: Nexara
Token Symbol: NXR
Total Supply: 100,000,000
Network: Ethereum ERC-20
Contract: [mainnet adresi]
Use Case: AI trading bot access tokenization
Unique Feature: Stake to access, revenue share, 2% deflationary burn
Community: [telegram + twitter üye sayısı]
Daily Volume: [Uniswap verisi]
Website: nexara-token.netlify.app
Whitepaper: [link]
```

---

## ADIM 8 — Topluluk Oylaması Platformları

Bu siteler proje listeler, topluluk oy verir, öne çıkanlar ilgi görür:

| Site | Yapılacak |
|---|---|
| **Coinvote.cc** | Ücretsiz kayıt, oy kampanyası başlat |
| **Coinhunt.cc** | Token ekle, günlük oy topla |
| **Coinsniper.net** | Yeni token ekle |
| **Gemfinder.io** | Ücretsiz listing |
| **Cryptorank.io** | Proje sayfası oluştur |

---

## TAM YOL HARİTASI

```
Şimdi:     Testnet aktif ✅
           Marketing hazır ✅
           
Adım 1:    Mainnet deploy (~150-300$ ETH)
Adım 2:    Uniswap V3 havuzu aç (~500$+ likidite)
Adım 3:    DexScreener/DEXTools otomatik çıkar
Adım 4:    CoinGecko + CMC başvurusu yap (ücretsiz)
Adım 5:    MEXC + Gate.io + BitMart başvuru (ücretsiz)
Adım 6:    Coinvote + Coinhunt oy kampanyası
Adım 7:    Topluluk büyüyünce büyük CEX hedefi
```

---

## ÖZET: Sıfır Para ile Yapılabilecekler

✅ DexScreener — Otomatik (DEX sonrası)
✅ DEXTools — Otomatik (DEX sonrası)
✅ GeckoTerminal — Otomatik (DEX sonrası)
✅ CoinGecko başvurusu — Ücretsiz form
✅ CoinMarketCap başvurusu — Ücretsiz form
✅ MEXC başvurusu — Ücretsiz form
✅ Gate.io başvurusu — Ücretsiz form
✅ BitMart başvurusu — Ücretsiz form
✅ Coinvote oy kampanyası — Ücretsiz
✅ Coinhunt oy kampanyası — Ücretsiz
✅ Coinsniper listing — Ücretsiz

Para gereken tek şey:
💰 Mainnet deploy + Uniswap likidite

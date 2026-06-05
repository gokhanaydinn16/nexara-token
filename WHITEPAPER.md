# NEXARA (NXR) — Whitepaper v1.0

## Özet

NEXARA (NXR), yapay zeka destekli kripto trading botlarına erişimi tokenize eden,
gelir paylaşımı ve stake mekanizmaları ile desteklenen bir DeFi protokolüdür.
Temel ürün: **Superajan** — Binance USD-M vadeli işlem piyasalarında çalışan,
orderbook analizi, whale akışı ve çapraz-piyasa arbitraj stratejilerini kullanan
kurumsal düzeyde bir trading motoru.

---

## 1. Problem

Kurumsal kalitede trading botları bugün sadece büyük fonların ve sofistike yatırımcıların
erişebildiği araçlardır. Bireysel yatırımcılar:

- Yüksek lisans ücreti ödemek zorunda kalır
- Algoritmanın ne yaptığını şeffaf biçimde göremez
- Botun kârından pay alamaz
- Governance'a katılamaz

---

## 2. Çözüm: NEXARA Ekosistemi

NXR, bu erişim bariyerini kaldırır. Token stake eden herkes:
- Superajan botuna tier'ına göre erişim kazanır
- Bot gelirinden oransal pay alır
- Protokol kararlarına oy kullanır

---

## 3. Superajan Bot

Superajan şu stratejileri eş zamanlı çalıştırır:

| Strateji | Açıklama |
|---|---|
| Orderbook Imbalance | Alış/satış baskısını gerçek zamanlı ölçer |
| Whale Flow Signal | Büyük cüzdan hareketlerini takip eder |
| Cross-Market Lag | Spot/vadeli fiyat farklarından arbitraj |
| Conviction Imbalance | Yüksek güvenlik skoru olan fırsatları seçer |
| PM Cohort Flow | Polymarket akışından momentum sinyali |

---

## 4. Token Utility — NXR Neden Değerli?

### 4.1 Erişim Katmanı (NexaraAccess)

| Tier | Gerekli Stake | Erişim |
|---|---|---|
| Bronze | 10,000 NXR | Temel sinyaller, 3 parite |
| Silver | 50,000 NXR | Tüm sinyaller, whale takip, 10 parite |
| Gold | 200,000 NXR | Tüm özellikler, öncelikli destek, sınırsız |

### 4.2 Gelir Paylaşımı (NexaraTreasury)

Bot abonelik gelirleri:
- %60 → Stake eden NXR sahiplerine dağıtılır
- %25 → Protokol geliştirme fonu
- %15 → Likidite derinliği koruması

### 4.3 Deflasyon Mekanizması

- Her NXR transferinde **%2 yakılır** → arz sürekli azalır
- Her transferin **%1'i** staking havuzuna gider → pasif getiri

### 4.4 Governance

- NXR stake edenler yeni strateji eklenmesine oy verir
- Fee değişiklikleri oy ile belirlenir
- Treasury harcamaları şeffaf ve oylamalı

---

## 5. Tokenomics

**Toplam Arz: 100,000,000 NXR**

| Kategori | Miktar | Oran | Kilit |
|---|---|---|---|
| Staking Ödülleri | 25,000,000 | %25 | Anlık dağıtım |
| Likidite Havuzu | 20,000,000 | %20 | 6 ay |
| Ekip & Geliştirme | 15,000,000 | %15 | 12 ay vesting |
| Topluluk & Marketing | 15,000,000 | %15 | 3 ay |
| Hazine (Treasury) | 15,000,000 | %15 | Governance kontrolü |
| IDO / Başlangıç Satışı | 10,000,000 | %10 | Anlık |

---

## 6. Yol Haritası

### Faz 1 — Temel (Tamamlandı ✅)
- [x] Token sözleşmesi deploy (Sepolia testnet)
- [x] Staking sözleşmesi deploy
- [x] Burn mekanizması aktif
- [x] Anti-whale koruması

### Faz 2 — Erişim Sistemi (Q3 2026)
- [ ] NexaraAccess sözleşmesi mainnet
- [ ] NexaraTreasury mainnet
- [ ] Superajan bot tier doğrulama entegrasyonu
- [ ] Dashboard (web arayüzü)

### Faz 3 — Büyüme (Q4 2026)
- [ ] Uniswap V3 likidite havuzu
- [ ] CoinGecko / CoinMarketCap listeleme
- [ ] Telegram bot entegrasyonu
- [ ] Mobil uygulama

### Faz 4 — Ekosistem (2027)
- [ ] Governance oy sistemi
- [ ] Çoklu exchange desteği
- [ ] NXR ile bot strateji NFT'leri
- [ ] Cross-chain köprü

---

## 7. Güvenlik

- OpenZeppelin sözleşmeleri kullanıldı
- ReentrancyGuard ile reentrancy koruması
- Anti-whale: max cüzdan %1 ile sınırlı
- Audit: Mainnet öncesi bağımsız denetim planlanmaktadır

---

## 8. Ekip

Superajan, Binance USD-M vadeli işlem piyasaları üzerine uzmanlaşmış
geliştirici ekibi tarafından inşa edilmiştir.

---

## 9. Yasal Uyarı

NXR bir yatırım aracı değildir. Token, Nexara protokolüne erişim ve
governance haklarını temsil eder. Kripto varlıklar yüksek risk içerir.
Yatırım kararlarınızı kendi araştırmanıza dayandırınız.

---

*Nexara Protocol — nexara.io (yakında)*
*v1.0 — Haziran 2026*

# Nexara Pay — Kurulum & Kullanım

**En doğru, yasal, sana ait ödeme sistemi.**

---

## NE YAPTIK

| Bileşen | Açıklama | Lisans? |
|---|---|---|
| **NexaraPay.sol** | Kripto ödeme akıllı sözleşmesi | ❌ Gerekmez |
| **pay.html** | Checkout sayfası (kripto + kart) | ❌ Gerekmez |
| Kart ödemesi | Transak (lisanslı on-ramp) | ✅ Transak'ta var |

**Pay Gateway adresi:** `0xA8a25e6c8A80B4c7456168951190037fb757c119` (Sepolia)

---

## NASIL ÇALIŞIR

### 🔷 Kripto Ödeme (şimdi çalışır, lisanssız)
```
Müşteri → Cüzdan bağla → ETH veya NXR ile öde
       → Para DOĞRUDAN treasury'ne gelir
       → NXR ile ödeyene otomatik %5 indirim
```
- Aracı yok, banka yok, kesinti yok
- Her ödeme blockchain'de kayıtlı (orderId ile takip)
- %100 sana ait

### 💳 Kart Ödemesi (Transak ile, yasal)
```
Müşteri → "Pay with Card" → Transak ekranı açılır
       → Kartını Transak'a girer (lisans onlarda)
       → NXR/ETH müşteri cüzdanına gelir
```
- **Sana lisans gerekmez** — Transak lisanslı
- Visa, Mastercard, Apple Pay, Google Pay, banka havalesi
- 160+ ülke

---

## KART ÖDEMESİNİ AKTİF ETMEK (3 adım)

1. **transak.com** → "Get API Key" → ücretsiz partner hesabı aç
2. KYC/şirket bilgisi (Transak ister, çünkü lisans onlarda)
3. API anahtarını al → `pay.html` içinde şu satıra koy:
   ```js
   const TRANSAK_API_KEY = "BURAYA_ANAHTAR";
   ```
4. Kaydet, yeniden deploy et → kart ödemesi canlı

> Alternatif on-ramp'ler: MoonPay, Ramp Network, Mercuryo — hepsi aynı mantık.

---

## TÜRKİYE'DE TL KARTI İÇİN (mal/hizmet satışı)

Eğer kripto değil de **TL ile mal/hizmet** satacaksan:

| Sağlayıcı | Gereklilik |
|---|---|
| **Shopier** | Sadece kimlik (şirketsiz başlanır!) |
| **iyzico** | Şirket/şahıs |
| **PayTR** | Şirket/şahıs |

Bunların entegrasyon kodunu da ekleyebilirim — söyle yeterli.

---

## MAINNET'E GEÇİŞ

Şu an Sepolia testnet'te. Gerçek para için:
1. `scripts/deploy-polygon.js` veya `deploy-mainnet.js` ile NexaraPay'i mainnet'e at
2. `pay.html` içindeki adresleri mainnet adresleriyle güncelle
3. Transak'ı production moduna al

---

## YASAL NOT

- **Kripto kabul** (kendi hizmetin için): çoğu yerde lisanssız serbest
- **Kart işleme**: ASLA kendin yapma → her zaman lisanslı sağlayıcı (Transak/iyzico)
- Vergi: gelirlerini beyan et (her ülkede zorunlu)

Bu mimari ile **hem bağımsızsın hem yasalsın.** 🔷

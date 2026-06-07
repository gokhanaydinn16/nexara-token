# 🖥️ Oracle Ücretsiz Sunucu + BTCPay Server Kurulum Rehberi

**Hedef:** Tam bağımsız, kendine ait Bitcoin/Lightning ödeme merkezi.
**Maliyet:** $0 (Oracle Always Free sunucu)

---

## ⚠️ ÖNCE BİLMEN GEREKEN

- Oracle hesabı açarken **kredi kartı doğrulaması** ister (sadece kimlik için, **para çekilmez** — Always Free).
- BTCPay, **kendi sunucunda** çalışır → kimse kapatamaz, para sende.
- Bitcoin node senkronizasyonu birkaç saat sürer (pruned mod ile hızlı).

---

## ADIM 1 — Oracle Cloud Hesabı (10 dk)

1. **cloud.oracle.com** → "Start for free"
2. Ülke: **Türkiye**, e-posta gir
3. Telefon doğrulama (SMS kodu)
4. **Kredi kartı** doğrulama (para çekilmez, sadece kimlik)
5. Hesap onaylanır

> ⚠️ Kart bilgisini SEN gireceksin (benim güvenlik sınırım — kart bilgisi giremem).

---

## ADIM 2 — Ücretsiz Sunucu (VM) Oluştur (5 dk)

1. Oracle panel → **"Create a VM instance"**
2. İsim: `nexara-pay`
3. Image: **Ubuntu 22.04**
4. Shape: **VM.Standard.A1.Flex** (ARM — Always Free)
   - OCPU: 2-4, RAM: 12-24 GB (ücretsiz sınır içinde)
5. **SSH key:** "Generate a key pair" → **private key'i indir** (sakla!)
6. **Create**

---

## ADIM 3 — Ağ Ayarı (portları aç)

1. VM → "Virtual Cloud Network" → Security List
2. **Ingress Rules** ekle:
   - Port **80** (HTTP) → 0.0.0.0/0
   - Port **443** (HTTPS) → 0.0.0.0/0
3. Save

---

## ADIM 4 — Sunucuya Bağlan

**Windows'ta (PowerShell):**
```powershell
ssh -i "indirdigin-key.key" ubuntu@SUNUCU_IP
```
(SUNUCU_IP = Oracle panelinde VM'in "Public IP")

---

## ADIM 5 — BTCPay Kur (tek komut)

Sunucuya bağlandıktan sonra:
```bash
# Kurulum scriptini indir
wget https://raw.githubusercontent.com/[repo]/install-btcpay.sh
# VEYA bu repodan kopyala: scripts/install-btcpay.sh

# Domain ayarla (varsa) veya IP kullan
export BTCPAY_HOST="pay.SENIN-DOMAIN.com"

# Kur
bash install-btcpay.sh
```

10-30 dakika sürer (otomatik). Bitince `https://BTCPAY_HOST` hazır.

---

## ADIM 6 — BTCPay İlk Ayar (tarayıcıda)

1. `https://pay.SENIN-DOMAIN.com` → aç
2. **Admin hesabı** oluştur (ilk giren admin)
3. **Store** oluştur: `Nexara Pay`
4. **Wallet bağla:**
   - Kendi cüzdanının **xpub**'unu gir (non-custodial — anahtar SENDE)
   - Veya BTCPay'in cüzdanını oluştur, seed'i KAYDET
5. **Settings → Pay Button** → kod al

---

## ADIM 7 — Website'ye Bağla

BTCPay'den aldığın "Pay Button" kodunu `pay.html`'e eklerim:
- Müşteri "Pay with Bitcoin" → BTCPay faturası → öde
- Para **doğrudan senin cüzdanına** (aracı yok)

---

## DOMAIN (opsiyonel ama önerilir)

BTCPay için domain iyi olur (`pay.nexara.com` gibi):
- **Ücretsiz domain:** Freenom (.tk, .ml) veya
- **Ucuz (~$1/yıl):** Namecheap, Porkbun
- Domain → Oracle IP'ye yönlendir (A record)

Domain yoksa IP ile de çalışır ama HTTPS sertifikası için domain gerekir.

---

## SONUÇ

```
Oracle Sunucu (ücretsiz)
└── BTCPay Server
    ├── Bitcoin (on-chain)
    ├── Lightning (anlık)
    ├── %0 komisyon
    ├── Non-custodial (para SENDE)
    └── Kimseye bağımlı DEĞİL
```

➕ NexaraPay (ETH/NXR) = Tam bağımsız kripto ödeme merkezi 🔷

---

## NE LAZIM (senden)

| Adım | Kim yapar |
|---|---|
| Oracle hesabı + kart doğrulama | SEN (güvenlik) |
| VM oluşturma | SEN (panelde) veya birlikte |
| SSH bağlantı | Birlikte (komutu ben veririm) |
| BTCPay kurulum | BEN (script ile) |
| pay.html entegrasyon | BEN |

**Sen Oracle hesabını aç + VM oluştur → IP'yi ve SSH key'i ver → gerisini ben kurarım.**

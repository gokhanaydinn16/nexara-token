#!/bin/bash
# ════════════════════════════════════════════════════════════
# NEXARA PAY — BTCPay Server Tek Komutluk Kurulum
# Sunucuda (Ubuntu) çalıştır: bash install-btcpay.sh
# ════════════════════════════════════════════════════════════
# Tam bağımsız, non-custodial, %0 komisyon Bitcoin + Lightning ödeme

set -e

echo "╔══════════════════════════════════════════╗"
echo "║   NEXARA PAY — BTCPay Server Kurulumu    ║"
echo "╚══════════════════════════════════════════╝"

# ── 1. Sistem güncelle ──────────────────────────────────────
echo "[1/6] Sistem güncelleniyor..."
sudo apt-get update -y && sudo apt-get upgrade -y

# ── 2. Gerekli araçlar ──────────────────────────────────────
echo "[2/6] Git ve araçlar kuruluyor..."
sudo apt-get install -y git curl

# ── 3. BTCPay deposu ────────────────────────────────────────
echo "[3/6] BTCPay Server indiriliyor..."
if [ ! -d "btcpayserver-docker" ]; then
  git clone https://github.com/btcpayserver/btcpayserver-docker
fi
cd btcpayserver-docker

# ── 4. Ayarlar ──────────────────────────────────────────────
# ÖNEMLİ: BTCPAY_HOST'u kendi domainin yap (örn: pay.nexara.com)
# Domain yoksa sunucu IP'si ile de çalışır ama domain önerilir
echo "[4/6] Ayarlar yapılıyor..."

export BTCPAY_HOST="${BTCPAY_HOST:-pay.nexara-token.com}"
export NBITCOIN_NETWORK="mainnet"
export BTCPAYGEN_CRYPTO1="btc"
export BTCPAYGEN_LIGHTNING="lnd"          # Lightning Network (anlık ödeme)
export BTCPAYGEN_ADDITIONAL_FRAGMENTS="opt-save-storage-s"
export BTCPAYGEN_REVERSEPROXY="nginx"
export LETSENCRYPT_EMAIL="gokhanaydin_16@hotmail.com"

# ── 5. Kurulum ──────────────────────────────────────────────
echo "[5/6] BTCPay kuruluyor (bu 10-30 dk sürebilir, blockchain pruned mod)..."
. ./btcpay-setup.sh -i

# ── 6. Bitti ────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║          BTCPAY SERVER KURULDU!                     ║"
echo "╠══════════════════════════════════════════════════════╣"
echo "║ Erişim: https://$BTCPAY_HOST"
echo "║                                                      ║"
echo "║ SONRAKI ADIMLAR:                                    ║"
echo "║ 1. Tarayıcıda yukarıdaki adrese git                 ║"
echo "║ 2. Admin hesabı oluştur (ilk giren admin olur)      ║"
echo "║ 3. Store oluştur: 'Nexara Pay'                      ║"
echo "║ 4. Wallet bağla (kendi cüzdanın - non-custodial)    ║"
echo "║ 5. Payment Button / API al → pay.html'e ekle        ║"
echo "║                                                      ║"
echo "║ Bitcoin node senkronize olurken (birkaç saat)       ║"
echo "║ küçük ödemeler yine de alınabilir.                  ║"
echo "╚══════════════════════════════════════════════════════╝"

const { ethers } = require("ethers");
const fs = require("fs");
const path = require("path");

const wallet = ethers.Wallet.createRandom();

console.log("\n========================================");
console.log("   NEXARA (NXR) — Test Cüzdanı");
console.log("========================================");
console.log("Adres      :", wallet.address);
console.log("Private Key:", wallet.privateKey);
console.log("Mnemonic   :", wallet.mnemonic.phrase);
console.log("========================================");
console.log("UYARI: Bu bilgileri güvenli bir yere kaydet!");
console.log("Bu sadece TEST cüzdanıdır, gerçek para koyma.");
console.log("========================================\n");

const envPath = path.join(__dirname, "../.env");
const envContent = `# Sepolia public RPC (API key gerekmez)
RPC_URL=https://ethereum-sepolia-rpc.publicnode.com

# Test cüzdanı private key (ASLA gerçek para koyma)
PRIVATE_KEY=${wallet.privateKey}

# Etherscan API key (verify için - şimdilik boş bırakılabilir)
ETHERSCAN_API_KEY=
`;

fs.writeFileSync(envPath, envContent);
console.log(".env dosyası otomatik oluşturuldu.");
console.log("\nSıradaki adım: Sepolia test ETH al");
console.log("Adresin:", wallet.address);
console.log("\nBu adrese test ETH almak için:");
console.log("1. https://faucet.chainstack.com/sepolia-testnet-faucet");
console.log("   veya");
console.log("2. https://www.alchemy.com/faucets/ethereum-sepolia");
console.log("\nAdresi kopyalayıp faucet sitesine yapıştır, 0.5 ETH gönderir.");

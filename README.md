# 🔷 Nexara (NXR)

**The Token That Powers AI Trading**

Nexara (NXR) is a deflationary ERC-20 token that tokenizes access to **Superajan**, an AI-powered algorithmic trading bot on Binance USD-M perpetual futures. Stake NXR to unlock tiered bot access and earn a share of trading revenue.

🌐 **Website:** https://nexara-token.netlify.app
🛡️ **Audit:** https://nexara-token.netlify.app/audit.html (0 critical issues)
🐦 **Twitter:** [@NexaraNXR](https://x.com/NexaraNXR)

---

## ✨ Features

- 🔥 **2% burn** on every transfer (deflationary)
- 📈 **12% APY** staking rewards
- 🛡️ **Anti-whale** protection (max 1% per wallet)
- 🤖 **AI bot access** via staking tiers (Bronze/Silver/Gold)
- 💰 **Revenue sharing** with stakers
- 💳 **Nexara Pay** — crypto payment gateway (ETH/NXR/USDT)

---

## 📜 Smart Contracts

| Contract | Description |
|---|---|
| `NexaraToken.sol` | ERC-20 token with burn, staking fee, anti-whale |
| `NexaraStaking.sol` | 12% APY staking, 30-day lock |
| `NexaraAccess.sol` | Tiered bot access (stake-to-access) |
| `NexaraTreasury.sol` | Revenue distribution to stakers |
| `NexaraPay.sol` | Self-hosted crypto payment gateway |

**Deployed (Sepolia Testnet):**
- Token: `0xa14F7e4DE163Bc05297AF005B6cD44A770842187`
- Staking: `0xa589014ee01E4F4f473ABD5587d304fA4879F5E4`
- Pay: `0xA8a25e6c8A80B4c7456168951190037fb757c119`

---

## 🛠️ Tech Stack

- **Solidity** 0.8.20 + **OpenZeppelin** (audited libraries)
- **Hardhat** development environment
- **ReentrancyGuard** + **SafeERC20** security
- **Slither** static analysis (0 critical findings)

---

## 🚀 Build & Deploy

```bash
npm install
npx hardhat compile
npx hardhat run scripts/deploy.js --network sepolia
```

---

## 🔒 Security

- Built on OpenZeppelin audited contracts
- ReentrancyGuard on all value-handling functions
- Automated audit with Slither (see [audit report](https://nexara-token.netlify.app/audit.html))
- No hidden mint, fixed supply

---

## 🗺️ Roadmap

- ✅ Q2 2026 — Token + Staking deployed
- 🔄 Q3 2026 — Mainnet + Bot tier integration
- 🔜 Q4 2026 — Uniswap + CoinGecko listing
- 🔮 2027 — Governance + Multi-exchange

---

## 📄 License

MIT

---

*Founded by Gökhan Aydın · Trade smarter. Stake deeper. 🔷*

/**
 * NEXARA — Polygon Mainnet Deploy (~$0.50 toplam)
 *
 * HAZIRLIK (5 dakika, ücretsiz):
 * 1. MetaMask'ta Polygon ağı ekle (chainlist.org)
 * 2. Coinbase veya Binance'ten $2 MATIC al → MetaMask'a gönder
 * 3. .env dosyasına ekle:
 *    POLYGON_RPC_URL=https://polygon-rpc.com
 *    PRIVATE_KEY=0x...
 *
 * ÇALIŞTIR:
 *    npx hardhat run scripts/deploy-polygon.js --network polygon
 */

const { ethers } = require("hardhat");
const fs = require("fs");

async function main() {
  const [deployer] = await ethers.getSigners();
  const balance = await ethers.provider.getBalance(deployer.address);

  console.log("╔══════════════════════════════════════════╗");
  console.log("║   NEXARA (NXR) — POLYGON DEPLOY (~$0.50)║");
  console.log("╚══════════════════════════════════════════╝");
  console.log(`Deployer : ${deployer.address}`);
  console.log(`Balance  : ${ethers.formatEther(balance)} MATIC\n`);

  if (parseFloat(ethers.formatEther(balance)) < 0.5) {
    throw new Error("Yetersiz MATIC! En az 0.5 MATIC lazım (~$0.30).");
  }

  // Deploy sırası
  const deploys = [
    ["NexaraToken",    [deployer.address]],
    ["NexaraStaking",  null], // token address sonra
    ["NexaraAccess",   null],
    ["NexaraTreasury", null],
  ];

  let tokenAddr, stakingAddr, accessAddr, treasuryAddr;

  console.log("[1/5] NexaraToken...");
  const Token = await (await ethers.getContractFactory("NexaraToken")).deploy(deployer.address);
  await Token.waitForDeployment();
  tokenAddr = await Token.getAddress();
  console.log(`      ✓ ${tokenAddr}`);

  console.log("[2/5] NexaraStaking...");
  const Staking = await (await ethers.getContractFactory("NexaraStaking")).deploy(tokenAddr, deployer.address);
  await Staking.waitForDeployment();
  stakingAddr = await Staking.getAddress();
  console.log(`      ✓ ${stakingAddr}`);

  console.log("[3/5] NexaraAccess...");
  const Access = await (await ethers.getContractFactory("NexaraAccess")).deploy(tokenAddr, deployer.address);
  await Access.waitForDeployment();
  accessAddr = await Access.getAddress();
  console.log(`      ✓ ${accessAddr}`);

  console.log("[4/5] NexaraTreasury...");
  const Treasury = await (await ethers.getContractFactory("NexaraTreasury")).deploy(tokenAddr, deployer.address);
  await Treasury.waitForDeployment();
  treasuryAddr = await Treasury.getAddress();
  console.log(`      ✓ ${treasuryAddr}`);

  console.log("[5/5] Bağlantılar kuruluyor...");
  const token = await ethers.getContractAt("NexaraToken", tokenAddr);
  await (await token.setStakingPool(stakingAddr)).wait();
  await (await Access.setTreasury(treasuryAddr)).wait();
  await (await token.setExcludedFromFees(accessAddr, true)).wait();
  await (await token.setExcludedFromFees(treasuryAddr, true)).wait();
  await (await token.setExcludedFromMaxWallet(accessAddr, true)).wait();
  await (await token.setExcludedFromMaxWallet(treasuryAddr, true)).wait();
  await (await token.transfer(stakingAddr, ethers.parseEther("25000000"))).wait();
  console.log("      ✓ 25,000,000 NXR staking'e gönderildi.");

  const result = {
    network: "polygon",
    deployer: deployer.address,
    timestamp: new Date().toISOString(),
    contracts: { NexaraToken: tokenAddr, NexaraStaking: stakingAddr, NexaraAccess: accessAddr, NexaraTreasury: treasuryAddr }
  };
  fs.writeFileSync("polygon-addresses.json", JSON.stringify(result, null, 2));

  console.log("\n╔══════════════════════════════════════════════════════╗");
  console.log("║           POLYGON DEPLOY TAMAMLANDI!                ║");
  console.log("╠══════════════════════════════════════════════════════╣");
  console.log(`║ Token    : ${tokenAddr}`);
  console.log(`║ Staking  : ${stakingAddr}`);
  console.log("╠══════════════════════════════════════════════════════╣");
  console.log("║ PolygonScan:                                         ║");
  console.log(`║ https://polygonscan.com/address/${tokenAddr.slice(0,20)}...`);
  console.log("╠══════════════════════════════════════════════════════╣");
  console.log("║ SONRAKI: QuickSwap'ta likidite ekle (~$20 MATIC)    ║");
  console.log("║ https://quickswap.exchange/#/pools                   ║");
  console.log("╚══════════════════════════════════════════════════════╝");
  console.log("\nVerify:");
  console.log(`npx hardhat verify --network polygon ${tokenAddr} "${deployer.address}"`);
}

main().catch(e => { console.error(e); process.exit(1); });

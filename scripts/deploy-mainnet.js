/**
 * NEXARA — Ethereum Mainnet Deploy
 * Çalıştır: npx hardhat run scripts/deploy-mainnet.js --network mainnet
 *
 * ÖNCE KONTROL ET:
 * 1. .env dosyasında MAINNET_RPC_URL ve PRIVATE_KEY var mı?
 * 2. Cüzdanda en az 0.15 ETH var mı? (deploy + likidite için)
 * 3. ETHERSCAN_API_KEY var mı? (verify için)
 */

const { ethers } = require("hardhat");

async function main() {
  const [deployer] = await ethers.getSigners();
  const balance = await ethers.provider.getBalance(deployer.address);

  console.log("╔══════════════════════════════════════════════╗");
  console.log("║     NEXARA (NXR) — MAINNET DEPLOY           ║");
  console.log("╚══════════════════════════════════════════════╝");
  console.log(`\nDeployer : ${deployer.address}`);
  console.log(`Balance  : ${ethers.formatEther(balance)} ETH`);

  if (parseFloat(ethers.formatEther(balance)) < 0.1) {
    throw new Error("Yetersiz ETH! En az 0.1 ETH lazım.");
  }

  console.log("\n[1/5] NexaraToken deploy ediliyor...");
  const Token = await ethers.getContractFactory("NexaraToken");
  const token = await Token.deploy(deployer.address);
  await token.waitForDeployment();
  const tokenAddr = await token.getAddress();
  console.log(`      Token: ${tokenAddr}`);

  console.log("[2/5] NexaraStaking deploy ediliyor...");
  const Staking = await ethers.getContractFactory("NexaraStaking");
  const staking = await Staking.deploy(tokenAddr, deployer.address);
  await staking.waitForDeployment();
  const stakingAddr = await staking.getAddress();
  console.log(`      Staking: ${stakingAddr}`);

  console.log("[3/5] NexaraAccess deploy ediliyor...");
  const Access = await ethers.getContractFactory("NexaraAccess");
  const access = await Access.deploy(tokenAddr, deployer.address);
  await access.waitForDeployment();
  const accessAddr = await access.getAddress();
  console.log(`      Access: ${accessAddr}`);

  console.log("[4/5] NexaraTreasury deploy ediliyor...");
  const Treasury = await ethers.getContractFactory("NexaraTreasury");
  const treasury = await Treasury.deploy(tokenAddr, deployer.address);
  await treasury.waitForDeployment();
  const treasuryAddr = await treasury.getAddress();
  console.log(`      Treasury: ${treasuryAddr}`);

  console.log("[5/5] Sözleşmeler bağlanıyor...");
  await (await token.setStakingPool(stakingAddr)).wait();
  await (await access.setTreasury(treasuryAddr)).wait();
  await (await token.setExcludedFromFees(accessAddr, true)).wait();
  await (await token.setExcludedFromFees(treasuryAddr, true)).wait();
  await (await token.setExcludedFromMaxWallet(accessAddr, true)).wait();
  await (await token.setExcludedFromMaxWallet(treasuryAddr, true)).wait();

  // Staking için 25M NXR gönder
  await (await token.transfer(stakingAddr, ethers.parseEther("25000000"))).wait();
  console.log("      25,000,000 NXR staking contract'a gönderildi.");

  // Sonuçları kaydet
  const result = {
    network: "mainnet",
    deployer: deployer.address,
    timestamp: new Date().toISOString(),
    contracts: {
      NexaraToken:    tokenAddr,
      NexaraStaking:  stakingAddr,
      NexaraAccess:   accessAddr,
      NexaraTreasury: treasuryAddr,
    }
  };

  require("fs").writeFileSync(
    "mainnet-addresses.json",
    JSON.stringify(result, null, 2)
  );

  console.log("\n╔══════════════════════════════════════════════╗");
  console.log("║        MAINNET DEPLOY TAMAMLANDI!           ║");
  console.log("╠══════════════════════════════════════════════╣");
  console.log(`║ Token    : ${tokenAddr}`);
  console.log(`║ Staking  : ${stakingAddr}`);
  console.log(`║ Access   : ${accessAddr}`);
  console.log(`║ Treasury : ${treasuryAddr}`);
  console.log("╠══════════════════════════════════════════════╣");
  console.log("║ SONRAKI ADIMLAR:                            ║");
  console.log("║ 1. Etherscan'da verify et (aşağıdaki komut)║");
  console.log("║ 2. Uniswap'ta likidite ekle                 ║");
  console.log("║ 3. Website'yi güncelle (yeni adreslerle)    ║");
  console.log("║ 4. CoinGecko başvurusu yap                  ║");
  console.log("╚══════════════════════════════════════════════╝");
  console.log("\nVerify komutları:");
  console.log(`npx hardhat verify --network mainnet ${tokenAddr} "${deployer.address}"`);
  console.log(`npx hardhat verify --network mainnet ${stakingAddr} "${tokenAddr}" "${deployer.address}"`);
  console.log(`npx hardhat verify --network mainnet ${accessAddr} "${tokenAddr}" "${deployer.address}"`);
  console.log(`npx hardhat verify --network mainnet ${treasuryAddr} "${tokenAddr}" "${deployer.address}"`);
}

main().catch(e => { console.error(e); process.exit(1); });

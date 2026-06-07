/**
 * NEXARA — Uniswap V3 Likidite Havuzu
 *
 * Bu script otomatik olarak:
 * 1. ETH/NXR çifti için Uniswap V3 pool oluşturur
 * 2. İlk likiditeyi ekler
 * 3. Başlangıç fiyatını belirler
 *
 * Önce mainnet-addresses.json dosyasının oluşturulmuş olması lazım.
 */

const { ethers } = require("hardhat");
const fs = require("fs");

// Uniswap V3 adresleri (Ethereum Mainnet)
const UNISWAP = {
  factory:         "0x1F98431c8aD98523631AE4a59f267346ea31F984",
  positionManager: "0xC36442b4a4522E871399CD717aBDD847Ab11FE88",
  WETH:            "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
};

// Başlangıç fiyatı: 1 ETH = 1,000,000 NXR → 1 NXR = ~0.003$ (ETH=3000$)
// İstediğin fiyata göre değiştir
const INITIAL_PRICE_NXR_PER_ETH = 1_000_000n;

async function main() {
  // Mainnet adreslerini oku
  if (!fs.existsSync("mainnet-addresses.json")) {
    throw new Error("mainnet-addresses.json bulunamadı. Önce deploy-mainnet.js çalıştır.");
  }
  const addresses = JSON.parse(fs.readFileSync("mainnet-addresses.json"));
  const TOKEN_ADDR = addresses.contracts.NexaraToken;

  const [deployer] = await ethers.getSigners();
  console.log("╔══════════════════════════════════════════════╗");
  console.log("║    NEXARA — UNISWAP V3 LİKİDİTE EKLEME     ║");
  console.log("╚══════════════════════════════════════════════╝");
  console.log(`\nDeployer : ${deployer.address}`);
  console.log(`Token    : ${TOKEN_ADDR}`);

  const ETH_AMOUNT = ethers.parseEther("0.5");  // 0.5 ETH likidite
  const NXR_AMOUNT = ETH_AMOUNT * INITIAL_PRICE_NXR_PER_ETH;

  console.log(`\nLikidite : ${ethers.formatEther(ETH_AMOUNT)} ETH + ${ethers.formatEther(NXR_AMOUNT)} NXR`);
  console.log(`Başlangıç fiyatı: 1 NXR = ${(1 / Number(INITIAL_PRICE_NXR_PER_ETH) * 3000).toFixed(6)}$ (ETH=3000$ varsayımı)`);

  const token = await ethers.getContractAt("NexaraToken", TOKEN_ADDR);

  // Position Manager ABI (minimal)
  const PM_ABI = [
    "function createAndInitializePoolIfNecessary(address token0,address token1,uint24 fee,uint160 sqrtPriceX96) external payable returns(address pool)",
    "function mint((address token0,address token1,uint24 fee,int24 tickLower,int24 tickUpper,uint256 amount0Desired,uint256 amount1Desired,uint256 amount0Min,uint256 amount1Min,address recipient,uint256 deadline)) external payable returns(uint256 tokenId,uint128 liquidity,uint256 amount0,uint256 amount1)",
  ];

  const pm = new ethers.Contract(UNISWAP.positionManager, PM_ABI, deployer);

  // Token sıralaması (Uniswap: küçük adres önce)
  const [token0, token1, amount0, amount1] =
    TOKEN_ADDR.toLowerCase() < UNISWAP.WETH.toLowerCase()
      ? [TOKEN_ADDR, UNISWAP.WETH, NXR_AMOUNT, ETH_AMOUNT]
      : [UNISWAP.WETH, TOKEN_ADDR, ETH_AMOUNT, NXR_AMOUNT];

  // sqrtPriceX96 hesapla
  const price = token0 === TOKEN_ADDR
    ? (1n * (2n ** 96n)) / INITIAL_PRICE_NXR_PER_ETH
    : INITIAL_PRICE_NXR_PER_ETH * (2n ** 96n);
  const sqrtPriceX96 = BigInt(Math.floor(Math.sqrt(Number(price)) * (2 ** 48)));

  // NXR approve
  console.log("\n[1/3] NXR approve ediliyor...");
  await (await token.approve(UNISWAP.positionManager, NXR_AMOUNT)).wait();

  // Pool oluştur + başlat
  console.log("[2/3] Pool oluşturuluyor (%1 fee tier)...");
  await (await pm.createAndInitializePoolIfNecessary(
    token0, token1, 10000, sqrtPriceX96
  )).wait();

  // Likidite ekle
  console.log("[3/3] Likidite ekleniyor...");
  const deadline = Math.floor(Date.now() / 1000) + 1800;
  const tx = await pm.mint({
    token0, token1,
    fee: 10000,
    tickLower: -887200,
    tickUpper:  887200,
    amount0Desired: amount0,
    amount1Desired: amount1,
    amount0Min: 0n,
    amount1Min: 0n,
    recipient: deployer.address,
    deadline,
  }, { value: ETH_AMOUNT });

  const receipt = await tx.wait();
  console.log(`\nTx: ${receipt.hash}`);

  console.log("\n╔══════════════════════════════════════════════╗");
  console.log("║      UNİSWAP LİKİDİTE EKLENDİ!             ║");
  console.log("╠══════════════════════════════════════════════╣");
  console.log(`║ Token    : ${TOKEN_ADDR}`);
  console.log(`║ Çift     : ETH / NXR`);
  console.log(`║ Etherscan: https://etherscan.io/tx/${receipt.hash.slice(0,20)}...`);
  console.log("╠══════════════════════════════════════════════╣");
  console.log("║ SONRAKI ADIMLAR:                            ║");
  console.log("║ 1. DexScreener'da NXR kontrol et (5 dk)    ║");
  console.log("║ 2. CoinGecko başvurusu yap                  ║");
  console.log("║ 3. Topluluğu Uniswap linkiyle bilgilendir   ║");
  console.log(`║ 4. app.uniswap.org/tokens/ethereum/${TOKEN_ADDR.slice(0,10)}...`);
  console.log("╚══════════════════════════════════════════════╝");
}

main().catch(e => { console.error(e); process.exit(1); });

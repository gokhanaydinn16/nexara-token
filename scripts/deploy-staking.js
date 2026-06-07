const { ethers } = require("hardhat");

// Token zaten deploy edildi
const TOKEN_ADDRESS = "0xa14F7e4DE163Bc05297AF005B6cD44A770842187";

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying with:", deployer.address);
  console.log("Balance:", ethers.formatEther(await ethers.provider.getBalance(deployer.address)), "ETH\n");

  // 1. Deploy NexaraStaking
  console.log("Deploying NexaraStaking...");
  const Staking = await ethers.getContractFactory("NexaraStaking");
  const staking = await Staking.deploy(TOKEN_ADDRESS, deployer.address);
  await staking.waitForDeployment();
  const stakingAddress = await staking.getAddress();
  console.log("NexaraStaking deployed to:", stakingAddress);

  // 2. Link staking pool to token
  console.log("\nLinking staking pool to token...");
  const Token = await ethers.getContractAt("NexaraToken", TOKEN_ADDRESS);
  const tx = await Token.setStakingPool(stakingAddress);
  await tx.wait();
  console.log("Staking pool linked.");

  // 3. Fund staking contract with 5% of supply
  console.log("Funding staking contract with 5,000,000 NXR...");
  const fundTx = await Token.transfer(stakingAddress, ethers.parseEther("5000000"));
  await fundTx.wait();
  console.log("Funded!");

  console.log("\n╔══════════════════════════════════════════╗");
  console.log("║   NEXARA (NXR) — DEPLOY TAMAMLANDI!     ║");
  console.log("╠══════════════════════════════════════════╣");
  console.log("║ Token:  ", TOKEN_ADDRESS, "║");
  console.log("║ Staking:", stakingAddress, "║");
  console.log("╠══════════════════════════════════════════╣");
  console.log("║ Etherscan:                               ║");
  console.log("║ https://sepolia.etherscan.io/address/    ║");
  console.log("║", TOKEN_ADDRESS, "║");
  console.log("╚══════════════════════════════════════════╝");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});

const { ethers } = require("hardhat");

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying with:", deployer.address);
  console.log("Balance:", ethers.formatEther(await ethers.provider.getBalance(deployer.address)), "ETH\n");

  // 1. Deploy NexaraToken
  const Token = await ethers.getContractFactory("NexaraToken");
  const token = await Token.deploy(deployer.address);
  await token.waitForDeployment();
  const tokenAddress = await token.getAddress();
  console.log("NexaraToken (NXR) deployed to:", tokenAddress);

  // 2. Deploy NexaraStaking
  const Staking = await ethers.getContractFactory("NexaraStaking");
  const staking = await Staking.deploy(tokenAddress, deployer.address);
  await staking.waitForDeployment();
  const stakingAddress = await staking.getAddress();
  console.log("NexaraStaking deployed to:    ", stakingAddress);

  // 3. Link staking pool to token
  const tx = await token.setStakingPool(stakingAddress);
  await tx.wait();
  console.log("\nStaking pool linked to token.");

  // 4. Fund staking contract with 5% of supply for rewards
  const rewardAlloc = ethers.parseEther("5000000"); // 5,000,000 NXR
  const fundTx = await token.transfer(stakingAddress, rewardAlloc);
  await fundTx.wait();
  console.log("Staking contract funded with 5,000,000 NXR for rewards.");

  console.log("\n========================================");
  console.log("NEXARA (NXR) — Deployment Complete");
  console.log("========================================");
  console.log("Token:   ", tokenAddress);
  console.log("Staking: ", stakingAddress);
  console.log("\nVerify on Etherscan:");
  console.log(`npx hardhat verify --network sepolia ${tokenAddress} "${deployer.address}"`);
  console.log(`npx hardhat verify --network sepolia ${stakingAddress} "${tokenAddress}" "${deployer.address}"`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});

const { ethers } = require("hardhat");

const TOKEN_ADDRESS   = "0xa14F7e4DE163Bc05297AF005B6cD44A770842187";
const STAKING_ADDRESS = "0xa589014ee01E4F4f473ABD5587d304fA4879F5E4";

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying with:", deployer.address);
  console.log("Balance:", ethers.formatEther(await ethers.provider.getBalance(deployer.address)), "ETH\n");

  const token = await ethers.getContractAt("NexaraToken", TOKEN_ADDRESS);

  // 1. NexaraAccess deploy
  console.log("1/4 Deploying NexaraAccess...");
  const Access = await ethers.getContractFactory("NexaraAccess");
  const access = await Access.deploy(TOKEN_ADDRESS, deployer.address);
  await access.waitForDeployment();
  const accessAddress = await access.getAddress();
  console.log("    NexaraAccess:", accessAddress);

  // 2. NexaraTreasury deploy
  console.log("2/4 Deploying NexaraTreasury...");
  const Treasury = await ethers.getContractFactory("NexaraTreasury");
  const treasury = await Treasury.deploy(TOKEN_ADDRESS, deployer.address);
  await treasury.waitForDeployment();
  const treasuryAddress = await treasury.getAddress();
  console.log("    NexaraTreasury:", treasuryAddress);

  // 3. Access → Treasury bağla
  console.log("3/4 Linking Treasury to Access...");
  await (await access.setTreasury(treasuryAddress)).wait();
  console.log("    Linked.");

  // 4. Exclude from fees
  console.log("4/4 Excluding contracts from fees...");
  await (await token.setExcludedFromFees(accessAddress, true)).wait();
  await (await token.setExcludedFromFees(treasuryAddress, true)).wait();
  await (await token.setExcludedFromMaxWallet(accessAddress, true)).wait();
  await (await token.setExcludedFromMaxWallet(treasuryAddress, true)).wait();
  console.log("    Done.\n");

  console.log("╔══════════════════════════════════════════════════════════════╗");
  console.log("║          NEXARA EKOSİSTEM — TAM DEPLOY TAMAMLANDI           ║");
  console.log("╠══════════════════════════════════════════════════════════════╣");
  console.log("║ Token    :", TOKEN_ADDRESS);
  console.log("║ Staking  :", STAKING_ADDRESS);
  console.log("║ Access   :", accessAddress);
  console.log("║ Treasury :", treasuryAddress);
  console.log("╠══════════════════════════════════════════════════════════════╣");
  console.log("║ Etherscan (Token):                                           ║");
  console.log("║ https://sepolia.etherscan.io/address/" + TOKEN_ADDRESS);
  console.log("╚══════════════════════════════════════════════════════════════╝");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});

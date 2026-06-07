const { ethers } = require("hardhat");

const TOKEN_ADDRESS = "0xa14F7e4DE163Bc05297AF005B6cD44A770842187";

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying NexaraPay with:", deployer.address);
  console.log("Balance:", ethers.formatEther(await ethers.provider.getBalance(deployer.address)), "ETH\n");

  // treasury = deployer (ödemeler buraya gelir), nxrToken = NXR
  const Pay = await ethers.getContractFactory("NexaraPay");
  const pay = await Pay.deploy(deployer.address, TOKEN_ADDRESS, deployer.address);
  await pay.waitForDeployment();
  const payAddress = await pay.getAddress();
  console.log("NexaraPay deployed to:", payAddress);

  console.log("\n╔══════════════════════════════════════════════╗");
  console.log("║          NEXARA PAY — DEPLOY TAMAM          ║");
  console.log("╠══════════════════════════════════════════════╣");
  console.log("║ Pay Gateway:", payAddress);
  console.log("║ Treasury   :", deployer.address);
  console.log("║ NXR Token  :", TOKEN_ADDRESS);
  console.log("╠══════════════════════════════════════════════╣");
  console.log("║ Kabul: ETH + NXR (USDT sonra eklenebilir)   ║");
  console.log("║ NXR ile ödemede %5 indirim aktif            ║");
  console.log("╚══════════════════════════════════════════════╝");
  console.log("\nEtherscan:");
  console.log(`https://sepolia.etherscan.io/address/${payAddress}`);
}

main().catch(e => { console.error(e); process.exit(1); });

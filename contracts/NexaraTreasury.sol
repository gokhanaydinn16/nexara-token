// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/**
 * NEXARA Treasury — Gelir Paylaşım Sistemi
 *
 * Bot abonelik ücretleri bu kontratta birikir.
 * NXR stake edenler oranlarına göre pay alır.
 * Her hafta owner "distribute()" çağırarak dağıtım yapar.
 */
contract NexaraTreasury is Ownable, ReentrancyGuard {
    IERC20 public immutable nexara;

    // Birikmiş dağıtılmamış ödüller
    uint256 public pendingRewards;

    // Kullanıcı başına ödül takibi
    mapping(address => uint256) public rewardDebt;
    mapping(address => uint256) public claimable;

    // Basit staker listesi (off-chain indexleme için)
    event RevenueReceived(uint256 amount);
    event RewardsDistributed(uint256 totalAmount, uint256 stakerCount);
    event RewardClaimed(address indexed user, uint256 amount);

    constructor(address _nexara, address initialOwner) Ownable(initialOwner) {
        nexara = IERC20(_nexara);
    }

    // ── Gelir Girişi (owner çağırır — bot gelirlerini buraya gönderir) ───────

    function receiveRevenue(uint256 amount) external onlyOwner {
        nexara.transferFrom(msg.sender, address(this), amount);
        pendingRewards += amount;
        emit RevenueReceived(amount);
    }

    // ── Dağıtım (owner haftalık çağırır) ─────────────────────────────────────

    function distribute(
        address[] calldata stakers,
        uint256[] calldata shares  // toplam 10000 = %100
    ) external onlyOwner {
        require(stakers.length == shares.length, "Length mismatch");
        require(pendingRewards > 0, "Nothing to distribute");

        uint256 total = pendingRewards;
        pendingRewards = 0;

        uint256 shareSum;
        for (uint256 i = 0; i < shares.length; i++) {
            shareSum += shares[i];
        }
        require(shareSum <= 10000, "Shares exceed 100%");

        for (uint256 i = 0; i < stakers.length; i++) {
            uint256 reward = (total * shares[i]) / 10000;
            claimable[stakers[i]] += reward;
        }

        emit RewardsDistributed(total, stakers.length);
    }

    // ── Kullanıcı ödül çekme ──────────────────────────────────────────────────

    function claim() external nonReentrant {
        uint256 amount = claimable[msg.sender];
        require(amount > 0, "Nothing to claim");
        claimable[msg.sender] = 0;
        nexara.transfer(msg.sender, amount);
        emit RewardClaimed(msg.sender, amount);
    }

    // ── Views ─────────────────────────────────────────────────────────────────

    function pendingClaim(address user) external view returns (uint256) {
        return claimable[user];
    }

    function treasuryBalance() external view returns (uint256) {
        return nexara.balanceOf(address(this));
    }
}

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/**
 * NEXARA Access — Superajan Bot Abonelik Sistemi
 *
 * Tier sistemi:
 *   Bronze  → 10,000 NXR stake  → Temel sinyaller
 *   Silver  → 50,000 NXR stake  → Gelişmiş sinyaller + whale takip
 *   Gold    → 200,000 NXR stake → Tüm özellikler + öncelikli erişim
 *
 * Superajan botu bu sözleşmeyi okuyarak kullanıcı tier'ını doğrular.
 */
contract NexaraAccess is Ownable, ReentrancyGuard {
    IERC20 public immutable nexara;

    uint256 public constant BRONZE_THRESHOLD = 10_000  * 10**18;
    uint256 public constant SILVER_THRESHOLD = 50_000  * 10**18;
    uint256 public constant GOLD_THRESHOLD   = 200_000 * 10**18;

    uint256 public constant LOCK_PERIOD = 30 days;

    enum Tier { None, Bronze, Silver, Gold }

    struct Subscription {
        uint256 stakedAmount;
        uint256 stakedAt;
        uint256 lastClaimed;
    }

    mapping(address => Subscription) public subscriptions;
    uint256 public totalStaked;

    // Revenue treasury address (NXRTreasury contract)
    address public treasury;

    event Subscribed(address indexed user, uint256 amount, Tier tier);
    event Unsubscribed(address indexed user, uint256 amount);
    event TierUpgraded(address indexed user, Tier oldTier, Tier newTier);

    constructor(address _nexara, address initialOwner) Ownable(initialOwner) {
        nexara = IERC20(_nexara);
    }

    // ── Stake / Unstake ──────────────────────────────────────────────────────

    function subscribe(uint256 amount) external nonReentrant {
        require(amount >= BRONZE_THRESHOLD, "Access: minimum 10,000 NXR");

        Subscription storage sub = subscriptions[msg.sender];
        Tier oldTier = getTier(msg.sender);

        nexara.transferFrom(msg.sender, address(this), amount);
        sub.stakedAmount += amount;
        sub.stakedAt      = block.timestamp;
        sub.lastClaimed   = block.timestamp;
        totalStaked      += amount;

        Tier newTier = getTier(msg.sender);
        if (oldTier != newTier) emit TierUpgraded(msg.sender, oldTier, newTier);
        emit Subscribed(msg.sender, amount, newTier);
    }

    function unsubscribe() external nonReentrant {
        Subscription storage sub = subscriptions[msg.sender];
        require(sub.stakedAmount > 0, "Access: nothing staked");
        require(
            block.timestamp >= sub.stakedAt + LOCK_PERIOD,
            "Access: lock period active"
        );

        uint256 amount = sub.stakedAmount;
        totalStaked -= amount;
        delete subscriptions[msg.sender];

        nexara.transfer(msg.sender, amount);
        emit Unsubscribed(msg.sender, amount);
    }

    // ── Views ─────────────────────────────────────────────────────────────────

    function getTier(address user) public view returns (Tier) {
        uint256 staked = subscriptions[user].stakedAmount;
        if (staked >= GOLD_THRESHOLD)   return Tier.Gold;
        if (staked >= SILVER_THRESHOLD) return Tier.Silver;
        if (staked >= BRONZE_THRESHOLD) return Tier.Bronze;
        return Tier.None;
    }

    function hasBotAccess(address user) external view returns (bool) {
        return getTier(user) != Tier.None;
    }

    function getTierName(address user) external view returns (string memory) {
        Tier t = getTier(user);
        if (t == Tier.Gold)   return "Gold";
        if (t == Tier.Silver) return "Silver";
        if (t == Tier.Bronze) return "Bronze";
        return "None";
    }

    function unlockTimeRemaining(address user) external view returns (uint256) {
        Subscription memory sub = subscriptions[user];
        if (sub.stakedAmount == 0) return 0;
        uint256 unlock = sub.stakedAt + LOCK_PERIOD;
        return block.timestamp >= unlock ? 0 : unlock - block.timestamp;
    }

    // ── Admin ─────────────────────────────────────────────────────────────────

    function setTreasury(address _treasury) external onlyOwner {
        treasury = _treasury;
    }
}

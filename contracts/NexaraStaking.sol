// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/**
 * NEXARA Staking
 * - 30-day lock period
 * - 12% APY (paid from staking pool funded by transfer fees)
 * - Compound-friendly: claim anytime, unstake after lock
 */
contract NexaraStaking is Ownable, ReentrancyGuard {
    IERC20 public immutable nexara;

    uint256 public constant LOCK_PERIOD       = 30 days;
    uint256 public constant APY_RATE          = 1200;      // 12%
    uint256 public constant RATE_DENOMINATOR  = 10_000;
    uint256 public constant SECONDS_PER_YEAR  = 365 days;

    struct Stake {
        uint256 amount;
        uint256 stakedAt;
        uint256 lastClaimed;
    }

    mapping(address => Stake) public stakes;
    uint256 public totalStaked;

    event Staked(address indexed user, uint256 amount);
    event Unstaked(address indexed user, uint256 amount);
    event RewardClaimed(address indexed user, uint256 reward);

    constructor(address _nexara, address initialOwner) Ownable(initialOwner) {
        nexara = IERC20(_nexara);
    }

    // ── User actions ─────────────────────────────────────────────────────────

    function stake(uint256 amount) external nonReentrant {
        require(amount > 0, "Staking: amount must be > 0");

        if (stakes[msg.sender].amount > 0) {
            _claimReward(msg.sender);
        }

        nexara.transferFrom(msg.sender, address(this), amount);

        stakes[msg.sender].amount      += amount;
        stakes[msg.sender].stakedAt     = block.timestamp;
        stakes[msg.sender].lastClaimed  = block.timestamp;
        totalStaked += amount;

        emit Staked(msg.sender, amount);
    }

    function unstake() external nonReentrant {
        Stake memory s = stakes[msg.sender];
        require(s.amount > 0, "Staking: nothing staked");
        require(
            block.timestamp >= s.stakedAt + LOCK_PERIOD,
            "Staking: lock period active"
        );

        _claimReward(msg.sender);

        uint256 amount = stakes[msg.sender].amount;
        totalStaked -= amount;
        delete stakes[msg.sender];

        nexara.transfer(msg.sender, amount);
        emit Unstaked(msg.sender, amount);
    }

    function claimReward() external nonReentrant {
        require(stakes[msg.sender].amount > 0, "Staking: nothing staked");
        _claimReward(msg.sender);
    }

    // ── Views ─────────────────────────────────────────────────────────────────

    function pendingReward(address user) public view returns (uint256) {
        Stake memory s = stakes[user];
        if (s.amount == 0) return 0;
        uint256 elapsed = block.timestamp - s.lastClaimed;
        return (s.amount * APY_RATE * elapsed) / (RATE_DENOMINATOR * SECONDS_PER_YEAR);
    }

    function unlockTimeRemaining(address user) external view returns (uint256) {
        Stake memory s = stakes[user];
        if (s.amount == 0) return 0;
        uint256 unlock = s.stakedAt + LOCK_PERIOD;
        return block.timestamp >= unlock ? 0 : unlock - block.timestamp;
    }

    // ── Internal ──────────────────────────────────────────────────────────────

    function _claimReward(address user) internal {
        uint256 reward = pendingReward(user);
        if (reward == 0) return;
        stakes[user].lastClaimed = block.timestamp;
        nexara.transfer(user, reward);
        emit RewardClaimed(user, reward);
    }
}

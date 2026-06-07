// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * NEXARA (NXR)
 * - 100,000,000 total supply
 * - 2% burn on every transfer (deflationary)
 * - 1% to staking pool on every transfer
 * - Anti-whale: max 1% of supply per wallet
 * - Fee-excluded addresses (DEX, staking contract, owner)
 */
contract NexaraToken is ERC20, Ownable {
    uint256 public constant MAX_SUPPLY       = 100_000_000 * 10 ** 18;
    uint256 public constant BURN_FEE         = 200;   // 2%
    uint256 public constant STAKING_FEE      = 100;   // 1%
    uint256 public constant FEE_DENOMINATOR  = 10_000;
    uint256 public constant MAX_WALLET       = MAX_SUPPLY / 100; // 1% = 1,000,000 NXR

    address public constant DEAD = 0x000000000000000000000000000000000000dEaD;
    address public stakingPool;

    mapping(address => bool) public isExcludedFromFees;
    mapping(address => bool) public isExcludedFromMaxWallet;

    event StakingPoolSet(address indexed pool);
    event FeeExclusionSet(address indexed account, bool excluded);

    constructor(address initialOwner) ERC20("Nexara", "NXR") Ownable(initialOwner) {
        _mint(initialOwner, MAX_SUPPLY);

        isExcludedFromFees[initialOwner]  = true;
        isExcludedFromFees[address(this)] = true;

        isExcludedFromMaxWallet[initialOwner] = true;
        isExcludedFromMaxWallet[DEAD]         = true;
    }

    // ── Admin ────────────────────────────────────────────────────────────────

    function setStakingPool(address _pool) external onlyOwner {
        require(_pool != address(0), "NXR: zero address");
        stakingPool = _pool;
        isExcludedFromFees[_pool]      = true;
        isExcludedFromMaxWallet[_pool] = true;
        emit StakingPoolSet(_pool);
    }

    function setExcludedFromFees(address account, bool excluded) external onlyOwner {
        isExcludedFromFees[account] = excluded;
        emit FeeExclusionSet(account, excluded);
    }

    function setExcludedFromMaxWallet(address account, bool excluded) external onlyOwner {
        isExcludedFromMaxWallet[account] = excluded;
    }

    // ── Transfer logic ───────────────────────────────────────────────────────

    function _update(address from, address to, uint256 amount) internal override {
        // Minting, burning, or excluded addresses — no fees
        if (from == address(0) || isExcludedFromFees[from] || isExcludedFromFees[to]) {
            super._update(from, to, amount);
            return;
        }

        uint256 burnAmount    = (amount * BURN_FEE)    / FEE_DENOMINATOR;
        uint256 stakingAmount = (stakingPool != address(0))
            ? (amount * STAKING_FEE) / FEE_DENOMINATOR
            : 0;
        uint256 transferAmount = amount - burnAmount - stakingAmount;

        // Anti-whale
        if (!isExcludedFromMaxWallet[to]) {
            require(
                balanceOf(to) + transferAmount <= MAX_WALLET,
                "NXR: exceeds max wallet"
            );
        }

        if (burnAmount > 0)    super._update(from, DEAD,        burnAmount);
        if (stakingAmount > 0) super._update(from, stakingPool, stakingAmount);
        super._update(from, to, transferAmount);
    }

    // ── Views ────────────────────────────────────────────────────────────────

    function circulatingSupply() external view returns (uint256) {
        return totalSupply() - balanceOf(DEAD);
    }

    function totalBurned() external view returns (uint256) {
        return balanceOf(DEAD);
    }
}

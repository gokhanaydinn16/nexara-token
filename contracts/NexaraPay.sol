// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/**
 * NEXARA PAY — Crypto Payment Gateway
 *
 * Lisans GEREKMEZ: Kendi mal/hizmetin için doğrudan kripto kabul edersin.
 * Aracı yok, banka yok — para doğrudan sana gelir.
 *
 * Desteklenen ödemeler:
 *   - ETH (native)
 *   - NXR (kendi token'ın)
 *   - USDT / USDC veya whitelist'teki herhangi bir ERC-20
 *
 * Her ödeme bir orderId ile kaydedilir → off-chain sipariş takibi yapılır.
 * NXR ile ödeyenlere otomatik indirim uygulanabilir (incentive).
 */
contract NexaraPay is Ownable, ReentrancyGuard {
    using SafeERC20 for IERC20;

    // Ödeme alıcısı (merchant treasury)
    address public treasury;

    // Kabul edilen ERC-20 tokenlar (USDT, USDC, NXR...)
    mapping(address => bool) public acceptedTokens;

    // NXR token adresi (indirim için)
    address public nxrToken;
    // NXR ile ödemede indirim (basis points, 500 = %5)
    uint256 public nxrDiscountBps = 500;
    uint256 public constant BPS = 10_000;

    // orderId => ödendi mi?
    mapping(bytes32 => bool) public orderPaid;

    struct Payment {
        address payer;
        address token;      // address(0) = ETH
        uint256 amount;
        uint256 timestamp;
    }
    mapping(bytes32 => Payment) public payments;

    event PaymentReceived(
        bytes32 indexed orderId,
        address indexed payer,
        address indexed token,
        uint256 amount,
        uint256 timestamp
    );
    event TreasuryUpdated(address treasury);
    event TokenAccepted(address token, bool accepted);
    event Withdrawn(address token, uint256 amount, address to);

    constructor(address _treasury, address _nxrToken, address initialOwner)
        Ownable(initialOwner)
    {
        require(_treasury != address(0), "Pay: zero treasury");
        treasury = _treasury;
        nxrToken = _nxrToken;
        if (_nxrToken != address(0)) {
            acceptedTokens[_nxrToken] = true;
        }
    }

    // ── Ödeme: ETH ile ────────────────────────────────────────────────────────

    function payWithETH(bytes32 orderId) external payable nonReentrant {
        require(msg.value > 0, "Pay: zero amount");
        require(!orderPaid[orderId], "Pay: order already paid");

        orderPaid[orderId] = true;
        payments[orderId] = Payment(msg.sender, address(0), msg.value, block.timestamp);

        (bool ok, ) = treasury.call{value: msg.value}("");
        require(ok, "Pay: ETH transfer failed");

        emit PaymentReceived(orderId, msg.sender, address(0), msg.value, block.timestamp);
    }

    // ── Ödeme: ERC-20 (NXR / USDT / USDC) ile ─────────────────────────────────

    function payWithToken(bytes32 orderId, address token, uint256 amount)
        external
        nonReentrant
    {
        require(acceptedTokens[token], "Pay: token not accepted");
        require(amount > 0, "Pay: zero amount");
        require(!orderPaid[orderId], "Pay: order already paid");

        orderPaid[orderId] = true;
        payments[orderId] = Payment(msg.sender, token, amount, block.timestamp);

        // NXR ile ödeyene indirim uygulanır → daha az token alınır
        uint256 finalAmount = amount;
        if (token == nxrToken && nxrDiscountBps > 0) {
            finalAmount = amount - (amount * nxrDiscountBps) / BPS;
        }

        IERC20(token).safeTransferFrom(msg.sender, treasury, finalAmount);

        emit PaymentReceived(orderId, msg.sender, token, finalAmount, block.timestamp);
    }

    // ── Views ─────────────────────────────────────────────────────────────────

    function isOrderPaid(bytes32 orderId) external view returns (bool) {
        return orderPaid[orderId];
    }

    function getPayment(bytes32 orderId) external view returns (Payment memory) {
        return payments[orderId];
    }

    /// orderId üretmek için yardımcı (off-chain de üretilebilir)
    function makeOrderId(string calldata ref) external pure returns (bytes32) {
        return keccak256(abi.encodePacked(ref));
    }

    // ── Admin ─────────────────────────────────────────────────────────────────

    function setTreasury(address _treasury) external onlyOwner {
        require(_treasury != address(0), "Pay: zero treasury");
        treasury = _treasury;
        emit TreasuryUpdated(_treasury);
    }

    function setAcceptedToken(address token, bool accepted) external onlyOwner {
        acceptedTokens[token] = accepted;
        emit TokenAccepted(token, accepted);
    }

    function setNxrDiscount(uint256 bps) external onlyOwner {
        require(bps <= 5000, "Pay: max 50%");
        nxrDiscountBps = bps;
    }

    /// Acil durumda kontrata yanlışlıkla kalan fonları çekme
    function rescue(address token, uint256 amount) external onlyOwner {
        if (token == address(0)) {
            (bool ok, ) = treasury.call{value: amount}("");
            require(ok, "Pay: rescue ETH failed");
        } else {
            IERC20(token).safeTransfer(treasury, amount);
        }
        emit Withdrawn(token, amount, treasury);
    }
}

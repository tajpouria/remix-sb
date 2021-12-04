// SPDX-License-Identifier: MIT

pragma solidity 0.8;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Lottery is VRFConsumerBase, Ownable {
    event RequestedRandomness(bytes32 requestId);

    uint256 public usdThreshold = 50 * 10**18;
    AggregatorV3Interface private priceFeedInterface;
    address payable[] public players;
    address payable public recentWinner;
    enum LotteryState {
        Opened,
        CalculatingWinner,
        Closed
    }
    LotteryState public lotteryState;

    bytes32 internal keyHash;
    uint256 internal fee = 0.1 * 10**18;

    constructor(
        address _priceFeed,
        address _vrfCoordinator,
        address _link,
        bytes32 _keyHash
    ) VRFConsumerBase(_vrfCoordinator, _link) {
        priceFeedInterface = AggregatorV3Interface(_priceFeed);
        lotteryState = LotteryState.Closed;
        keyHash = _keyHash;
    }

    function getEntranceFee() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeedInterface.latestRoundData();
        uint256 latestUsdPrice = uint256(answer) * 10 * 10**10;

        return (usdThreshold * 10**18) / latestUsdPrice;
    }

    function enterLottery() external payable {
        require(
            lotteryState == LotteryState.Opened,
            "Lottery is not opened yet"
        );
        require(
            msg.value >= getEntranceFee(),
            "Staked amount must be grater than entrance fee"
        );

        players.push(payable(msg.sender));
    }

    function openLottery() external onlyOwner {
        require(
            lotteryState == LotteryState.Closed,
            "Lottery state is not closed yet"
        );
        lotteryState = LotteryState.Opened;
    }

    function closeLottery() external onlyOwner {
        require(
            lotteryState == LotteryState.Opened,
            "Lottery is not opened yet"
        );

        bytes32 requestId = requestRandomness(keyHash, fee);
        emit RequestedRandomness(requestId);

        lotteryState = LotteryState.CalculatingWinner;
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        _requestId;

        require(
            lotteryState == LotteryState.CalculatingWinner,
            "Lottery is must be in calculating winner state"
        );

        address payable winnerPlayer = players[_randomness % players.length];
        winnerPlayer.transfer(address(this).balance);
        recentWinner = winnerPlayer;

        players = new address payable[](0);
        lotteryState = LotteryState.Closed;
    }
}

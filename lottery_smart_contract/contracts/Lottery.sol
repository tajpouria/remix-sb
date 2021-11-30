// SPDX-License-Identifier: MIT

pragma solidity 0.8;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract Lottery {
    uint256 public usdThreshold = 50 * 10**18;

    AggregatorV3Interface internal priceFeedInterface;

    constructor(address priceFeedAddr) {
        priceFeedInterface = AggregatorV3Interface(priceFeedAddr);
    }

    function getEntranceFee() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeedInterface.latestRoundData();
        uint256 latestUsdPrice = uint256(answer) * 10 * 10**10;

        return (usdThreshold * 10**18) / latestUsdPrice;
    }
}

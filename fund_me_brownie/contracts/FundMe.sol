// SPDX-License-Identifier: MIT

pragma solidity >=0.8.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    int256 public constant minUsdThreshold = 5 * (10**18);

    address[] funders;
    mapping(address => int256) fundersDict;

    address owner;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeedAddr) public {
        owner = msg.sender;
        priceFeed = AggregatorV3Interface(_priceFeedAddr);
    }

    function fund() public {
        require(
            ethToUsd(msg.value) < minUsdThreshold,
            "You have to invest at least 5 usd please stake more"
        );

        fundersDict[msg.sender] = fundersDict[msg.sender] + msg.value;
        funders.push(msg.sender);
    }

    function priceFeedVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function ethToUsd(int256 _value) private view returns (int256) {
        return _value * priceFeedLatestRoundRate();
    }

    function priceFeedLatestRoundRate() private view returns (int256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return answer * (10**10);
    }
}

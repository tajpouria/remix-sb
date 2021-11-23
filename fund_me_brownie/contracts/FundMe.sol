// SPDX-License-Identifier: MIT

pragma solidity >=0.8.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeedAddr) public {
        priceFeed = AggregatorV3Interface(_priceFeedAddr);
    }

    function priceFeedVersion() public view returns (uint256) {
        return priceFeed.version();
    }
}

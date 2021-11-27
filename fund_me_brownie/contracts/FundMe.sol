// SPDX-License-Identifier: MIT

pragma solidity >=0.8.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    uint256 public constant minUsdThreshold = 5 * (10**18);

    address[] funders;
    mapping(address => uint256) fundersDict;

    address owner;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeedAddr) {
        owner = msg.sender;
        priceFeed = AggregatorV3Interface(_priceFeedAddr);
    }

    modifier onlyOwner() {
        require(
            msg.sender == owner,
            "Only contract's owner can do the withdrawal"
        );
        _;
    }

    function fund() external payable {
        require(
            ethToUsd(msg.value) > minUsdThreshold,
            "You have to invest at least 5 usd please stake more"
        );

        fundersDict[msg.sender] = fundersDict[msg.sender] + msg.value;
        funders.push(msg.sender);
    }

    function withdraw() external payable onlyOwner {
        payable(msg.sender).transfer(address(this).balance);

        for (uint256 i = 0; i < funders.length; i++) {
            address f = funders[i];
            fundersDict[f] = 0;
        }
        funders = new address[](0);
    }

    function priceFeedVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function ethToUsd(uint256 _value) private view returns (uint256) {
        return _value * priceFeedLatestRoundRate();
    }

    function priceFeedLatestRoundRate() private view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer) * (10**10);
    }
}

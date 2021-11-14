// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

contract FundMe {
    address public owner;

    address[] public funders;
    mapping(address => uint256) public addressToFundMap;

    address private constant priceFeedAddr =
        0x8A753747A1Fa494EC906cE90E9f37563A8AF630e;
    uint256 public leastAcceptableStakeInUsd = 50 * 10**18;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(
            msg.sender == owner,
            "Only contract owner can trigger this method!"
        );
        _;
    }

    function fund() public payable {
        require(
            ethToUsdConversion(msg.value) >= leastAcceptableStakeInUsd,
            string(
                abi.encodePacked(
                    "The least acceptable stake amount is equivalent to ",
                    Strings.toString(leastAcceptableStakeInUsd / 10**18),
                    " USD. please stake more!"
                )
            )
        );

        funders.push(msg.sender);
        addressToFundMap[msg.sender] = addressToFundMap[msg.sender] + msg.value;
    }

    function withdraw() public onlyOwner {
        payable(msg.sender).transfer(address(this).balance);

        for (uint256 i; i < funders.length; i++) {
            address addr = funders[i];
            addressToFundMap[addr] = 0;
        }
        funders = new address[](0);
    }

    function getPriceFeedVersion() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(priceFeedAddr);
        return priceFeed.version();
    }

    function getPriceFeedDecimals() public view returns (uint8) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(priceFeedAddr);
        return priceFeed.decimals();
    }

    function getPriceFeedLatestRoundDate() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(priceFeedAddr);
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * (10**10));
    }

    function ethToUsdConversion(uint256 _ethAmout)
        public
        view
        returns (uint256)
    {
        return (getPriceFeedLatestRoundDate() * _ethAmout) / 10**18;
    }
}

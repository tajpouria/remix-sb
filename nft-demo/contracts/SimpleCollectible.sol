// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract SimpleCollectible is ERC721URIStorage {
    using Counters for Counters.Counter;

    Counters.Counter public latestTokenId;

    constructor() ERC721("SimpleCollectible", "SCB") {}

    function createCollectible(string memory tokenURI)
        public
        returns (uint256 tokenId)
    {
        latestTokenId.increment();
        uint256 newTokenId = latestTokenId.current();

        _safeMint(msg.sender, newTokenId);
        _setTokenURI(newTokenId, tokenURI);

        return newTokenId;
    }
}

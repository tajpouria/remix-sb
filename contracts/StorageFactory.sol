// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;

import "./SimpleStorage.sol";

contract StorageFactory {
    SimpleStorage[] public storageStore;

    function createSimpleStorage() public {
        storageStore.push(new SimpleStorage());
    }

    function store(
        uint256 _simpleStorageIndex,
        string memory _personName,
        int256 _personFavoriteNumber
    ) public {
        SimpleStorage(address(storageStore[_simpleStorageIndex])).addPerson(
            _personName,
            _personFavoriteNumber
        );
    }

    function get(uint256 _simpleStorageIndex, string memory _personName)
        public
        view
        returns (int256)
    {
        return
            SimpleStorage(address(storageStore[_simpleStorageIndex])).retrieve(
                _personName
            );
    }
}

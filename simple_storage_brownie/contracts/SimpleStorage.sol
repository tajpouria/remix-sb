// SPDX-License-Identifier: MIT
pragma solidity 0.8.10;

contract SimpleStorage {
    int256 public value;

    function store(int256 _value) public {
        value = _value;
    }

    function retrieve() public view returns (int256) {
        return value;
    }
}

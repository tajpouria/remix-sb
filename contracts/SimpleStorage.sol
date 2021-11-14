// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0;

contract SimpleStorage {
    struct Person {
        string name;
        int256 favoriteNumber;
    }

    Person[] public people;
    mapping(string => int256) public peopleFavoriteNumber;

    function addPerson(string memory _name, int256 _favoriteNumber) public {
        people.push(Person(_name, _favoriteNumber));
        peopleFavoriteNumber[_name] = _favoriteNumber;
    }

    function retrieve(string memory _name) public view returns (int256) {
        return peopleFavoriteNumber[_name];
    }
}

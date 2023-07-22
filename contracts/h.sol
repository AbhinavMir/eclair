// SPDX-License-Identifier: MIT
pragma solidity ^0.8.6;

contract HelloWorld {
    string public greet = "Hello, World!";

    function sayHello() public view returns (string memory) {
        return greet;
    }
}

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PayeeContract {
    address[] private payees;
    address private owner;

    constructor(address[] memory initialPayees) {
        owner = msg.sender;
        payees = initialPayees;
    }

    function getAllPayees() public view returns (address[] memory) {
        return payees;
    }

    function addPayee(address newPayee) public {
        require(msg.sender == owner, "Only the owner can add payees");
        payees.push(newPayee);
    }

    function removePayee(address payee) public {
        require(msg.sender == owner, "Only the owner can remove payees");
        for (uint256 i = 0; i < payees.length; i++) {
            if (payees[i] == payee) {
                payees[i] = payees[payees.length - 1];
                payees.pop();
                break;
            }
        }
    }

    function payableFunction() public payable {
        // Perform some operations with the received Ether
    }

    function addBalance(uint amount) public payable {
        require(msg.value == amount, "Amount does not match value sent");
        
    }

    function _sendEth(uint _amount, address _to) internal 
    {
        (bool success, bytes memory data) = _to.call{value: _amount}("");
        require(success, "Failed to send Ether");
    }

    function sendEth(uint amount, address[] memory to) public onlyOwner() {
        uint amountPerPayee = amount / to.length;
        for (uint256 i = 0; i < to.length; i++) {
            _sendEth(amountPerPayee, to[i]);
        }
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function");
        _;
    }

    modifier hasEnoughEther(uint amount)
    {
        require(address(this).balance >= amount, "Not enough Ether in contract");
        _;
    }

    fallback() external payable {
        // Fallback function logic
    }

    receive() external payable {
        // Receive function logic
    }
}

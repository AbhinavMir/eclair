// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract test_this {

    address[] private students;
    function addNewStudents(address[] memory newStudents) payable public returns (address[] memory, string memory){
        for (uint256 i = 0; i < newStudents.length; i++) {
            students.push(newStudents[i]);
        }
        return (students, "Students added successfully");
    }
}

// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import ".deps/npm/@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract LuckyDraw is VRFConsumerBase {
    bytes32 internal keyHash;
    uint256 internal fee;
    address public owner;
    uint256 public numWinners;
    address[] public candidates;
    address[] public winners;
    bool public drawClosed;
    uint256 public linkBalance;
    address private vrfCoordinator;

    constructor(address _vrfCoordinator, address _linkToken, bytes32 _keyHash, uint256 _fee) VRFConsumerBase(_vrfCoordinator, _linkToken) {
        keyHash = _keyHash;
        fee = _fee;
        owner = msg.sender;
        vrfCoordinator = _vrfCoordinator;
    }

    function withdrawLink() public {
        require(msg.sender == owner, "Only owner can withdraw LINK");
        require(LINK.transfer(msg.sender, LINK.balanceOf(address(this))), "Unable to transfer");
        linkBalance = LINK.balanceOf(address(this));
    }

    function setCandidates(address[] memory _candidates) public {
        require(msg.sender == owner, "Only owner can set candidates");
        require(!drawClosed, "Draw has already been closed");
        candidates = _candidates;
    }

    function getCandidates() public view returns (address[] memory) {
        return candidates;
    }

    function setNumWinners(uint256 _numWinners) public {
        require(msg.sender == owner, "Only owner can set number of winners");
        require(!drawClosed, "Draw has already been closed");
        numWinners = _numWinners;
    }

    function closeDraw() public {
        require(msg.sender == owner, "Only owner can close draw");
        require(candidates.length >= numWinners, "Not enough candidates to select winners");
        drawClosed = true;
    }

    function getRandomNumber() public returns (bytes32 requestId) {
        require(msg.sender == owner, "Only owner can request random number");
        require(drawClosed, "Draw is still open");
        require(LINK.balanceOf(address(this)) >= fee, "Not enough LINK to fulfill request");
        return requestRandomness(keyHash, fee);
    }

    function fulfillRandomness(bytes32 /* requestId */, uint256 randomness) internal override {
        require(msg.sender == vrfCoordinator, "Only VRF coordinator can fulfill randomness");
        require(winners.length == 0, "Winners have already been selected");
        for (uint i = 0; i < numWinners; i++) {
            uint256 index = uint256(keccak256(abi.encode(randomness, i))) % candidates.length;
            address winner = candidates[index];
            winners.push(winner);
            candidates[index] = candidates[candidates.length - 1];
            candidates.pop();
        }
    }
}
pragma abicoder v2;
import "main.sol";

contract TestLuckyDraw {
    LuckyDraw luckyDraw = new LuckyDraw("a","a","a","a");

    function testSetCandidates() public {
        address[] memory candidates = new address[](3);
        candidates[0] = 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4;
        candidates[1] = 0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2;
        candidates[2] = 0x4B20993Bc481177ec7E8f571ceCaE8A9e22C02db;

        luckyDraw.setCandidates(candidates);
        
        address[] memory actualCandidates = luckyDraw.getCandidates();
        assert(actualCandidates.length == 3);
        assert(actualCandidates[0] == candidates[0]);
        assert(actualCandidates[1] == candidates[1]);
        assert(actualCandidates[2] == candidates[2]);
    }

    function testGetRandomNumber() public {
        address[] memory candidates = new address[](3);
        candidates[0] = 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4;
        candidates[1] = 0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2;
        candidates[2] = 0x4B20993Bc481177ec7E8f571ceCaE8A9e22C02db;

        luckyDraw.setCandidates(candidates);

        bytes32 requestId = luckyDraw.getRandomNumber();
        assert(requestId != 0);
    }
}
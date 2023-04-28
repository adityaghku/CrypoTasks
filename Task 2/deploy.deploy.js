module.exports = function(deployer) {
  const vrfCoordinator = "0x8103B0A8A00be2DDC778e6e7eaa21791Cd364625"; // Replace with your own address
  const linkToken = "0x779877A7B0D9E8603169DdbD7836e478b4624789"; // Replace with your own address
  const keyHash = "0x474e34a077df58807dbe9c96d3c009b23b3c6d0cce433e59bbf5b34f823bc56c"; // Replace with your own key hash
  const fee = 0.00012917500036169; // Replace with your own fee

  deployer.deploy(LuckyDraw, vrfCoordinator, linkToken, keyHash, fee);
};
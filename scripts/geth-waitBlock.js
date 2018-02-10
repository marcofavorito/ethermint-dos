function waitBlock(txHash) {
  function innerWaitBlock() {
    var receipt = web3.eth.getTransactionReceipt(txHash);
    if (receipt) {
      console.log("Your transaction has been validated");
    } else {
      console.log("Waiting a mined block to include your contract... currently in block " + web3.eth.blockNumber);
      setTimeout(innerWaitBlock, 500);
    }
  }
  innerWaitBlock();
}
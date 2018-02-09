// var addr_1;
// var addr_2;
// addr_1 = eth.accounts[0];
// addr_2 = personal.newAccount("1234");
// personal.unlockAccount(addr_1, "1234", 2000);
// var transaction = function(sender, receiver, amount){
//     // console.log( sender + " => " + receiver + ", " + amount + " ether");
//     return eth.sendTransaction({from:sender, to:receiver, value: web3.toWei(amount, "ether")})
// }
// var hash;
// hash = transaction(addr_1, addr_2, 0.0000000001);
// web3.eth.getTransactionReceipt(hash);


var main = function(test_tx_num) {
    var addr_1 = eth.accounts[0];
    var addr_2 = personal.newAccount("1234");
    personal.unlockAccount(addr_1, "1234", 2000);

    var curTime, hash;
    var startTime = Date.now();
    console.log("Start test time: " + startTime);

    var transactions = {};
    var blocks = {};

    for (var i = 0; i<test_tx_num; i++){
        console.log("tx id: " + i);
            curTime = Date.now();
        hash = transaction(addr_1, addr_2, 0.0000000001);
        console.log(hash);
        transactions[i]={"submit_time": curTime, "hash":hash};
    }

    var endTime = Date.now();



}


var transaction = function(sender, receiver, amount){
    // console.log( sender + " => " + receiver + ", " + amount + " ether");
    return eth.sendTransaction({from:sender, to:receiver, value: web3.toWei(amount, "ether")})
}




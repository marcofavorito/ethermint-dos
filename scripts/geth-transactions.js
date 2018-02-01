var addr_1;
var addr_2;

// var NUM_TX = 10E+10;
// var NUM_TX = 0;

var main = function(test_tx_num) {
    addr_1 = eth.accounts[0];
    addr_2 = personal.newAccount("1234");
    personal.unlockAccount(addr_1, "1234", 300);
    personal.unlockAccount(addr_2, "1234", 300);


    transaction(addr_1, addr_2, 0.000000000001);

    for (var i = 0; i<test_tx_num-1; i++){
        console.log("it: " + i);
        transaction(addr_1, addr_2, 0.000000000000001);
        // transaction(addr_2, addr_1, 0.000000000000001);
    }
}


var transaction = function(sender, receiver, amount){
    console.log( sender + " => " + receiver + ", " + amount + " ether");
    eth.sendTransaction({from:sender, to:receiver, value: web3.toWei(amount, "ether")})
}




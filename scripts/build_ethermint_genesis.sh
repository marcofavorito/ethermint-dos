#!/usr/bin/env bash

# returns a ethermint dir './.ethermint' with new addresses initialized

echo "1234" > password.txt
cat > base_genesis.json <<- EOM
{
    "config": {
        "chainId": 15,
        "homesteadBlock": 0,
        "eip155Block": 0,
        "eip158Block": 0
    },
    "nonce": "0xdeadbeefdeadbeef",
    "timestamp": "0x00",
    "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "mixhash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "difficulty": "0x40",
    "gasLimit": "0x8000000",
    "alloc": {
        "0xADDRESS_1": { "balance": "1000000000000000000" },
        "0xADDRESS_2": { "balance": "1000000000000000000" }
    }
}
EOM

# wipe the old blockchain and wallet/keystore
rm -rf datadir
mkdir datadir

# first we create some accounts
geth --datadir=./datadir --password ./password.txt account new > account1.txt
geth --datadir=./datadir --password ./password.txt account new > account2.txt

ADDRESS_1=$(grep -E --only-matching "[0-9a-f]{40}"  account1.txt)
ADDRESS_2=$(grep -E --only-matching "[0-9a-f]{40}"  account2.txt)

# update genesis json to use the addresses from one of the new accounts
# <script here modifies genesis.json to replace the account ids with the just generated ones>
cp base_genesis.json genesis.json
sed --in-place "s/ADDRESS_1/$ADDRESS_1/" genesis.json
sed --in-place "s/ADDRESS_2/$ADDRESS_2/" genesis.json

# create the blockchain with the fund allocations
geth --datadir ./datadir init genesis.json

rm -R .ethermint
ethermint --datadir .ethermint init genesis.json
rm -R .ethermint/keystore
cp ./datadir/keystore .ethermint/keystore -R



The experiment has been executed by using:

    python3 ethermint-dos.py 4 --verbose
    
Notice the `--verbose` flag, which allows to audit in very detail all the activities under-the-hood.

The network started to validate empty blocks.
Then I simulate an Ethereum transaction through the Ethermint service, using `geth`. After the commit of that tx, I manually stopped the network. 

Files named as `docs/log-nodeX` contains the Tendermint logs for node `X`.
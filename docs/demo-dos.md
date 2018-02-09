The experiment has been executed by using:

    python3 ethermint-dos.py 4 1 --verbosity 1 --dummy --save_logs

We used the `dummy` application for convenience, but the observations made in this documents still hold for other ABCI apps (e.g. Ethermint), since our DoS experiment only affects the consensus phase.

Please, be sure that you have already run `scripts/get_binaries.sh` so you are sure to have the right version of Tendermint and Tendermint Evil.

## Tendermint Evil: what it is?

As explained in other documents, [Tendermint Evil](https://github.com/MarcoFavorito/tendermint/tree/dos-tendermint-master) is my fork of Tendermint Core, where I made some changes in the source code to affect the consensus algorithm.

For this experiment, we'll use [this version](https://github.com/MarcoFavorito/tendermint/releases/tag/v0.12.1). It simply does not send anything on the network.

In the following I show to you how this change affects the consensus phase.

## Description
The byzantine node is `Node 3`.

### Height=1, Round=0
- [Node 0](../res/demo-dos-logs/log-tendermint-node0.log#L55)
- [Node 1](../res/demo-dos-logs/log-tendermint-node1.log#L43)
- [Node 2](../res/demo-dos-logs/log-tendermint-node2.log#L48)
- [Node 3](../res/demo-dos-logs/log-tendermint-node3.log#L59)

The genesis block is correctly committed, since `2/3` of the nodes are enough to complete the consensus phase.
[Here](../res/demo-dos-logs/log-tendermint-node0#L156) you can see the `nil-vote` in the data structure `Commit` of the block at height 2. This is due to the fact that the correct nodes never received pre-votes or pre-commit of the byzantine node for the block at height=1. 

### Height=2, Round=0
- [Node 0](../res/demo-dos-logs/log-tendermint-node0#L103)
- [Node 1](../res/demo-dos-logs/log-tendermint-node1#L104)
- [Node 2](../res/demo-dos-logs/log-tendermint-node2#L104)
- Node 3: X

The system should block here, since the flag `--consensus.create_empty_blocks` is set to `false` for every node. This means that new blocks will be created only if there are some pending transactions.

The byzantine `Node 3` had not proceeded because cannot synchronize with the other nodes.

Now we send a transaction to the network. In another terminal, type:

    curl 'localhost:46607/broadcast_tx_commit?tx="myFirstTransaction"'
    
The `curl` call is blocked until the transaction is committed. The node associated to `localhost:466X7` is `Node X`: in this case, we interact with `Node 0`, but it would be the same if we use `curl` with `localhost:46617` (Node 1) or `localhost:46627` (Node 2).   

The consequences of this commands are the following:
- The transaction is submitted to the `dummy` ABCI app to check if it is valid (by calling `CheckTx` function);
- Once the transaction is checked, it is [added to the mempool and broadcast to the other nodes](../res/demo-dos-logs/log-tendermint-node0.log#L104);
- At this point there is one pending transaction. Hence, every node enter into the `propose` phase.
- The deterministic algorithm to determine the proposer [chooses the byzantine node, `Node 3`. Indeed, check the message `Not our turn to propose` of every correct node:
    - [Node 0](../res/demo-dos-logs/log-tendermint-node0.log#L106)
    - [Node 1](../res/demo-dos-logs/log-tendermint-node1.log#L107)
    - [Node 2](../res/demo-dos-logs/log-tendermint-node2.log#L107)
- ... But unfortunately, no proposal arrive, since the proposer is _silent_. After the [timeout ends](../res/demo-dos-logs/log-tendermint-node0.log#L107) (3 seconds in current configurations), every node [proposes a `nil` block](../res/demo-dos-logs/log-tendermint-node0.log#L109).
- A "`nil` round" is performed (i.e.: nil prevotes and nil precommits) in order to exit the current round and go to the next one.

### Height=2, Round=1

For this round [the proposer is Node 2](../res/demo-dos-logs/log-tendermint-node2.log#L123), which proposes the right block.

Since only one node of four nodes is down, the round is completed correctly.

You can see the votes for block at height=2 on the field `Commit` of the block at height=3:
- [Node 0](../res/demo-dos-logs/log-tendermint-node0.log#L203)
- [Node 1](../res/demo-dos-logs/log-tendermint-node1.log#L201)
- [Node 2](../res/demo-dos-logs/log-tendermint-node2.log#L203)


## Conclusions

As you might have noticed, the only phase affected in validating a transaction is the `Propose` phase. 

Periodically, whenever the byzantine node is chosen, we need an extra round to validate the block, introducing a delay equal to the `timeoutProposeR` (see [here](https://tendermint.readthedocs.io/en/master/specification/byzantine-consensus-algorithm.html#propose-step-height-h-round-r) for details).   
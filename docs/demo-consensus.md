The experiment has been executed by using:

    python3 ethermint-dos.py 4 --verbosity 1
    
Notice the `--verbosity` flag, which allows to audit in very detail all the activities under-the-hood.

The network started to validate empty blocks.
Then I simulate an Ethereum transaction through the Ethermint service, using `geth`. After the commit of that tx, I manually stopped the network. 

All the log files are in `res/demo-consensus-logs`, which contains the Tendermint logs for every node.

## Experiment report step-by-step

Now I'll show you how Tendermint protocol works looking at the generated log by each node in my experiment.
The experiment simply consists of:
- Network setup
- Wait for some empty blocks 
- Send a transaction and wait for its commit
- Network shut down.


As soon as the network is set up (i.e. every node connect with other peers), they start the protocol.

For each of these block, one might observe the algorithm consensus phases (as summarized [here](../README.md#consensus)) by inspecting the logs.
These phases are: 
1. NewHeight
2. Propose
3. Prevote
4. Precommit
5. Commit

Follows the inspection for these three blocks:
1. Empty block
2. Block with one transaction
3. Empty block (after one transaction) 


Notice: the log lines reported in the following subsection are taken from `./log-tendermint-node0` (since a lot of steps are the same for every node), unless otherwise specified. However, to make it easy to browse the logs of the other nodes, I report the start line for the phase I'm talking about.

### 1) Empty block

#### New Height
- [Node 0](../res/demo-consensus-logs/log-tendermint-node0.log#L56)
- [Node 1](../res/demo-consensus-logs/log-tendermint-node1.log#L51)
- [Node 2](../res/demo-consensus-logs/log-tendermint-node2.log#L54)
- [Node 3](../res/demo-consensus-logs/log-tendermint-node3.log#L63)

Nodes started the algorithm to validate a new block (at new height).

#### Propose
- [Node 0](../res/demo-consensus-logs/log-tendermint-node0.log#L57)
- [Node 1](../res/demo-consensus-logs/log-tendermint-node1.log#L52)
- [Node 2](../res/demo-consensus-logs/log-tendermint-node2.log#L55)
- [Node 3](../res/demo-consensus-logs/log-tendermint-node3.log#L64)

All nodes enters in the `Propose` phase.

As explained in the documentation [2] (Proposals):
> The proposer is chosen by a deterministic and non-choking round robin selection algorithm that selects proposers in proportion to their voting power.

You can verify that `Node 0` recognize that it was the proposer for this round:

    I[02-01|10:16:00.154] enterPropose: Our turn to propose module=consensus proposer=03BFB72A3AAEEE7D28774C9DD10DBFD0E6B67479 privValidator="PrivValidator{03BFB72A3AAEEE7D28774C9DD10DBFD0E6B67479 LH:0, LR:0, LS:0}"
    
Then, it prepare the proposal and, before broadcasting to its peer, sign it with its private key:

    I[02-01|10:16:00.237] Signed proposal module=consensus height=1 round=0 proposal="Proposal{1/0 1:8EE72641EA71 (-1,:0:000000000000) {/C4A602980853.../}}"

Upon a node receive the block, they enter into the next phase:

    I[02-01|10:16:00.363] Received complete proposal block module=consensus height=1 hash=2D2480E64F8EEE3D2332B0532920B766ED505287
    
*Notice*: also the proposer receive its proposal, according to the semantics of the broadcast primitive.

### Prevote

- [Node 0](../res/demo-consensus-log/log-tendermint-node0#L61)
- [Node 1](../res/demo-consensus-log/log-tendermint-node1#L55)
- [Node 2](../res/demo-consensus-log/log-tendermint-node2#L64)
- [Node 3](../res/demo-consensus-log/log-tendermint-node3#L67)

Just after the block is received, every node enters into `Prevote` phase:

    I[02-01|10:16:00.363] enterPrevote(1/0). Current: 1/0/RoundStepPropose module=consensus
    
After recognizing that the block is valid:

    I[02-01|10:16:00.363] enterPrevote: ProposalBlock is valid module=consensus height=1 round=0
    
They broadcast their own vote:

    I[02-01|10:16:00.363] enterPrevote: ProposalBlock is valid module=consensus height=1 round=0
    
You can see that every node receives the others' votes (log lines for `Node 0`:

    I[02-01|10:16:00.405] Signed and pushed vote                       module=consensus height=1 round=0 vote="Vote{0:03BFB72A3AAE 1/00/1(Prevote) 2D2480E64F8E {/DE4FB2FFD695.../}}" err=null
    I[02-01|10:16:00.489] Added to prevote                             module=consensus vote="Vote{0:03BFB72A3AAE 1/00/1(Prevote) 2D2480E64F8E {/DE4FB2FFD695.../}}" prevotes="VoteSet{H:1 R:0 T:1 +2/3:<nil> BA{4:X___} map[]}"
    I[02-01|10:16:01.032] Added to prevote                             module=consensus vote="Vote{2:7C596E399C96 1/00/1(Prevote) 2D2480E64F8E {/CF4E83D3F7F9.../}}" prevotes="VoteSet{H:1 R:0 T:1 +2/3:<nil> BA{4:X_X_} map[]}"
    I[02-01|10:16:01.124] Added to prevote                             module=consensus vote="Vote{3:C96BD793411D 1/00/1(Prevote) 2D2480E64F8E {/B30E5A3597DB.../}}" prevotes="VoteSet{H:1 R:0 T:1 +2/3:2D2480E64F8EEE3D2332B0532920B766ED505287:1:8EE72641EA71 BA{4:X_XX} map[]}"
    I[02-01|10:16:01.124] enterPrecommit(1/0). Current: 1/0/RoundStepPrevote module=consensus 
    
Two observations:
- The node receive its prevote (according to broadcast semantics.
- As soon as every nodes receive more than ![](https://latex.codecogs.com/gif.latex?%5Cfrac%7B2%7D%7B3%7D) of the votes (the fraction is intended in terms of **voting power** of the senders), the node enters into the next phase:

    
    I[02-01|10:16:01.124] enterPrecommit(1/0). Current: 1/0/RoundStepPrevote module=consensus 


Notice that 

    #prevotes = 3 > 2/3 * #nodes = 2/3 * 4
    
Since in our example every node has the same voting power.

### Precommit

- [Node 0](../res/demo-consensus-logs/log-tendermint-node0.log#L67)
- [Node 1](../res/demo-consensus-logs/log-tendermint-node1.log#L71)
- [Node 2](../res/demo-consensus-logs/log-tendermint-node2.log#L70)
- [Node 3](../res/demo-consensus-logs/log-tendermint-node3.log#L75)

Here you might observe the interesting Tendermint locking mechanism:  

    I[02-01|10:16:01.124] enterPrecommit(1/0). Current: 1/0/RoundStepPrevote module=consensus 
    I[02-01|10:16:01.124] enterPrecommit: +2/3 prevoted proposal block. Locking module=consensus hash=2D2480E64F8EEE3D2332B0532920B766ED505287

Since no node is locked (we are in the first block), every node can locks on this block and broadcast its `precommit` vote. For details, please refer to [2] (`Precommit Step (height:H,round:R)`):

    I[02-01|10:16:01.236] Signed and pushed vote module=consensus height=1 round=0 vote="Vote{0:03BFB72A3AAE 1/00/2(Precommit) 2D2480E64F8E {/5C5ABFC49697.../}}" err=null
    
Follows the logs lines of received `Vote`:

    I[02-01|10:16:01.504] Added to precommit                           module=consensus vote="Vote{0:03BFB72A3AAE 1/00/2(Precommit) 2D2480E64F8E {/5C5ABFC49697.../}}" precommits="VoteSet{H:1 R:0 T:2 +2/3:<nil> BA{4:X___} map[]}"
    ...
    I[02-01|10:16:01.820] Added to precommit                           module=consensus vote="Vote{2:7C596E399C96 1/00/2(Precommit) 2D2480E64F8E {/F50ABC8EDA13.../}}" precommits="VoteSet{H:1 R:0 T:2 +2/3:<nil> BA{4:X_X_} map[]}"
    I[02-01|10:16:02.115] Added to precommit                           module=consensus vote="Vote{1:44A4C01F4CE8 1/00/2(Precommit) 2D2480E64F8E {/853D00DA3FBB.../}}" precommits="VoteSet{H:1 R:0 T:2 +2/3:2D2480E64F8EEE3D2332B0532920B766ED505287:1:8EE72641EA71 BA{4:XXX_} map[]}"

As soon as more than ![](https://latex.codecogs.com/gif.latex?%5Cfrac%7B2%7D%7B3%7D) of precommit are received, every node goes to the `Commit` phase:

    I[02-01|10:16:02.115] enterCommit(1/0). Current: 1/0/RoundStepPrecommit module=consensus 

### Commit
- [Node 0](../res/demo-consensus-logs/log-tendermint-node0.log#L84)
- [Node 1](../res/demo-consensus-logs/log-tendermint-node1.log#L84)
- [Node 2](../res/demo-consensus-logs/log-tendermint-node2.log#L85)
- [Node 3](../res/demo-consensus-logs/log-tendermint-node3.log#L86)

The commit of the block is finalized:

    I[02-01|10:16:02.214] Finalizing commit of block with 0 txs module=consensus height=1 hash=2D2480E64F8EEE3D2332B0532920B766ED505287 root=
    
Every node waits until block is received:

    I[02-01|10:16:02.214] Block{
      Header{
        ChainID:        chain-XZAHNX
        Height:         1
        Time:           2018-02-01 11:16:00.154 +0100 CET
        NumTxs:         0
        LastBlockID:    :0:000000000000
        LastCommit:     
        Data:           
        Validators:     FE3D4B9214631E68992CBBDC55344E2D9FDED402
        App:            
      }#2D2480E64F8EEE3D2332B0532920B766ED505287
      Data{
        
      }#
      Commit{
        BlockID:    :0:000000000000
        Precommits: 
      }#
    }#2D2480E64F8EEE3D2332B0532920B766ED505287 module=consensus  


For the details about every field, please refer to [this link](https://tendermint.readthedocs.io/en/master/specification/block-structure.html)

Notice:
- the `Commit` refers to the **previous** block, but since we are at block with height=1, we have no previous block to refer.
- the `Header.Data` is empty, since there are no transactions.

Indeed, look [here](https://github.com/tendermint/tendermint/blob/master/types/block.go#L238):

> // Commit contains the evidence that a block was committed by a set of validators.  
> // NOTE: Commit is empty for height 1, but never nil.  
> type Commit struct { ...  

For example, look at the differences with [the block at height=2](https://github.com/MarcoFavorito/ethermint-dos/blob/master/docs/log-tendermint-node0#L130):

    I[02-01|10:16:06.164] Block{
      Header{
        ChainID:        chain-XZAHNX
        Height:         2
        Time:           2018-02-01 11:16:03.324 +0100 CET
        NumTxs:         0
        LastBlockID:    2D2480E64F8EEE3D2332B0532920B766ED505287:1:8EE72641EA71
        LastCommit:     2272D29B326B516182070073CC3C8CC70AD9AE5D
        Data:           
        Validators:     FE3D4B9214631E68992CBBDC55344E2D9FDED402
        App:            3B883DCAA7B8E2519D7CD545AC13CC7CF32A5F09FB664D2620D188F0190D2C3C
      }#467A3BEF16F019DC1DCA3C47D15D93FD5F820291
      Data{
        
      }#
      Commit{
        BlockID:    2D2480E64F8EEE3D2332B0532920B766ED505287:1:8EE72641EA71
        Precommits: Vote{0:03BFB72A3AAE 1/00/2(Precommit) 2D2480E64F8E {/5C5ABFC49697.../}}
        Vote{1:44A4C01F4CE8 1/00/2(Precommit) 2D2480E64F8E {/853D00DA3FBB.../}}
        Vote{2:7C596E399C96 1/00/2(Precommit) 2D2480E64F8E {/F50ABC8EDA13.../}}
        Vote{3:C96BD793411D 1/00/2(Precommit) 2D2480E64F8E {/80BAA270231A.../}}
      }#2272D29B326B516182070073CC3C8CC70AD9AE5D
    }#467A3BEF16F019DC1DCA3C47D15D93FD5F820291 module=consensus 

The field `Header.Data` is still empty (no transactions), while `Header.LastBlockID`, `Header.LastCommit` and `Commit` fields are updated accordingly with the previous commit. 


Then, it moves to `NewHeight(H+1)`


### NewHeight(H+1)


Move Precommits to LastCommit and increment height:

    I[02-01|10:16:03.132] Added to lastPrecommits: VoteSet{H:1 R:0 T:2 +2/3:2D2480E64F8EEE3D2332B0532920B766ED505287:1:8EE72641EA71 BA{4:XXXX} map[]} module=consensus 
    I[02-01|10:16:03.323] enterNewRound(2/0). Current: 2/0/RoundStepNewHeight module=consensus 
    

Wait until StartTime to receive straggler commits:

    I[02-01|10:16:03.116] Timed out module=consensus dur=157.304279ms height=2 round=0 step=RoundStepNewHeight
 
Go to `Propose(H,0)`:

    I[02-01|10:16:03.181] enterNewRound(2/0). Current: 2/0/RoundStepNewHeight module=consensus 



## 2) Block with one transaction
The consensus phases for this block start at the following lines:
- [Node 0](../res/demo-consensus-logs/log-tendermint-node0.log#L210)
- [Node 1](../res/demo-consensus-logs/log-tendermint-node1.log#L208)
- [Node 2](../res/demo-consensus-logs/log-tendermint-node2.log#L209)
- [Node 3](../res/demo-consensus-logs/log-tendermint-node3.log#L209)


After some block, after block at height 3 is committed, the system receives a new transaction.

The schema is almost the same as the previous case, but now [a new transaction is detected](https://github.com/MarcoFavorito/ethermint-dos/blob/master/docs/log-tendermint-node1#L208):

    I[02-01|10:16:11.435] Recheck txs                                  module=mempool numtxs=1 height=3
    I[02-01|10:16:11.436] Done rechecking txs                          module=mempool 
    I[02-01|10:16:11.698] enterPropose(4/0). Current: 4/0/RoundStepNewHeight module=consensus 
    I[02-01|10:16:12.827] enterNewRound(4/0). Current: 4/0/RoundStepNewHeight module=consensus 
    I[02-01|10:16:12.827] enterPropose(4/0). Current: 4/0/RoundStepNewRound module=consensus 
    I[02-01|10:16:12.827] enterPropose: Not our turn to propose        module=consensus proposer=C96BD793411D931858CA78CF09B4C801E53B3A61 privValidator="PrivValidator{44A4C01F4CE8D4798970FB87136E8A1372C1389E LH:3, LR:0, LS:3}"

As you can see, it's not the turn of `Node 0` to propose. But it is the turn of `Node  2`:

    I[02-01|10:16:11.268] Recheck txs                                  module=mempool numtxs=1 height=3
    I[02-01|10:16:11.269] Done rechecking txs                          module=mempool 
    I[02-01|10:16:11.606] enterPropose(4/0). Current: 4/0/RoundStepNewHeight module=consensus 
    I[02-01|10:16:11.606] enterPropose: Our turn to propose            module=consensus proposer=C96BD793411D931858CA78CF09B4C801E53B3A61 privValidator="PrivValidator{C96BD793411D931858CA78CF09B4C801E53B3A61 LH:3, LR:0, LS:3}"
    I[02-01|10:16:11.698] Signed proposal                              module=consensus height=4 round=0 proposal="Proposal{4/0 1:F6F96A06614F (-1,:0:000000000000) {/63DC0A87442C.../}}"


Notice: the transaction has been submitted to the network through `Node 0`:


    I[02-01|10:16:08.903] Added good transaction                       module=mempool tx="\ufffdh\ufffd\ufffd\u00040\ufffd4\u0000\ufffd\u0001_\ufffd\ufffd\u0015\ufffdX\ufffdd\ufffd\ufffd\ufffd\ufffdrg\r\u0013\ufffd\ufffd\ufffd\ufffd\ufffdꚃ\u000fB@\ufffdA\ufffd\ufffd\ufffdjx\ufffdv\ufffd85x\ufffd\ufffdu\ufffd\ufffd\ufffdKJ\ufffd\ufffd%,t\ufffdMAn\ufffd.\ufffd\ufffd\u001a\ufffdx\ufffd\ufffd]\\E\t\u0004d\ufffd\ufffdrf\ufffd#~\u001bR\ufffd*\ufffd@\ufffd$\ufffd\ufffdýQ3\\m" res="&{CheckTx:Error code (0): }"
    I[02-01|10:16:08.903] HTTPRestRPC                                  module=rpc-server method=/broadcast_tx_sync args="[<[]uint8 Value>]" returns="[<*core_types.ResultBroadcastTx Value> <error Value>]"
    I[02-01|10:16:08.903] Served RPC HTTP response                     module=rpc-server method=POST url=/broadcast_tx_sync status=200 duration=0 remoteAddr=127.0.0.1:44434

and detected by the other nodes:
        
    I[02-01|10:16:09.004] Added good transaction module=mempool tx="\ufffdh\ufffd\ufffd\u00040\ufffd4\u0000\ufffd\u0001_\ufffd\ufffd\u0015\ufffdX\ufffdd\ufffd\ufffd\ufffd\ufffdrg\r\u0013\ufffd\ufffd\ufffd\ufffd\ufffdꚃ\u000fB@\ufffdA\ufffd\ufffd\ufffdjx\ufffdv\ufffd85x\ufffd\ufffdu\ufffd\ufffd\ufffdKJ\ufffd\ufffd%,t\ufffdMAn\ufffd.\ufffd\ufffd\u001a\ufffdx\ufffd\ufffd]\\E\t\u0004d\ufffd\ufffdrf\ufffd#~\u001bR\ufffd*\ufffd@\ufffd$\ufffd\ufffdýQ3\\m" res="&{CheckTx:Error code (0): }"

Follow the links to the lines:
- [Node 0](../res/demo-consensus-logs/log-tendermint-node0.log#L162)
- [Node 1](../res/demo-consensus-logs/log-tendermint-node1.log#L163)
- [Node 2](../res/demo-consensus-logs/log-tendermint-node2.log#L167)
- [Node 3](../res/demo-consensus-logs/log-tendermint-node3.log#L169)


The main differences are about [the block data](../res/demo-consensus-logs/log-tendermint-node0.log#L228):

    I[02-01|10:16:14.679] Finalizing commit of block with 1 txs        module=consensus height=4 hash=8E361D1FBB827F4EDBD2C7D9F4B0E0FAF7514001 root=4B839CE019F4D1165EB57F7BF08A2299CBC7318E4342DF6FEA10A7DFED2FAA99
    I[02-01|10:16:14.680] Block{
      Header{
        ChainID:        chain-XZAHNX
        Height:         4
        Time:           2018-02-01 11:16:11.606 +0100 CET
        NumTxs:         1
        LastBlockID:    8167EB816B6E6AFC24F0B2082AD4A36FA4968794:1:4E7A443194E8
        LastCommit:     FA489A7A165CA652C4120484B502D275C2B43998
        Data:           699EBA54C9B26ABD2629627824C9A0ECE580D6D5
        Validators:     FE3D4B9214631E68992CBBDC55344E2D9FDED402
        App:            4B839CE019F4D1165EB57F7BF08A2299CBC7318E4342DF6FEA10A7DFED2FAA99
      }#8E361D1FBB827F4EDBD2C7D9F4B0E0FAF7514001
      Data{
        Tx:Tx{F86880850430E2340083015F909415F058D864DCEBE3DC72670D13C7EDD7EF9EEA9A830F42408041A0BDE96A78E176903835788B9E75F2EF8F4B4ACADE252C74E64D416EF52EB5801AA078EFEF5D5C4509046495F6726691237E1B52E02ADE408024B99AC3BD51335C6D}
      }#699EBA54C9B26ABD2629627824C9A0ECE580D6D5
      Commit{
        BlockID:    8167EB816B6E6AFC24F0B2082AD4A36FA4968794:1:4E7A443194E8
        Precommits: Vote{0:03BFB72A3AAE 3/00/2(Precommit) 8167EB816B6E {/07DAA5991D39.../}}
        nil-Vote
        Vote{2:7C596E399C96 3/00/2(Precommit) 8167EB816B6E {/0012FD990FF2.../}}
        Vote{3:C96BD793411D 3/00/2(Precommit) 8167EB816B6E {/D1CED5081293.../}}
      }#FA489A7A165CA652C4120484B502D275C2B43998
    }#8E361D1FBB827F4EDBD2C7D9F4B0E0FAF7514001 module=consensus 
    I[02-01|10:16:14.698] Timed out                                    module=consensus dur=3s height=4 round=0 step=RoundStepPropose
    I[02-01|10:16:15.068] Executed block                               module=state height=4 validTxs=1 invalidTxs=0






## 3) Empty block (after one transaction)

For the other block there are no relevant differences with case 1). The block is correctly chained with the last commit (i.e. block at point 2).

## References

- [[1] Tendermint Docs: Introduction](https://tendermint.readthedocs.io/en/master/introduction.html)
- [[2] Tendermint Docs: Byzantine Consensus Algorithm](https://tendermint.readthedocs.io/en/master/specification/byzantine-consensus-algorithm.html)
- [[3] Tendermint:  Byzantine Fault Tolerance in the Age of Blockchains](https://allquantor.at/blockchainbib/pdf/buchman2016tendermint.pdf)
- [[4] Tendermint: Consensus without Mining](https://tendermint.com/static/docs/tendermint.pdf)
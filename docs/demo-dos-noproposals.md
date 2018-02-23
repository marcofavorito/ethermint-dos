# DoS with [Tendermint Evil 'NoProposals'](https://github.com/MarcoFavorito/tendermint/releases/tag/v0.12.1.3)

## Introduction
In this document I'll report and describe the logs of the execution of the following command:
    
    python3 ethermint-dos.py 4 2 --tendermint_evil 'noproposals' --verbosity 1 --save-logs
    
I.e. a Tendermint network of 4 nodes with 2 byzantine nodes of type ['NoProposals'](https://github.com/MarcoFavorito/tendermint/releases/tag/v0.12.1.3).

## What happens
The algorithm proceeds as always, but when it is the turn of the byzantines to propose a new block, they simply do not send anything, no blocks and no proposal message. The round is skipped and when a correct node becomes proposer, the algorithm works correctly (because the other 2 byzantine nodes take part to the algorithm i.e. send Prevotes and Precommit).

## The Network
In this experiment, the network is composed as the following:
- Node 0 is correct;
- Node 1 is correct;
- Node 2 is byzantine;
- Node 3 is byzantine;

## Logs description
[Here](../res/demo-dos-noproposals) you can find the logs of the activity of the network configured as described above.

We'll see in detail each step of some blocks validation.

### Height=1
Follows the log line ranges at height 1 for every node:

- [Node 0](../res/demo-dos-noproposals/log-tendermint-node0.log#L50-L127)
- [Node 1](../res/demo-dos-noproposals/log-tendermint-node1.log#L55-L125)
- [Node 2](../res/demo-dos-noproposals/log-tendermint-node2.log#L46-L125)
- [Node 3](../res/demo-dos-noproposals/log-tendermint-node3.log#L40-L127)

#### Height=1 Round=0
- It's time for the node 2 to propose (see [lines 48-49](../res/demo-dos-noproposals/log-tendermint-node2.log#L48-L49)).
- Since it is byzantine it actually does not send anything.
- The other nodes, once the timeout expires, prevote for `nil` (see e.g. the proposal of node 0, [lines 69-72](../res/demo-dos-noproposals/log-tendermint-node0.log#L69-L72))

#### Height=1 Round=1
- It's time for the node 0 to propose (see [lines 48-49](../res/demo-dos-noproposals/log-tendermint-node0.log#L82-L85)).
- Since it is correct, it proposes and sends a block to its peers.
- The other nodes, once received the proposal block, prevote for it. 
    - Node 1: [lines 84-87](../res/demo-dos-noproposals/log-tendermint-node1.log#L84-L87)
    - Node 2: [lines 85-88](../res/demo-dos-noproposals/log-tendermint-node2.log#L85-L88)
    - Node 3: [lines 87-90](../res/demo-dos-noproposals/log-tendermint-node3.log#L87-L90)

### Height=2
Follows the log line ranges at height 2 for every node:

- [Node 0](../res/demo-dos-noproposals/log-tendermint-node0.log#L128-L176)
- [Node 1](../res/demo-dos-noproposals/log-tendermint-node1.log#L126-L173)
- [Node 2](../res/demo-dos-noproposals/log-tendermint-node2.log#L126-L173)
- [Node 3](../res/demo-dos-noproposals/log-tendermint-node3.log#L128-L175)


#### Height=2 Round=0
- It's time for the node 0 to propose (see [lines 129-131](../res/demo-dos-noproposals/log-tendermint-node0.log#L129-L131)).
- Since it is correct, it proposes and sends a block to its peers.
- The other nodes, once received the proposal block, prevote for it. 
    - Node 1: [lines 129-132](../res/demo-dos-noproposals/log-tendermint-node1.log#L129-L132)
    - Node 2: [lines 129-132](../res/demo-dos-noproposals/log-tendermint-node2.log#L129-L132)
    - Node 3: [lines 131-134](../res/demo-dos-noproposals/log-tendermint-node3.log#L131-L134)

### Height=3
Follows the log line ranges at height 2 for every node:

- [Node 0](../res/demo-dos-noproposals/log-tendermint-node0.log#L177-L223)
- [Node 1](../res/demo-dos-noproposals/log-tendermint-node1.log#L174-L221)
- [Node 2](../res/demo-dos-noproposals/log-tendermint-node2.log#L174-L220)
- [Node 3](../res/demo-dos-noproposals/log-tendermint-node3.log#L176-L223)

#### Height=3 Round=0
- It's time for the node 1 to propose (see [lines 175-177](../res/demo-dos-noproposals/log-tendermint-node1.log#L175-L177)).
- Since it is correct, it proposes and sends a block to its peers.
- The other nodes, once received the proposal block, prevote for it. 
    - Node 0: [lines 180-183](../res/demo-dos-noproposals/log-tendermint-node0.log#L180-L183)
    - Node 2: [lines 177-180](../res/demo-dos-noproposals/log-tendermint-node2.log#L177-L180)
    - Node 3: [lines 179-182](../res/demo-dos-noproposals/log-tendermint-node3.log#L179-L182)

### Height=4
Follows the log line ranges at height 4 for every node:
- [Node 0](../res/demo-dos-noproposals/log-tendermint-node0.log#L224-L304)
- [Node 1](../res/demo-dos-noproposals/log-tendermint-node1.log#L222-L303)
- [Node 2](../res/demo-dos-noproposals/log-tendermint-node2.log#L221-L300)
- [Node 3](../res/demo-dos-noproposals/log-tendermint-node3.log#L224-L300)

#### Height=4 Round=0
- It's time for the node 3 to propose (see [lines 226-227](../res/demo-dos-noproposals/log-tendermint-node3.log#L226-L227)).
- Since it is byzantine it actually does not send anything.
- The other nodes, once the timeout expires, prevote for `nil` (see the proposal of node 0, [lines 227-230](../res/demo-dos-noproposals/log-tendermint-node0.log#L227-L230))

#### Height=4 Round=1
- It's time for the node 2 to propose (see [lines 239-240](../res/demo-dos-noproposals/log-tendermint-node2.log#L239-L240)).
- Since it is byzantine it actually does not send anything.
- The other nodes, once the timeout expires, prevote for `nil` (see the proposal of node 0, [lines 244-247](../res/demo-dos-noproposals/log-tendermint-node0.log#L244-L247))

#### Height=4 Round=2
- It's time for the node 0 to propose (see [lines 258-260](../res/demo-dos-noproposals/log-tendermint-node0.log#L258-L260)).
- Since it is correct, it proposes and sends a block to its peers.
- The other nodes, once received the proposal block, prevote for it. 
    - Node 1: [lines 260-263](../res/demo-dos-noproposals/log-tendermint-node1.log#L260-L263)
    - Node 2: [lines 258-261](../res/demo-dos-noproposals/log-tendermint-node2.log#L258-L261)
    - Node 3: [lines 258-261](../res/demo-dos-noproposals/log-tendermint-node3.log#L258-L261)

### Height=5
Follows the log line ranges at height 4 for every node:
- [Node 0](../res/demo-dos-noproposals/log-tendermint-node0.log#L306-L369)
- [Node 1](../res/demo-dos-noproposals/log-tendermint-node1.log#L305-L364)
- [Node 2](../res/demo-dos-noproposals/log-tendermint-node2.log#L302-L365)
- [Node 3](../res/demo-dos-noproposals/log-tendermint-node3.log#L302-L364)

#### Height=5 Round=0
- It's time for the node 2 to propose (see [lines 302-304](../res/demo-dos-noproposals/log-tendermint-node2.log#L302-L304)).
- Since it is byzantine it actually does not send anything.
- The other nodes, once the timeout expires, prevote for `nil` (see the proposal of node 0, [lines 308-311](../res/demo-dos-noproposals/log-tendermint-node0.log#L308-L311))

#### Height=5 Round=1
- It's time for the node 0 to propose (see [lines 322-324](../res/demo-dos-noproposals/log-tendermint-node0.log#L322-L324)).
- Since it is correct, it proposes and sends a block to its peers.
- The other nodes, once received the proposal block, prevote for it. 
    - Node 1: [lines 321-324](../res/demo-dos-noproposals/log-tendermint-node1.log#L321-L324)
    - Node 2: [lines 322-325](../res/demo-dos-noproposals/log-tendermint-node2.log#L322-L325)
    - Node 3: [lines 321-324](../res/demo-dos-noproposals/log-tendermint-node3.log#L321-L324)

### Height>=6
At this point, since the round-robin procedure that choose the next proposer is fair and deterministic, the sequence of the chosen proposer for each height/round is the same.
Indeed, notice that:
    
    (Height, Round) Proposer Node
    -------------------------------------
    ( 1, 0)          2          <
    ( 1, 1)          0
    ( 2, 0)          0          <
    ( 3, 0)          1          <
    ( 4, 0)          3          <
    ( 4, 1)          2
    ( 4, 2)          0
    ( 5, 0)          2          <
    ( 5, 1)          0
    ( 6, 0)          0          <
    ( 7, 0)          1          <
    ( 8, 0)          3          <
    ( 8, 1)          2
    ( 8, 2)          1
    ( 9, 0)          2          <
    ( 9, 1)          0
    (10, 0)          0          <
    
The sequence for the first round of every block is:

    (2 0 1 3)+
    
## Conclusions
As expected, the algorithm goes on even if we have 2 byzantine nodes (and N >= 3f + 1 does not hold), since the byzantine nodes participate in the algorithm.
The algorithm is delayed periodically thanks to the determinism of the round-robin procedure that chooses the proposer.


 

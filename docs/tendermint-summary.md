# Tendermint Core: a brief summary

## Consensus

### Working assumptions
Now we describe the working assumptions for the consensus algorithm, in the light of [FLP impossbiility](https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf).
The working assumptions (stated in [1] 6.1 On Byzantine Consensus):
> 1. The network is partially synchronous;
> 2. All non-byzantine nodes have access to an internal clock that can stay sufficiently accurate for a short duration of time until consensus on the next block is achieved; The clocks do not need to agree on a global time and may drift at some bounded rate relative to global time.
> 3. At least 2/3 of the voting power is honest;

In [Tendermint: Consistent or Available](report.md#tendermint:-consistent-or-available?) the assumptions are discussed in more detail.


### Consensus Phases
There are 3 phases + 2 special phases, Commit and NewHeight:
- Propose
- Prevote
- Precommit
- Commit
- NewHeight

A _Round_ is:
    
    Propose -> Prevote -> Precommit

In the optimal scenario, the order of steps is:

    NewHeight -> Propose -> Prevote -> Precommit+ -> Commit -> NewHeight ->...


Why things might go wrong? Some examples:

    - The designated proposer was not online.
    - The block proposed by the designated proposer was not valid.
    - The block proposed by the designated proposer did not propagate in time.
    - The block proposed was valid, but +2/3 of prevotes for the proposed block were not received in time for enough validator nodes by the time they reached the Precommit step. Even though +2/3 of prevotes are necessary to progress to the next step, at least one validator may have voted <nil> or maliciously voted for something else.
    - The block proposed was valid, and +2/3 of prevotes were received for enough nodes, but +2/3 of precommits for the proposed block were not received for enough validator nodes.

Common exit conditions:

- After +2/3 precommits for a particular block. –> goto Commit(H)
- After any +2/3 prevotes received at (H,R+x). –> goto Prevote(H,R+x)
- After any +2/3 precommits received at (H,R+x). –> goto Precommit(H,R+x)


Now I briefly describe every phase of the state machine behind the Tendermint protocol. The specification is mainly taken from [3].

#### Propose (height H, round R)

Upon entering Propose, the designated proposer proposes a block at height `H` and round `R`.

- The **proposer** is chosen by a deterministic and non-choking round robin selection algorithm that selects proposers **in proportion to their voting power**. (see [implementation](https://github.com/tendermint/tendermint/blob/develop/types/validator_set.go))
- A proposal is signed and published by the designated proposer at each round. 

Exit conditions:
- After timeoutProposeR after entering Propose. –> goto Prevote(H,R)
- After receiving proposal block and all prevotes at PoLC-Round. –> goto Prevote(H,R)
- After common exit conditions


DEF **Proposal**:
- a block 
- an optional latest `PoLC-Round < R` (proof-of-lock-change) which is included iff the proposer knows of one. This hints the network to allow nodes to unlock (when safe) to ensure the **liveness property** 



#### Prevote Step (height H, round R)

Upon entering Prevote, each validator broadcasts its prevote vote.

- First, if the validator is locked on a block since LastLockRound but now has a PoLC for something else at round PoLC-Round where LastLockRound < PoLC-Round < R, then it unlocks.
- If the validator is still locked on a block, it prevotes that.
- Else, if the proposed block from Propose(H,R) is good, it prevotes that.
- Else, if the proposal is invalid or wasn’t received on time, it prevotes <nil>.

The Prevote step ends: 
- After +2/3 prevotes for a particular block or <nil>. –> goto Precommit(H,R)
- After timeoutPrevote after receiving any +2/3 prevotes. –> goto Precommit(H,R) 
- After common exit conditions



#### Precommit Step (height H, round R)

Upon entering Precommit, each validator broadcasts its precommit vote. 

- If the validator has a PoLC at (H,R) for a particular block B, it (re)locks (or changes lock to) and precommits B and sets LastLockRound = R. 
- Else, if the validator has a PoLC at (H,R) for <nil>, it unlocks and precommits <nil>. 
- Else, it keeps the lock unchanged and precommits <nil>.

A precommit for <nil> means “I didn’t see a PoLC for this round, but I did get +2/3 prevotes and waited a bit”.

The Precommit step ends: 
- After +2/3 precommits for <nil>. –> goto Propose(H,R+1)
- After timeoutPrecommit after receiving any +2/3 precommits. –> goto Propose(H,R+1)
- After common exit conditions

#### Commit Step (height H)

Set CommitTime = now()
Wait until block is received. –> goto NewHeight(H+1)


#### NewHeight Step (height H)

- Move Precommits to LastCommit and increment height.
- Set StartTime = CommitTime+timeoutCommit
- Wait until StartTime to receive straggler commits. –> goto Propose(H,0)


### Miscellanea

#### Gossip
[Background Gossip](https://tendermint.readthedocs.io/en/master/specification/byzantine-consensus-algorithm.html#background-gossip) 

- A node **MAY NOT HAVE** a corresponding validator private key, but it nevertheless **plays an active role in the consensus process** by relaying relevant meta-data, proposals, blocks, and votes to its peers.
- **validator-node**:
> - has the private keys of an active validator
> -  is engaged in signing votes

- **All nodes** (not just validator-nodes) have an **associated state** (the current height, round, and step) and work to make progress.

`Connection` and `Channel`
 **epidemic gossip protocol**
 



## References
- [[1] Tendermint: Consensus without Mining](https://tendermint.com/static/docs/tendermint.pdf)
- [[2] Tendermint:  Byzantine Fault Tolerance in the Age of Blockchains](https://allquantor.at/blockchainbib/pdf/buchman2016tendermint.pdf)
- [[3] Tendermint Read the Docs](http://tendermint.readthedocs.io/projects/tools/en/master/index.html#)]
- [[4] Practical Byzantine Fault Tolerance](http://pmg.csail.mit.edu/papers/osdi99.pdf)
- [[5] Consensus in the presence of Partial Synchrony](https://groups.csail.mit.edu/tds/papers/Lynch/jacm88.pdf)




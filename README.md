# ethermint-dos
Ethermint Denial-of-Service experiment
 
A university project in which I test how a byzantine client in a Ethermint network affects the consensus phases. Please refer to [my version of tendermint](https://github.com/MarcoFavorito/tendermint) for the modified source code.

[Here](docs/report.md) you will find the report.

- [Repo structure](#repo-structure)
- [How to use](#how-to-use)
- [What is Tendermint](#what-is-tendermint)
- [What is Ethermint](#what-is-ethermint)
- [DoS](#dos)


## Repo structure

- `app/`: Python code for the experiment execution. Its entry point is `ethermint-dos.py`;
- `bench/`: scripts for benchmarking various network configurations (i.e. with and without byzantine nodes);
- `bin/`: Binaries for the experiment, namely:
    - `tendermint` (v0.12.1): Tendermint Core binary.
    - `tendermint_evil`: [my fork](https://github.com/MarcoFavorito/tendermint) of `tendermint` (v0.12.1);
    - `ethermint` (v0.5.3): the Ethermint ABCI app, which interacts with Tendermint for the consensus and implements the logic of Ethereum.
- `docs/`: contains:
    - `report.md`: description of the project purposes;
    - `logs.md`: step-by-step report of a Tendermint network activity;
- `res/`: some files referenced from the docs;
- `scripts/` contains useful scripts to install the dependencies. 
    - `clean.sh`: remove working folders after the execution of `ethermint-dos.py`;
    - `get_binaries.sh` allows you to update the `bin/` content;
    - `geth-script-loader.sh` is an utility script for inject commands into the JavaScript console;
## How to use

`ethermint-dos.py` is a useful script for rapidly set up a Ethermint/Tendermint network.

Usage:

    python3 ethermint-dos.py -h
    
However, it uses system commands such as `gnome-terminal`, so there are high chances that your platform cannot support it. Sorry. 

I'll update the script to allow one node to call `bin/tendermint_evil`: that node will be our byzantine client.

There will be also some scripts for benchmarking (in terms of e.g. transactions/block throughput) between zero byzantine and one byzantine.

**Notice**: when playing with the script, you might find the following commands quite useful:

    for pid in $(ps -ef | grep "tendermint" | awk '{print $2}'); do sudo kill -9 $pid; done
    for pid in $(ps -ef | grep "ethermint" | awk '{print $2}'); do sudo kill -9 $pid; done

 

## What is Tendermint
Ethermint is built upon Tendermint... But [what is Tendermint](https://tendermint.readthedocs.io/en/master/introduction.html)?

[Tendermint](https://tendermint.com/) is a software for Byzantine fault-tolerant (BFT) state machines replication, powered by blockchain-based consensus. It is **secure**, since allow to 1/3 of nodes to fail, and **consistent**, since every correct node agree on the same state of the application.

The two main component of Tendermint are:
1. **Tendermint Core**: consensus engine
2. **Application BlockChain Interface** (ABCI): enables the transactions to be processes in any programming language


### How ABCI works: message types
Tendermint Core interacts with the application via a socket protocol that satisfies ABCI. [Here](https://tendermint.readthedocs.io/en/master/introduction.html#intro-to-abci) you might find an enlighting example with the Bitcoin system.

The message types exchanged by nodes are many. The more important are 3:

1. **DeliverTx**: with which every transaction is delivered in the blockchain. Application needs to validate each transaction received with the DeliverTx message against the current state.
2. **CheckTx**: used for validate transactions, before entering into the mempool.
3. **Commit**: used to compute a cryptographic commitment to the current application state, to be placed into the next block header.

Tendermint Core creates three ABCI connections to the application:

1. for validating transactions to put into the mempool;
2. for run block proposals for the consensus engine;
3. for querying the app state


#### other message types:
see [here](https://github.com/tendermint/abci#message-types)
TendermintCore sends the requests, and the ABCI application sends the responses. Here, we describe the requests and responses as function arguments and return values, and make some notes about usage:

- Echo
- Flush
- Info
> **LastBlockHeight** (int64): Latest block for which the app has called Commit
>**LastBlockAppHash** ([]byte): Latest result of Commit
- SetOption
- InitChain
- Query
- BeginBlock
- CheckTx
- DeliverTx
- EndBlock
- Commit

### Blocks
[Blocks](https://godoc.org/github.com/tendermint/tendermint/types#Block) are made of:

- Header
- Data
- Last Commit

The **[Header](https://godoc.org/github.com/tendermint/tendermint/types#Header)** contains :
> - last block info
> - prev block info 
> - hashes of block data
> - hashes from the app output from the prev block
> - consensus info: the evidence

The [Commit](https://godoc.org/github.com/tendermint/tendermint/types#Commit)
> Set of [Votes](https://godoc.org/github.com/tendermint/tendermint/types#Vote)
> 	mainly containing the **signature**, the **address** of the validator and other infos about block

The [BlockID](https://godoc.org/github.com/tendermint/tendermint/types#BlockID):
> **BlockHash**: hash of the block header
> **[PartSetHeader](https://tendermint.readthedocs.io/en/master/specification/block-structure.html#partset)**: 
>	- total number of pieces in a PartSet 
> 	- the Merkle root hash of those pieces
> see LibSwift
> PartSet is used to split a byteslice of data into parts (pieces) for transmission. By splitting data into smaller parts and computing a Merkle root hash on the list, you can verify that a part is legitimately part of the complete data, and the part can be forwarded to other peers before all the parts are known. In short, it’s a fast way to securely propagate a large chunk of data (like a block) over a gossip network.


### Consensus
[paper on Tendermint](https://tendermint.com/static/docs/tendermint.pdf) 
- Description of the working assumptions for the consensus algorithm, in the light of [FLP impossbiility](https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf)
> - Partial-synchrony
> - all non-byzantine nodes have access to an internal clock that can stay sufficiently accurate for a short duration of time until consensus on the next block is achieved
>

#### Overview
see [this image](https://tendermint.readthedocs.io/en/master/_images/consensus_logic.png) and [this](https://tendermint.readthedocs.io/en/master/introduction.html#consensus-overview)

also this [schema](https://tendermint.readthedocs.io/en/master/_images/tm-transaction-flow.png) is helpful

#### State machine
At each height of the blockchain, a **round-based protocol** is run to determine the next block

Steps: **NewHeight**, **Propose**, **Prevote**, **Precommit**, and **Commit**

DEF **Round**: 
> (Propose -> Prevote -> Precommit)

Optimal scenario: 
> NewHeight -> (Propose -> Prevote -> Precommit)+ -> Commit 

Why things might go wrong?
Examples:

    - The designated proposer was not online.
    - The block proposed by the designated proposer was not valid.
    - The block proposed by the designated proposer did not propagate in time.
    - The block proposed was valid, but +2/3 of prevotes for the proposed block were not received in time for enough validator nodes by the time they reached the Precommit step. Even though +2/3 of prevotes are necessary to progress to the next step, at least one validator may have voted <nil> or maliciously voted for something else.
    - The block proposed was valid, and +2/3 of prevotes were received for enough nodes, but +2/3 of precommits for the proposed block were not received for enough validator nodes.

#### Gossip
[here](https://tendermint.readthedocs.io/en/master/specification/byzantine-consensus-algorithm.html#background-gossip) 

- A node **MAY NOT HAVE** a corresponding validator private key, but it nevertheless **plays an active role in the consensus process** by relaying relevant meta-data, proposals, blocks, and votes to its peers.
- **validator-node**:
> - has the private keys of an active validator
> -  is engaged in signing votes

- **All nodes** (not just validator-nodes) have an **associated state** (the current height, round, and step) and work to make progress.

`Connection` and `Channel`
 **epidemic gossip protocol**
 
### Consensus Phases

- Propose
- Prevote
- Precommit
- Commit
- NewHeight

#### Propose
- The **proposer** is chosen by a deterministic and non-choking round robin selection algorithm that selects proposers **in proportion to their voting power**. (see [implementation](https://github.com/tendermint/tendermint/blob/develop/types/validator_set.go))
- A proposal is signed and published by the designated proposer at each round. 


DEF **Proposal**:
> - a block 
> - an optional latest `PoLC-Round < R` (proof-of-lock-change) which is included iff the proposer knows of one. This hints the network to allow nodes to unlock (when safe) to ensure the **liveness property** 

#### Prevote
TODO
#### Precommit
TODO
#### Commit
TODO
#### NewHeight
TODO

## What is Ethermint
In short, it is an app that:

- implements the logic of Ethereum
- is ABCI-compliant

All consensus stuff is managed by Tendermint Core. 

## DoS
Question: How a (byzantine) node can affect the consensus phase?
Let's assume in the first istance the failure is **fail-silent**. This means that it sends no message in the network.
Some important informations about the node are:

- It is a validator node or not? If yes, which is its voting power?
- How it is connected with other nodes?
- Which are its peers? How many validators?

Some important informations (to keep in mind when considering a silent node):

- Each round is longer than the previous round by a small fixed increment of time. This allows the network to eventually achieve consensus in a partially synchronous network.
- Each round has a designated proposer chosen in round-robin fashion such that validators are chosen with frequency in proportion to their voting power
- Propose phase:
> - In the beginning of the Propose step the designated proposer for that round broadcasts a proposal to its peers via gossip.
> - If the proposer is locked on a block from some prior round it proposes the locked block and includes a proof-of-lock in the proposal (more on that later).
> - During the Propose step all nodes gossip the proposal to their neighboring peers.
- [PartSet](https://tendermint.readthedocs.io/en/master/specification/block-structure.html#partset)


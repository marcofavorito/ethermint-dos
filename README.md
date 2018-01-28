# ethermint-dos
Ethermint Denial-of-Service experiment
 
A university project in which I test how a byzantine client in a Ethermint network affects the consensus phases. please refer to [my version of ethermint](https://github.com/MarcoFavorito/ethermint) for the modified source code.

### What is Tendermint
Ethermint is built upon Tendermint... But [what is Tendermint](https://tendermint.readthedocs.io/en/master/introduction.html) what is Tendermint?

[Tendermint](https://tendermint.com/) is a software for Byzantine fault-tolerant (BFT) state machines replication, powered by blockchain-based consensus. It is **secure**, since allow to 1/3 of nodes to fail, and **consistent**, since every correct node agree on the same state of the application.

The two main component of Tendermint are:
1. **Tendermint Core**: consensus engine
2. **Application BlockChain Interface** (ABCI): enables the transactions to be processes in any programming language


#### How ABCI works: message types
Tendermint Core interacts with the application via a socket protocol that satisfies ABCI. [Here](https://tendermint.readthedocs.io/en/master/introduction.html#intro-to-abci) you might find an enlighting example with the Bitcoin system.

The message types exchanged by nodes are many. The more important are 3:

1. **DeliverTx**: with which every transaction is delivered in the blockchain. Application needs to validate each transaction received with the DeliverTx message against the current state.
2. **CheckTx**: used for validate transactions, before entering into the mempool.
3. **Commit**: used to compute a cryptographic commitment to the current application state, to be placed into the next block header.

Tendermint Core creates three ABCI connections to the application:

1. for validating transactions to put into the mempool;
2. for run block proposals for the consensus engine;
3. for querying the app state

#### Consensus overview
see [this image](https://tendermint.readthedocs.io/en/master/_images/consensus_logic.png) and [this](https://tendermint.readthedocs.io/en/master/introduction.html#consensus-overview)


#### other message types:
see [here](https://github.com/tendermint/abci#message-types)
TendermintCore sends the requests, and the ABCI application sends the responses. Here, we describe the requests and responses as function arguments and return values, and make some notes about usage:

- Echo
- Flush
- Info
- SetOption
- InitChain
- Query
- BeginBlock
- CheckTx
- DeliverTx
- EndBlock
- Commit
# ethermint-dos
Ethermint Denial-of-Service experiment
 
A university project in which I test how a byzantine client in a Ethermint network affects the consensus phases. Please refer to [my version of tendermint](https://github.com/MarcoFavorito/tendermint) for the modified source code.

[Here](docs/report.md) you will find the report.

- [Repo structure](#repo-structure)
- [How to use](#how-to-use)
- [What is Tendermint](#what-is-tendermint)
- [What is Ethermint](#what-is-ethermint)
- [DoS](#dos)

The platform used is `Ubuntu 16.04.3 LTS`.

## Repo structure

- `app/`: Python code for the experiment execution. Its entry point is `ethermint-dos.py`;
- `bench/`: scripts for benchmarking various network configurations (i.e. with and without byzantine nodes);
- `bin/`: Binaries for the experiment, namely:
    - `tendermint` (v0.12.1): Tendermint Core binary.
    - `tendermint_evil`: Symbolic link to one of the Tendermint Evil versions. See [my fork](https://github.com/MarcoFavorito/tendermint) of `tendermint` (v0.12.1);
    - `ethermint` (v0.5.3): the Ethermint ABCI app, which interacts with Tendermint for the consensus and implements the logic of Ethereum.
    - other Tendermint Evil binaries:
- `docs/`: contains:
    - `report.md`: description of the project purposes;
    - `logs.md`: step-by-step report of a Tendermint network activity;
- `res/`: some files referenced from the docs;
- `scripts/` contains useful scripts to install the dependencies. 
    - `clean.sh`: remove working folders after the execution of `ethermint-dos.py`;
    - `get_binaries.sh` allows you to update the `bin/` content;
    - `geth-script-loader.sh` is an utility script for inject commands into the JavaScript console;
## How to use
First of all, run:

    ./scripts/get_binaries.sh

To download all the needed binaries in `./bin`.

`ethermint-dos.py` is a useful script for rapidly set up a Ethermint/Tendermint network.

Usage:

    python3 ethermint-dos.py -h
    
However, it uses system commands such as `gnome-terminal`, so there are high chances that your platform cannot support it. Sorry. 

I'll update the script to allow one node to call `bin/tendermint_evil`: that node will be our byzantine client. It is a symbolic link to one of the choosen byzantine versions of Tendermint (default: [Tendermint Evil 'Shy'](https://github.com/MarcoFavorito/tendermint/releases/tag/v0.12.1.2))

There will be also some scripts for benchmarking (in terms of e.g. transactions/block throughput) between zero byzantine and one byzantine.

**Notice**: when playing with the script, you might find the following commands quite useful:

    for pid in $(ps -ef | grep "tendermint" | awk '{print $2}'); do sudo kill -9 $pid; done
    for pid in $(ps -ef | grep "ethermint" | awk '{print $2}'); do sudo kill -9 $pid; done
    docker rm -f $(docker ps -aq)
 

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

### How Tendermint Core works: the consensus algorithm

Tendermint Core manages the Proof-of-Stake consensus algorithm to commit the incoming transactions in the blockchain.


You might be interested in this schemas:
- [Consensus overview](https://tendermint.readthedocs.io/en/master/_images/consensus_logic.png) and [this](https://tendermint.readthedocs.io/en/master/introduction.html#consensus-overview)
- [Tendermint in a Nutshell](https://tendermint.readthedocs.io/en/master/_images/tm-transaction-flow.png) is helpful
 
For further details, please read [this summary](./docs/tendermint-summary.md).

## What is Ethermint
In short, it is an app that:

- implements the logic of Ethereum
- is ABCI-compliant

All consensus stuff is managed by Tendermint Core. 

## DoS

In this [document](./docs/dos-attacks.md) I summarize notes and results on DoS attacks to Tendermint. 
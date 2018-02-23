# DoS with [Tendermint Evil 'NoProposals'](https://github.com/MarcoFavorito/tendermint/releases/tag/v0.12.1.3)

## Introduction
In this document I'll report and describe the logs of the execution of the following command:
    
    python3 ethermint-dos.py 4 2 --tendermint_evil 'noproposals' --verbosity 1 --save-logs
    
I.e. a Tendermint network of 4 nodes with 2 byzantine nodes of type ['NoProposals'](https://github.com/MarcoFavorito/tendermint/releases/tag/v0.12.1.3).

## What happens
The algorithm proceeds as always, but when it is the turn of the byzantines to propose a new block, they simply do not send anything, no blocks and no proposal message. The round is skipped and when a correct node becomes proposer, the algorithm works correctly (because the other 2 byzantine nodes take part to the algorithm i.e. send Prevotes and Precommit).

## The Network
In this experiment, the network is composed as the following:
- Node 1 is correct;
- Node 2 is correct;
- Node 3 is byzantine;
- Node 4 is byzantine;

## Logs description
[Here](../res/demo-dos-noproposals) you can find the logs of the activity of the network configured as described above.

We'll see in detail each step of some blocks validation.

### Height=1

#### Height=1 Round=0
#### Height=1 Round=1

### Height=2
#### Height=2 Round=0

### Height=3
#### Height=3 Round=0

### Height=4
#### Height=4 Round=0
#### Height=4 Round=1
#### Height=4 Round=2

### Height=5
#### Height=5 Round=0
#### Height=5 Round=1

### Height=6
#### Height=6 Round=0
### Height=7
#### Height=7 Round=0




 

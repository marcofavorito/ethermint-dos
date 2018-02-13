In this document I try to make the same analysis described [here](https://eprints.soton.ac.uk/415083/2/itasec18_main.pdf) on Tendermint/Ethermint, i.e.:

1. Classify the Tendermint consensus algorithm according to the CAP theorem
2. Performance Analysis
3. Feasible attacks and protocol vulnerabilities;
4. DoS client


## 1) Tendermint and the CAP theorem

Now we briefly sumarize what the CAP properties (namely, Consistency, Availability and Partition Tolerance) mean in blockchain applications:

- _Consistency_: A blockchain achieves consistency when forks are avoided.
- _Availability_:A blockchain is available if transactions submitted by clients are served and even-
tually committed, i.e.  permanently added to the chain.
- _Partition Tolerance_: When a network partition occurs,  Tendermint validators are divided into disjoint groups in such a way that nodes in different groups cannot communicate each other.

Since a blockchain must tolerate partitions, hence CA option is not considered, we analyse the algorithms with respect to CP and AP options. 

### Tendermint: Consistent or Available?
In this section we will see that the Tendermint system guarantees consistency in spite of availability (which is not surprising since Tendermint consensus algorithm is a PBFT-based algorithm).

We'll examine the working assumptions and their implications on the protocol properties.

#### Consistency
As stated in [1]:
> A block is considered committed when a 2/3 majority of validators sign commit votes for that block. A fork occurs when two blocks at the same height are each signed by a 2/3 majority of validators. By simple arithmetic, a fork can only happen when at least a 1/3 majority of validators signs duplicitously. 
>
Hence, as long as there exists a majority of honest validators, in terms of their voting power, no forks can happen (see [Assumption 3](tendermint-summary.md#working-assumptions))

More formally, Tendermint ensures _Safety_ ([1] 6.3) and _Liveness_ ([1] 6.4) properties as long as ![](https://latex.codecogs.com/gif.latex?N\ge3f&plus;1). 

__NOTICE__: numbers in the inequality must be intended in terms of _voting power_ and **not** in terms of _number of nodes_.

This property underlines the similarities with PBFT, more precisely on the optimal resiliency (see Section 3 "Service Properties" in [4]).

Details:
> __Safety property__: If there are less than 1/3 in Byzantine voting power and at least one good validator decides on a block B, then no good validator will decide on any block other than B.
> __Liveness Property__: If there are less than 1/3 in Byzantine voting power then this protocol does not deadlock.

The differences with PBFT are (see 10.2.4 "PBF" in [2]):
- No fixed primary node: the proposer changes every blocks;
- The  use  of blocks  allows  Tendermint  to  include  the  set  of pre-commit messages  from one block in the next block, removing the need for an explicit commit message.
- Accountability guarantees when forks or some bad behaviors happen (3.5 [2]).


The [Assumption 2](tendermint-summary.md#working-assumptions) is needed in order to ensure that eventually the consensus procedure at a certain height is completed. 
Key statements to see this are:
- Each round is longer than the previous round by a small fixed increment of time. This allows the network to eventually achieve consensus in a partially synchronous network (6.2 [1]);
- The asynchronous and local nature of `CommitTime` allows the network to maintain consensus despite drifting clocks, as long as the clocks remain accurate enough during the consensus process of a given height (6.2 [1]);

In other words, there is no need of global time synchronization, but the drift has to be bounded to allow the timeout mechanism to work. Eventually, the timeouts become big enough to allow the messages to be delivered in time for an enough number of nodes.
Clocks do not need to be synced across validators, as they are reset each time a validator observes votes from two-thirds or more others.

Remember that timeouts come into play in several phases of the algorithm, as exit conditions [3]:
- `Propose` step: after `timeoutProposeR` after entering `Propose`;
- `Prevote` step: after `timeoutPrevote` after receiving any +2/3 prevotes;
- `Precommit` step: after `timeoutPrecommit` after receiving any +2/3 precommits;
- `NewHeight` step: Set `StartTime = CommitTime+timeoutCommit` and wait until `StartTime` to receive straggler commits.

#### Availability

When the [Assumption 1](tendermint-summary.md#working-assumptions) fails, no consensus is possible. This result is known as the FLP impossibility result [6].

Indeed, as stated in [2] (3.2 Consensus):
> After the proposal, rounds proceed in a fully asynchronous manner - a
validator makes progress only after hearing from at least two-thirds of the
other validators.  This relieves any sort of dependence on synchronized clocks
or  bounded  network  delays,  but  implies  that  the  network  will  halt  if  one-
third or more of the validators become unresponsive
>

#### Conclusion
When the assumption on the network fails, consistency is preserved while availability is given up. Hence Tendermint can be classified as CP system, according to the CAP theorem.

The below picture summarizes the message passing schema:

![](../res/tendermint-messages.png)

[Here](demo-consensus.md) you can find description of logs of a Tendermint network to prove the depitched behavior.

## 2) Performance analysis

### How to
The following instructions require `tsung` to be installed.
- [Official website](http://tsung.erlang-projects.org/)
- [useful post on Tsung](https://engineering.helpshift.com/2014/tsung/)

In one terminal, run:

    python3 ethermint-dos.py 4 --dummy --no-docker
    
In another terminal, run:

    tsung -f bench/dummy/dummy.xml start

It prompts you a `ssh-askpass`. The session is associated to a log directory number (something like `20180202-2241`)

If you want to see progresses, run:

     tail -f $HOME.tsung/log/LOG_DIRECTORY/tsung.log 

where `$LOG_DIRECTORY` is the number shown before.

Once the execution ends, type:

    rm output -Rf
    mkdir output && cd output
    /usr/lib/tsung/bin/tsung_stats.pl --stats $HOME/.tsung/log/$LOG_DIRECTORY/tsung.log
    firefox graph.html
    
Replace `firefox` with your favorite browser.
    
### Results

You can execute the load test by yourself, or see the result of a test that I've executed, saved in [`res/loadtests_results`](../res/loadtests_results).

For example, given a zip file called `data.zip`:

    open_test_results.sh data.zip



## 3) Feasible attacks and protocol vulnerabilities;
TODO

## 4) DoS client

Please refer to this [demo](demo-dos.md) for the details.


## References
- [[1] Tendermint: Consensus without Mining](https://tendermint.com/static/docs/tendermint.pdf)
- [[2] Tendermint:  Byzantine Fault Tolerance in the Age of Blockchains](https://allquantor.at/blockchainbib/pdf/buchman2016tendermint.pdf)
- [[3] Tendermint Read the Docs](http://tendermint.readthedocs.io/projects/tools/en/master/index.html#)]
- [[4] Practical Byzantine Fault Tolerance](http://pmg.csail.mit.edu/papers/osdi99.pdf)
- [[5] Consensus in the presence of Partial Synchrony](https://groups.csail.mit.edu/tds/papers/Lynch/jacm88.pdf)
- [[6] Impossibility of Distributed Consensus with One Faulty Process](https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf)
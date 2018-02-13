# DoS Attacks
Here I explain in detail what are the effects of my [Tendermint Evil versions](tendermint-evil-versions.md) on the consensus algorithm.

You can set up a Tendermint network with the relative Tendermint Evil version with the following command:

    python3 ethermint-dos.py 4 1 --dummy --verbosity 1 --tendermint_evil <version-name>
        
## [Tendermint Silent](tendermint-evil-versions.md#tendermint-'silent')

Since no message is sent into the network from the byzantine node, the only step when __every__ correct node waits messages from it is the Propose step when the designated proposer is the byzantine node.

This implies that `timeoutProposeR` expires and the algorithm proceed quickly to the other phases in order to start a new round.

More precisely, every correct node, when does not receive the proposal from the byzantine node, does the following:
- In Propose, after `timeoutProposeR` after entering Propose. –> goto Prevote(H,R)
- In Prevote, if the proposal is invalid or wasn’t received on time, it prevotes <nil>.
- Still in Prevote, after +2/3 prevotes for a particular block or <nil>. –> goto Precommit(H,R)
- Upon entering Precommit, each validator broadcasts its precommit vote. Since no valid PoLC is received (no proposal is made), and get 2/3 of prevotes to nil or `timeoutPrecommit` expires, the node precommits nil.
- after receiving 2/3 of precommits for nil, goes to Propose(H, R+1) (i.e. to a new round.)

At round `R+1` a correct node is designated as proposer, hence the algorithm proceeds correctly.

The fixed delay is `timeoutProposeR`; other delays might depends on the network status.

Notice: this version does not send neither heartbeat messages to the other peers. This means that eventually the connections with the byzantine node are ignored by the other correct nodes, and hence the byzantine node is excluded from the protocol. Eventually, the introduced delay (as described before) is deleted. 


## [Tendermint Shy](tendermint-evil-versions.md#tendermint-'shy')

This version is a bit smarter: it sends heartbeat messages but does not send proposals, blocks and votes.

In this way the other peers keep the connections and the byzantine node is not excluded, implying that the consensus algorithm is periodically delayed whenever the byzantine node is chosen as proposer.  

## Notes
How a (byzantine) node can affect the consensus phase?
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
> - During the Propose step all nodes gossip the proposal to their neighboring peers (see [PartSet](https://tendermint.readthedocs.io/en/master/specification/block-structure.html#partset))


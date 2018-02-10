# Tendermint Evil versions

## Tendermint 'Silent'

[Link to the release](https://github.com/MarcoFavorito/tendermint/releases/tag/v0.12.1.1)

This version of "Tendermint Evil" has no [`Send`](https://github.com/MarcoFavorito/tendermint/blob/b5f130ccab1260f6291466ed639651f8747f87e7/p2p/connection.go#L222) and [`TrySend`](https://github.com/MarcoFavorito/tendermint/blob/b5f130ccab1260f6291466ed639651f8747f87e7/p2p/connection.go#L255) functions to send bytes into the network.

modified files:
- `p2p/connection.go`
- `p2p/peer.go` (only for logging purposes)

This version causes a network partition since no message passes through/from/to the byzantine node.

## Tendermint 'Shy'


[Link to the release](https://github.com/MarcoFavorito/tendermint/releases/tag/v0.12.1.2)

The byzantine node is not absolutely isolated as the previous case, but just do not sends any block, proposals and votes. It still sends heartbeat messages to keep the connections with other peers (and so receiving updates about the blockchain).

[Link to the changes](https://github.com/MarcoFavorito/tendermint/commit/3aca496199870fe65b28605eff54d3073c4c1d96).

The main purposes are:
- Weaken the network: another node failure blocks the consensus algorithm (no enough voting power to commit blocks);
- Delay the commit phase: when at some height the byzantine node becomes the proposer, the algorithm is delayed about the [`timeoutProposeR`](https://tendermint.readthedocs.io/en/master/specification/byzantine-consensus-algorithm.html#propose-step-height-h-round-r) since no proposal is made. After the timeout, the round-robin algorithm select another node, and the algorithm moves to a new round (but same height).
  
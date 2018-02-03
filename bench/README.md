Here you will find scripts for benchmarking various configurations of Tendermint networks.

Requirements are:
- the ones for `ethermint-dos.py` (see the main README.md);
- `tsung` (look [here](../docs/report.md#how-to))

## Dummy Example

After the correct installation, you might find useful `dummy/tsung_dummy_bench.sh`.
It executes a load test on:
- a Tendermint network of 4 nodes;
- a Tendermint network of 4 nodes, in which one of them is byzantine (in our case, it simply does not participate to the consensus protocol);

From the root directory, run:

    ./bench/dummy/tsung_dummy_bench.sh
    
It takes approximately five minutes. The execution consists of:
1. Set up of a "good" network;
2. Load test on it;
3. Set up of a "evil" network;
4. Load test on it;
5. Plot comparison

Each load test session, for now, is composed as follows (see `dummy/dummy.xml`):
- Phase 1: 30 seconds, connection rate: 25 user per second
- Phase 2:  1 minute,  connection rate: 100 user per second
- Phase 3:  1 minute,  connection rate: 250 user per second

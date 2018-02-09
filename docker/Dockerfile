FROM ubuntu:16.04

RUN apt-get update && apt-get upgrade -y

ADD ./bin/tendermint_evil   /bin/tendermint_evil
ADD ./bin/tendermint        /bin/tendermint
ADD ./bin/ethermint         /bin/ethermint

ENV DATA_ROOT_ETHERMINT /root/ethermint
ARG NUM_NODES=4

WORKDIR /root/

# p2p port
EXPOSE 46656
# rpc port
EXPOSE 46657
# abci port
EXPOSE 46658

RUN mkdir $DATA_ROOT_ETHERMINT
ADD ./docker/genesis.json /root/genesis.json
RUN tendermint testnet --n $NUM_NODES
RUN ethermint --datadir $DATA_ROOT_ETHERMINT init
#/root/genesis.json

WORKDIR /




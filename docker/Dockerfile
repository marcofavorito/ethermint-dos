FROM ubuntu:16.04

RUN apt-get update && apt-get upgrade -y

ARG NUM_NODES=4
ENV DATA_ROOT_ETHERMINT /root/ethermint

ADD ./bin/   /bin/
ADD ./res/genesis.json /root/genesis.json
ADD ./res/keystore /root/keystore
ADD ./res/accounts.csv /root/accounts.csv
ADD ./res/password.txt /root/password.txt


# p2p port
EXPOSE 46656
# rpc port
EXPOSE 46657
# abci port
EXPOSE 46658

########
# setup
########

WORKDIR /root/

#tendermint
RUN tendermint testnet --n $NUM_NODES
RUN tendermint --home .tendermint init

#ethermint
RUN mkdir $DATA_ROOT_ETHERMINT
#RUN ethermint --datadir $DATA_ROOT_ETHERMINT init
RUN ethermint --datadir $DATA_ROOT_ETHERMINT init genesis.json
RUN rm -R $DATA_ROOT_ETHERMINT/keystore -R
RUN mv keystore $DATA_ROOT_ETHERMINT/keystore

WORKDIR /




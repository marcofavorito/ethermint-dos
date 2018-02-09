FROM ubuntu:16.04


# Grab deps (jq, hexdump, xxd, killall)
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y apt-utils jq bsdmainutils vim-common psmisc netcat curl software-properties-common

RUN add-apt-repository ppa:longsleep/golang-backports
RUN apt-get update
RUN apt-get install -y golang-go

RUN apt-get install -y git

RUN add-apt-repository ppa:masterminds/glide && apt-get update
RUN apt-get install glide

RUN mkdir -p /root/gopath
ENV GOPATH /root/gopath
RUN go get github.com/tendermint/tendermint; exit 0
ENV REPO $GOPATH/src/github.com/tendermint/tendermint/

ENV PATH $PATH:$GOPATH/bin

WORKDIR $REPO

RUN git checkout v0.12.1
RUN make get_vendor_deps
RUN make install
RUN go install ./cmd/tendermint


WORKDIR /root/

# p2p port
EXPOSE 46656
# rpc port
EXPOSE 46657

RUN mkdir .tendermint
RUN tendermint --home .tendermint init

RUN tendermint testnet
#CMD tendermint node proxy_app dummy




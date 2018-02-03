#!/usr/bin/env bash

TENDERMINT_VERSION="0.12.1"
TENDERMINT_EVIL_VERSION="0.12.1"
ETHERMINT_VERSION="0.5.3"

echo "Getting Tendermint..."
#curl -OL https://github.com/tendermint/tendermint/releases/download/v$TENDERMINT_VERSION/tendermint_${TENDERMINT_VERSION}_linux_amd64.zip
#unzip -o tendermint_${TENDERMINT_VERSION}_linux_amd64.zip -d bin/
curl -OL https://github.com/tendermint/tendermint/releases/download/v$TENDERMINT_VERSION/linux_amd64.zip
unzip -o linux_amd64.zip -d bin/


echo "Getting Tendermint Evil..."
curl -OL https://github.com/MarcoFavorito/tendermint/releases/download/v${TENDERMINT_EVIL_VERSION}/tendermint.zip
unzip tendermint.zip
mv tendermint bin/tendermint_evil

echo "Getting Ethermint..."
curl -OL https://github.com/tendermint/ethermint/releases/download/v${ETHERMINT_VERSION}/ethermint_${ETHERMINT_VERSION}_linux-amd64.zip
unzip -o ethermint_${ETHERMINT_VERSION}_linux-amd64.zip -d bin/

rm *.zip
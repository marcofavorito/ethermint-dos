#!/usr/bin/env bash

TENDERMINT_VERSION="0.12.1"
TENDERMINT_EVIL_SILENT_VERSION="0.12.1.1"
TENDERMINT_EVIL_SHY_VERSION="0.12.1.2"
ETHERMINT_VERSION="0.5.3"

rm bin/*

echo "Getting Tendermint..."
#curl -OL https://github.com/tendermint/tendermint/releases/download/v$TENDERMINT_VERSION/tendermint_${TENDERMINT_VERSION}_linux_amd64.zip
#unzip -o tendermint_${TENDERMINT_VERSION}_linux_amd64.zip -d bin/
curl -OL https://github.com/tendermint/tendermint/releases/download/v$TENDERMINT_VERSION/linux_amd64.zip
unzip -o linux_amd64.zip -d bin/


echo "Getting Tendermint Evil Silent..."
curl -OL https://github.com/MarcoFavorito/tendermint/releases/download/v${TENDERMINT_EVIL_SILENT_VERSION}/tendermint.zip
unzip -o tendermint.zip -d bin/

echo "Getting Tendermint Evil Shy..."
curl -OL https://github.com/MarcoFavorito/tendermint/releases/download/v${TENDERMINT_EVIL_SHY_VERSION}/tendermint.zip
unzip -o tendermint.zip -d bin/

echo "Getting Ethermint..."
curl -OL https://github.com/tendermint/ethermint/releases/download/v${ETHERMINT_VERSION}/ethermint_${ETHERMINT_VERSION}_linux-amd64.zip
unzip -o ethermint_${ETHERMINT_VERSION}_linux-amd64.zip -d bin/
#curl -OL https://github.com/MarcoFavorito/ethermint/releases/download/ethermint_broadcast_tx_commit/ethermint.zip
#unzip -o ethermint.zip -d bin/
rm *.zip

ln -s tendermint_shy bin/tendermint_evil
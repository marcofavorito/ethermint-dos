#!/usr/bin/env bash

echo "Getting Tendermint..."
curl -OL https://github.com/tendermint/tendermint/releases/download/v0.14.0/tendermint_0.14.0_linux_amd64.zip
unzip -o tendermint_0.14.0_linux_amd64.zip -d bin/

echo "Getting Tendermint Evil..."
curl -OL https://github.com/MarcoFavorito/tendermint/releases/download/v0.14.0/tendermint.zip
unzip tendermint.zip
mv tendermint bin/tendermint_evil

echo "Getting Ethermint..."
curl -OL https://github.com/tendermint/ethermint/releases/download/v0.5.3/ethermint_0.5.3_linux-amd64.zip
unzip -o ethermint_0.5.3_linux-amd64.zip -d bin/

rm *.zip
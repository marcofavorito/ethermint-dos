#!/usr/bin/env bash

curl -OL https://github.com/tendermint/tendermint/releases/download/v0.14.0/tendermint_0.14.0_linux_amd64.zip
unzip -o tendermint_0.14.0_linux_amd64.zip -d bin/

curl -OL https://github.com/MarcoFavorito/tendermint/releases/download/v0.14.0/tendermint.zip
unzip tendermint.zip
mv tendermint bin/tendermint_evil

rm *.zip
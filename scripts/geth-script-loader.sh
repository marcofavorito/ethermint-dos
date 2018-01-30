#!/usr/bin/env bash

ETHERMINT_ENDPOINT=$1
SCRIPT_PATH=$2

geth attach $ETHERMINT_ENDPOINT << EOF
loadScript("$2");
EOF

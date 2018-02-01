#!/usr/bin/env bash

#older version:
#ETHERMINT_ENDPOINT=$1
#SCRIPT_PATH=$2
#geth  attach $ETHERMINT_ENDPOINT << EOF
#loadScript("$SCRIPT_PATH");
#EOF

ETHERMINT_DATADIR=$1
SCRIPT_PATH=$2
TEST_TX_NUM=$3
echo "geth --datadir $ETHERMINT_DATADIR attach --preload \"$SCRIPT_PATH\" --exec 'main($TEST_TX_NUM)'"
geth --datadir $ETHERMINT_DATADIR attach --preload $SCRIPT_PATH --exec "main($TEST_TX_NUM)"


#!/usr/bin/env bash

WORKING_DIR=./bench/dummy_dockerized
TSUNG_CONFIG_FILE=$WORKING_DIR/dummy_dockerized.xml

rm -R $WORKING_DIR/normal $WORKING_DIR/evil $WORKING_DIR/graphs
mkdir $WORKING_DIR/normal $WORKING_DIR/evil $WORKING_DIR/graphs

echo "***********************************************"
echo "Test normal network (where all nodes are correct)"
./scripts/tsung_test.sh $TSUNG_CONFIG_FILE  $WORKING_DIR/normal    "python3 ethermint-dos.py 4 0 --dummy --verbosity 1"

for pid in $(ps -ef | grep "tendermint" | awk '{print $2}'); do sudo kill -9 $pid; done
docker rm -f $(docker ps -a --filter name="local_testnet" -q)

echo "***********************************************"
echo "Test evil network (with one byzantine node)"
./scripts/tsung_test.sh $TSUNG_CONFIG_FILE  $WORKING_DIR/evil      "python3 ethermint-dos.py 4 1 --dummy --verbosity 1"

for pid in $(ps -ef | grep "tendermint" | awk '{print $2}'); do sudo kill -9 $pid; done
docker rm -f $(docker ps -a --filter name="local_testnet" -q)


LAST_LOG_DIR_NORM=$(ls $WORKING_DIR/normal/log/| grep -o -E "[0-9]{8}-[0-9]{4}" | tail -1)
LAST_LOG_DIR_EVIL=$(ls $WORKING_DIR/evil/log/| grep -o -E "[0-9]{8}-[0-9]{4}" | tail -1)

echo "***********************************************"

tsplot "Normal" $WORKING_DIR/normal/log/$LAST_LOG_DIR_NORM/tsung.log "Evil" $WORKING_DIR/evil/log/$LAST_LOG_DIR_EVIL/tsung.log -d $WORKING_DIR/graphs
cd $WORKING_DIR/graphs/
find . ! -name '*_tn.png'  | xargs firefox
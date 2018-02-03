#!/usr/bin/env bash

TSUNG_CONFIG_FILE=./bench/dummy/dummy.xml

for pid in $(ps -ef | grep "tendermint" | awk '{print $2}'); do sudo kill -9 $pid; done

echo "***********************************************"
echo "Test normal network (where all nodes are correct)"
./bench/dummy/tsung_dummy_test.sh $TSUNG_CONFIG_FILE  ./bench/dummy/normal    "python3 ethermint-dos.py 4 0 --dummy --verbosity 1"
for pid in $(ps -ef | grep "tendermint" | awk '{print $2}'); do sudo kill -9 $pid; done

echo "***********************************************"
echo "Test evil network (with one byzantine node)"
./bench/dummy/tsung_dummy_test.sh   $TSUNG_CONFIG_FILE  ./bench/dummy/evil      "python3 ethermint-dos.py 4 1 --dummy --verbosity 1"
for pid in $(ps -ef | grep "tendermint" | awk '{print $2}'); do sudo kill -9 $pid; done

LAST_LOG_DIR_NORM=$(ls bench/dummy/normal/log/| grep -o -E "[0-9]{8}-[0-9]{4}" | tail -1)
LAST_LOG_DIR_EVIL=$(ls bench/dummy/evil/log/| grep -o -E "[0-9]{8}-[0-9]{4}" | tail -1)

echo "***********************************************"

tsplot "Normal" ./bench/dummy/normal/log/$LAST_LOG_DIR_NORM/tsung.log "Evil" ./bench/dummy/evil/log/$LAST_LOG_DIR_EVIL/tsung.log -d bench/dummy/graphs
cd bench/dummy/graphs/
find . ! -name '*_tn.png'  | xargs firefox
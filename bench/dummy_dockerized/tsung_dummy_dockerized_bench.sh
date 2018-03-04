#!/usr/bin/env bash

WORKING_DIR=./bench/dummy_dockerized
TSUNG_CONFIG_FILE=$WORKING_DIR/dummy_dockerized.xml

rm -R $WORKING_DIR/normal $WORKING_DIR/evil $WORKING_DIR/graphs
mkdir $WORKING_DIR/normal $WORKING_DIR/evil $WORKING_DIR/graphs

WORKING_DIR_NORMAL=${WORKING_DIR}/normal
WORKING_DIR_EVIL_1=${WORKING_DIR}/evil_1
WORKING_DIR_EVIL_2=${WORKING_DIR}/evil_2


rm -R $WORKING_DIR_NORMAL $WORKING_DIR_EVIL_1 $WORKING_DIR_EVIL_2 $WORKING_DIR/graphs
mkdir $WORKING_DIR_NORMAL $WORKING_DIR_EVIL_1 $WORKING_DIR_EVIL_2 $WORKING_DIR/graphs
docker rm -f $(docker ps -a --filter name="local_testnet" -q)
docker build -t marcofavorito/ethermint-dos -f ./docker/Dockerfile .

echo "***********************************************"
echo "Test normal network where every node of 4 are correct (f = 0)"
./scripts/tsung_test.sh $TSUNG_CONFIG_FILE  ${WORKING_DIR_NORMAL}       "python3 ethermint-dos.py 4 0 --dummy --verbosity 1 "

docker rm -f $(docker ps -a --filter name="local_testnet" -q)

echo "***********************************************"
echo "Test evil network with one byzantine node of 4 (f < N/3)"
./scripts/tsung_test.sh $TSUNG_CONFIG_FILE  ${WORKING_DIR_EVIL_1}      "python3 ethermint-dos.py 4 1  --dummy --verbosity 1 "

docker rm -f $(docker ps -a --filter name="local_testnet" -q)

echo "***********************************************"
echo "Test evil network with two byzantine nodes of 4 (f >= N/3)"
./scripts/tsung_test.sh $TSUNG_CONFIG_FILE  ${WORKING_DIR_EVIL_2}      "python3 ethermint-dos.py 4 2  --dummy --verbosity 1 "

docker rm -f $(docker ps -a --filter name="local_testnet" -q)



  LAST_LOG_DIR_NORM=$(ls ${WORKING_DIR_NORMAL}/log/| grep -o -E "[0-9]{8}-[0-9]{4}" | tail -1)
LAST_LOG_DIR_EVIL_1=$(ls ${WORKING_DIR_EVIL_1}/log/| grep -o -E "[0-9]{8}-[0-9]{4}" | tail -1)
LAST_LOG_DIR_EVIL_2=$(ls ${WORKING_DIR_EVIL_2}/log/| grep -o -E "[0-9]{8}-[0-9]{4}" | tail -1)

echo "***********************************************"

tsplot "Normal" $WORKING_DIR_NORMAL/log/$LAST_LOG_DIR_NORM/tsung.log "Evil f<N/3" $WORKING_DIR_EVIL_1/log/$LAST_LOG_DIR_EVIL_1/tsung.log "Evil f>=N/3" $WORKING_DIR_EVIL_2/log/$LAST_LOG_DIR_EVIL_2/tsung.log -d $WORKING_DIR/graphs
cd $WORKING_DIR/graphs/
find . ! -name '*_tn.png'  | xargs firefox

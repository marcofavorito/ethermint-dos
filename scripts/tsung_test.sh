#!/usr/bin/env bash

TSUNG_CONFIG_FILE=$1
OUTPUT_DIR=$2
CMD=$3
ETHERMINT_FLAG=$4

gnome-terminal -e "$CMD"
echo "Wait 15 seconds..."
sleep 15

if [ -n "$ETHERMINT_FLAG" ]
then python3 ./scripts/ethermint_app_setup.py "http://172.57.101.100:8545"; sleep 5;
fi


tsung -f $TSUNG_CONFIG_FILE -l $OUTPUT_DIR/log start | tee tsung.temp
LOG_DIRECTORY=$(grep "Log directory" tsung.temp | cut -d ':' -f 2)
rm tsung.temp

cd $OUTPUT_DIR
/usr/lib/tsung/bin/tsung_stats.pl --stats $LOG_DIRECTORY/tsung.log

firefox $(pwd)/graph.html &

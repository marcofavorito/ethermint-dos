#!/usr/bin/env bash

TSUNG_CONFIG_FILE=$1
OUTPUT_DIR=$2
CMD=$3

gnome-terminal -e "$CMD"
echo "Wait a few seconds..."
sleep 5
tsung -f $TSUNG_CONFIG_FILE -l $OUTPUT_DIR/log start | tee tsung.temp
LOG_DIRECTORY=$(grep "Log directory" tsung.temp | cut -d ':' -f 2)
rm tsung.temp

cd $OUTPUT_DIR
/usr/lib/tsung/bin/tsung_stats.pl --stats $LOG_DIRECTORY/tsung.log

firefox $(pwd)/graph.html

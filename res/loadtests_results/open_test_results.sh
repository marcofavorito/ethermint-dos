#!/usr/bin/env bash

filename=$(basename "$1")
extension="${filename##*.}"
filename="${filename%.*}"

unzip -o $1 -d $filename
cd $filename/graphs
find . ! -name '*_tn.png'  | xargs firefox &
cd ../
firefox $(pwd)/evil/graph.html $(pwd)//normal/graph.html &

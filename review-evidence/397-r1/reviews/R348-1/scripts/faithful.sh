#!/bin/bash
# Faithful reproduction at the exact head: build, run populated scenarios as published.
# usage: faithful.sh <repo> <scratch> ; writes <scratch>/faithful-*.out
set -u
REPO=$1; S=$2
. "$(dirname "$0")/env.sh"
cd "$REPO"
for shape in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
  d=$S/build-$shape
  /usr/bin/time -v python -B tb/verilator/fw_service_budget/run.py --shape $shape --build-dir $d --build-only > $S/faithful-build-$shape.out 2>&1
  echo "build $shape rc=$?" >> $S/faithful-status.txt
done
python -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_1x1_tdm8 --build-dir $S/build-endstation_ax7101_1x1_tdm8 --reuse-build --populated > $S/faithful-run-1x1.out 2>&1 &
p1=$!
python -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_8x8 --build-dir $S/build-endstation_ax7101_8x8 --reuse-build --populated --device-wait-us 1000 --record-budget-findings > $S/faithful-run-8x8.out 2>&1 &
p2=$!
wait $p1; echo "run 1x1 rc=$?" >> $S/faithful-status.txt
wait $p2; echo "run 8x8 rc=$?" >> $S/faithful-status.txt
echo DONE >> $S/faithful-status.txt

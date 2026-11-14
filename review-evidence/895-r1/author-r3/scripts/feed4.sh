#!/bin/bash
# Round 3 (lane 895): as round 2's feed3.sh on the legs S-* at the head the clone r3/S holds: arm A's merged parts
# viewed as one leg, every leg's measured costs by round 1's parsers (S2b's, unchanged), the load gate's tables as
# tables895.py feeds them (printed, not committed), and the least margins. usage: feed4.sh OUT
set -u
O=$1
T=/data-2/milan/tmp/895-a775
L=$T/r3/S
S=$MANAGEMENT/2026-09-23/895-a775/scripts
. $S/env.sh
mkdir -p "$O"
for p in 1 8; do
  v=$T/builds/S-A$p-view; mkdir -p $v
  ln -sfn $T/builds/S-A$p/build.json $v/build.json; ln -sfn $T/builds/S-A$p/results-all $v/results
done
bash $S/costs/costs.sh "$O/G1" 1x1/1if 1 $L/tb/verilator/ctrl_service_budget $T/builds/S-A1-view $T/builds/S-N1 \
  $T/builds/S-W1 $T/builds/S-B1 > "$O/costs-G1.log" 2>&1; echo "costs G1 rc $?" >> "$O/feed.txt"
bash $S/costs/costs.sh "$O/G8" 8x8/2if 2 $L/tb/verilator/ctrl_service_budget $T/builds/S-A8-view $T/builds/S-N8 \
  $T/builds/S-W8 $T/builds/S-B8 > "$O/costs-G8.log" 2>&1; echo "costs G8 rc $?" >> "$O/feed.txt"
python3 -I $S/costs/tables895.py $L "$O" > "$O/tables.txt" 2>&1; echo "tables rc $?" >> "$O/feed.txt"
python3 -I $S/costs/least_margin.py $T/builds/S-A1/results-all/results.json $T/builds/S-A8/results-all/results.json \
  $T/builds/S-N1/results/results.json $T/builds/S-N8/results/results.json $T/builds/S-W1/results/results.json \
  $T/builds/S-W8/results/results.json $T/builds/S-B1/results/results.json $T/builds/S-B8/results/results.json \
  > "$O/least-margin.txt" 2>&1
cat "$O/feed.txt"

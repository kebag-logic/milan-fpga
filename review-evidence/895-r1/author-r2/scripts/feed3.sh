#!/bin/bash
# Round 2 (lane 895): merge arm A's parts at both points and regrade them, view them as one leg, read every leg's
# measured costs by round 1's parsers (S2b's, unchanged) and feed the load gate's tables (tables895.py).
# usage: feed.sh OUT   (the legs are builds/R3-*; the clone is r2/L at the legs' commit)
set -u
O=$1
T=/data-2/milan/tmp/895-a775
L=$T/r2/L2
S=$MANAGEMENT/2026-09-23/895-a775/scripts
. $S/env.sh
mkdir -p "$O"
for p in 1 8; do
  pt=$([ $p = 1 ] && echo 1x1 || echo 8x8)
  if ! grep -q "regrade rc=0" "$O/mergeA$p.txt" 2>/dev/null; then
    python3 -B $S/merge.py R3-A$p $pt $L > "$O/mergeA$p.txt" 2>&1; echo "merge A$p rc $?" >> "$O/feed.txt"
  fi
  v=$T/builds/R3-A$p-view; mkdir -p $v
  ln -sfn $T/builds/R3-A$p/build.json $v/build.json; ln -sfn $T/builds/R3-A$p/results-all $v/results
done
bash $S/costs/costs.sh "$O/G1" 1x1/1if 1 $L/tb/verilator/ctrl_service_budget $T/builds/R3-A1-view $T/builds/R3-N1 \
  $T/builds/R3-W1 $T/builds/R3-B1 > "$O/costs-G1.log" 2>&1; echo "costs G1 rc $?" >> "$O/feed.txt"
bash $S/costs/costs.sh "$O/G8" 8x8/2if 2 $L/tb/verilator/ctrl_service_budget $T/builds/R3-A8-view $T/builds/R3-N8 \
  $T/builds/R3-W8 $T/builds/R3-B8 > "$O/costs-G8.log" 2>&1; echo "costs G8 rc $?" >> "$O/feed.txt"
python3 -I $S/costs/tables895.py $L "$O" > "$O/tables.txt" 2>&1; echo "tables rc $?" >> "$O/feed.txt"
python3 -I $S/costs/least_margin.py $T/builds/R3-A1/results-all/results.json $T/builds/R3-A8/results-all/results.json \
  $T/builds/R3-N1/results/results.json $T/builds/R3-N8/results/results.json $T/builds/R3-W1/results/results.json \
  $T/builds/R3-W8/results/results.json $T/builds/R3-B1/results/results.json $T/builds/R3-B8/results/results.json \
  > "$O/least-margin.txt" 2>&1
cat "$O/feed.txt"

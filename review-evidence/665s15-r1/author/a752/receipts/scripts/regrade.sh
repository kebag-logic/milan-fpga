#!/bin/bash
# Merge a split gate leg's parts (each group's script and log) and grade every group at once on the same build and
# clone, as one run's verdict. usage: regrade.sh NAME POINT NPARTS
set -u
NAME=$1 POINT=$2 N=$3
T=<scratch>
. $T/scripts/env.sh
C=$T/hleg-wt-$NAME
B=$T/builds/$NAME
M=$B/results-all
mkdir -p "$M"
for k in $(seq 0 $((N - 1))); do cp -n "$B/results-part$k"/*.txt "$B/results-part$k"/*.log "$M/"; done
L=$T/logs/$NAME-regrade.log
echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=no | wc -l) regrade of $N parts" > "$L"
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$B" --reuse-build --regrade \
    --out "$M" --record-budget-findings --record-share-findings >> "$L" 2>&1
echo "rc=$?" >> "$L"
git -C "$C" status --short --untracked-files=all > $T/logs/$NAME-tree-after.txt

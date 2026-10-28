#!/bin/bash
# The harness's as-built control (#791) at 1x1, at the review clone's head: must print
# "CONTROL as-built caught" with rc 0. The build directory is disposable scratch.
. "$(dirname "$0")/env.sh"
B=$PACKET/scratch/builds/asbuilt-1x1; rm -rf "$B"; mkdir -p "$(dirname "$B")"
cd "$CHECKOUT" && echo "HEAD $(git rev-parse HEAD) DIRTY $(git status --porcelain | wc -l)"
start=$(date +%s)
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir "$B" --record-budget-findings \
  --cpu-regions as-built --jobs 4
rc=$?; echo "elapsed=$(( $(date +%s) - start ))s rc=$rc"
echo "tree after: $(git status --porcelain | wc -l) changed path(s)"

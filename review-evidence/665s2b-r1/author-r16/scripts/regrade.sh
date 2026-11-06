#!/bin/bash
# Grade a leg's recorded logs again with a checkout's harness (run.py --regrade), its log and rc kept.
# usage: regrade.sh LEG CHECKOUT TAG GROUPS|all POINT [run.py args]
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683u/scripts/env.sh
T=$VALIDATION_STORAGE/665s2b-a683u
LEG=$1 C=$T/$2 TAG=$3 GROUPS_ARG=$4 POINT=$5; shift 5
g=(); [ "$GROUPS_ARG" != all ] && g=(--groups "$GROUPS_ARG")
start=$(date +%s)
echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=no | wc -l)" > "$T/logs/$LEG-$TAG.log"
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$T/builds/$LEG" --reuse-build \
  --regrade "${g[@]}" --record-budget-findings --record-share-findings "$@" >> "$T/logs/$LEG-$TAG.log" 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s" >> "$T/logs/$LEG-$TAG.log"
echo "rc=$rc" >> "$T/logs/$LEG-$TAG.log"

#!/bin/bash
# One harness leg: build a point and run its groups from a checkout, into a fresh build directory.
# usage: leg.sh CHECKOUT NAME POINT [extra run.py args...]
# Writes $B/NAME (build and results) and $L/NAME.log (driver), with the head, elapsed and rc last.
set -u
. $MANAGEMENT/2026-09-23/665s1-a680k/probes/env.sh
C=$1 NAME=$2 POINT=$3; shift 3
B=$VALIDATION_STORAGE/scratch/665s1-a680k-work/builds
L=$VALIDATION_STORAGE/scratch/665s1-a680k-work/logs
mkdir -p "$B" "$L"
start=$(date +%s)
echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=no | wc -l)" > "$L/$NAME.log"
echo "\$ run.py --point $POINT --build-dir <builds>/$NAME --record-budget-findings $*" >> "$L/$NAME.log"
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$B/$NAME" \
  --record-budget-findings "$@" >> "$L/$NAME.log" 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s" >> "$L/$NAME.log"
echo "rc=$rc" >> "$L/$NAME.log"

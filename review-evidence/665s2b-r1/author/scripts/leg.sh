#!/bin/bash
# One harness leg: build (or reuse) a point and run its groups from a checkout.
# usage: leg.sh CHECKOUT NAME POINT [extra run.py args...]
# Writes $B/NAME (build), $B/NAME/results (logs), $L/NAME.log (driver), with elapsed and rc last.
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683l/scripts/env.sh
C=$1 NAME=$2 POINT=$3; shift 3
B=$VALIDATION_STORAGE/665s2b-a683l/builds
L=$VALIDATION_STORAGE/665s2b-a683l/logs
mkdir -p "$B" "$L"
reuse=()
[ -f "$B/$NAME/build.json" ] && reuse=(--reuse-build)
start=$(date +%s)
echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=no | wc -l)" > "$L/$NAME.log"
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$B/$NAME" \
  "${reuse[@]}" --record-budget-findings "$@" >> "$L/$NAME.log" 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s" >> "$L/$NAME.log"
echo "rc=$rc" >> "$L/$NAME.log"

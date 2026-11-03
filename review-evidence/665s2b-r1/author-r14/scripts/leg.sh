#!/bin/bash
# One harness leg: build (or reuse) a point and run groups from a checkout, every row and pass finding recorded.
# usage: leg.sh CHECKOUT NAME POINT GROUPS|all [extra run.py args]
# Writes $B/NAME (build), $B/NAME/results (logs), $L/NAME.log (driver), with elapsed and rc last.
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683q/scripts/env.sh
C=$1 NAME=$2 POINT=$3 GROUPS_ARG=$4; shift 4
B=$VALIDATION_STORAGE/665s2b-a683q/builds
L=$VALIDATION_STORAGE/665s2b-a683q/logs
mkdir -p "$B" "$L"
reuse=()
[ -f "$B/$NAME/build.json" ] && reuse=(--reuse-build)
g=()
[ "$GROUPS_ARG" != all ] && g=(--groups "$GROUPS_ARG")
start=$(date +%s)
echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=no | wc -l)" > "$L/$NAME.log"
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$B/$NAME" "${reuse[@]}" \
  "${g[@]}" --record-budget-findings --record-share-findings --jobs "${JOBS:-8}" "$@" >> "$L/$NAME.log" 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s" >> "$L/$NAME.log"
echo "rc=$rc" >> "$L/$NAME.log"

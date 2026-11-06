#!/bin/bash
# One harness leg on another leg's build (reused when it exists), its results kept apart: BUILD/results-NAME.
# usage: leg2.sh CHECKOUT NAME BUILD POINT GROUPS [extra run.py args]; writes $L/NAME.log with elapsed and rc last.
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683u/scripts/env.sh
C=$1 NAME=$2 BUILD=$3 POINT=$4 GROUPS_ARG=$5; shift 5
B=$VALIDATION_STORAGE/665s2b-a683u/builds
L=$VALIDATION_STORAGE/665s2b-a683u/logs
reuse=()
[ -f "$B/$BUILD/build.json" ] && reuse=(--reuse-build)
start=$(date +%s)
echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=no | wc -l)" > "$L/$NAME.log"
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$B/$BUILD" "${reuse[@]}" \
  --out "$B/$BUILD/results-$NAME" --groups "$GROUPS_ARG" --record-budget-findings --record-share-findings \
  --jobs "${JOBS:-8}" "$@" >> "$L/$NAME.log" 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s" >> "$L/$NAME.log"
echo "rc=$rc" >> "$L/$NAME.log"

#!/bin/bash
# One harness leg: build (or reuse) a point at one fetch-L1 geometry and run its groups.
# usage: leg.sh CHECKOUT NAME POINT FETCH_L1 [extra run.py args...]
# Writes BUILDS/NAME (build), BUILDS/NAME/results (logs), LOGS/NAME.log (driver), with its rc last.
set -u
. $MANAGEMENT/2026-09-23/665s2c-a685/scripts/env.sh
C=$1 NAME=$2 POINT=$3 GEOM=$4; shift 4
B=$VALIDATION_STORAGE/665s2c-a685/builds
L=$VALIDATION_STORAGE/665s2c-a685/logs
mkdir -p "$L"
reuse=()
[ -f "$B/$NAME/build.json" ] && reuse=(--reuse-build)
start=$(date +%s)
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$B/$NAME" \
  --fetch-l1 "$GEOM" --jobs 8 "${reuse[@]}" "$@" > "$L/$NAME.log" 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s" >> "$L/$NAME.log"
echo "rc=$rc" >> "$L/$NAME.log"

#!/bin/bash
# Bring an arm measured with S2's round-2 scenario to round 3 (f8876638): run the groups round 3
# changed or added on the arm's attested build, then regrade every group with round 3's grader.
# usage: complete_r3.sh CHECKOUT NAME POINT FETCH_L1 GRP [extra run.py args...]
set -u
. $MANAGEMENT/2026-09-23/665s2c-a685/scripts/env.sh
C=$1 NAME=$2 POINT=$3 GEOM=$4 GRP=$5; shift 5
B=$VALIDATION_STORAGE/665s2c-a685/builds/$NAME
L=$VALIDATION_STORAGE/665s2c-a685/logs
H=$C/tb/verilator/ctrl_service_budget/run.py
python3 -B "$H" --point "$POINT" --build-dir "$B" --fetch-l1 "$GEOM" --reuse-build --groups "$GRP" \
  --out "$B/results" --jobs 2 "$@" > "$L/$NAME-r3run.log" 2>&1
echo "rc=$?" >> "$L/$NAME-r3run.log"
python3 -B "$H" --point "$POINT" --build-dir "$B" --fetch-l1 "$GEOM" --regrade --out "$B/results" "$@" \
  > "$L/$NAME-regrade.log" 2>&1
echo "rc=$?" >> "$L/$NAME-regrade.log"

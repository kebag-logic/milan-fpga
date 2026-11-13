#!/bin/bash
# One measurement leg on its own clean clone: every group of the arm at the point (or --groups), one build, one run.
# usage: leg30.sh CLONE NAME POINT JOBS [run.py args]     (logs/NAME.log, its rc in logs/NAME.log.rc)
set -u
C=$1 NAME=$2 POINT=$3 J=$4; shift 4
T=/data-2/milan/tmp/665s2b-a683zo
. $T/scripts/env.sh
B=$T/builds/$NAME L=$T/logs/$NAME.log
export MAKEFLAGS="-j12 --no-print-directory" PYTHONUNBUFFERED=1 TMPDIR=$T/tmp/$NAME
mkdir -p "$TMPDIR"
echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=all | wc -l) point $POINT jobs $J args $* start $(date +%T)" > "$L"
start=$(date +%s)
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$B" --jobs "$J" \
    --record-budget-findings --record-share-findings "$@" >> "$L" 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s rc=$rc end $(date +%T)" >> "$L"
git -C "$C" status --porcelain --untracked-files=all > "$T/logs/$NAME-tree-after.txt"
echo $rc > "$L.rc"

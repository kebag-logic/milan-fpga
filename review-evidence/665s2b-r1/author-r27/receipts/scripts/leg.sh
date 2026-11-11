#!/bin/bash
# One leg: a fresh build of a point on a clean clone and a run of the named groups on it.
# usage: leg.sh CLONE NAME POINT GROUPS [run.py args]   (logs/NAME.log, its rc in logs/NAME.log.rc)
set -u
C=$1 NAME=$2 POINT=$3 GROUPS_=$4; shift 4
T=<scratch>
. $T/scripts/env.sh
B=$T/builds/$NAME L=$T/logs/$NAME.log
export TMPDIR=$T/tmp/$NAME MAKEFLAGS="-j8 --no-print-directory" PYTHONUNBUFFERED=1; mkdir -p "$TMPDIR" "$B"
echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=all | wc -l) groups $GROUPS_ args $*" > "$L"
start=$(date +%s)
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$B" --groups "$GROUPS_" \
    --out "$B/results-new" --record-budget-findings --record-share-findings --jobs 4 "$@" >> "$L" 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s rc=$rc" >> "$L"
git -C "$C" status --porcelain --untracked-files=all > "$T/logs/$NAME-tree-after.txt"
echo $rc > "$L.rc"

#!/bin/bash
# One harness point on a clean clone: build, then every group, each timed with peak memory; rc files written last.
# usage: hleg.sh CLONE POINT SHAPE N_IF OUT [run options...]
set -u
C=$1 PT=$2 SHAPE=$3 N=$4 O=$5; shift 5
. "$(dirname "$0")/env.sh"
cd "$C" || exit 2
echo "HEAD $(git rev-parse HEAD) DIRTY $(git status --porcelain --untracked-files=all | wc -l) point $PT" > "$O.head"
/usr/bin/time -v -o "$O-build.time" python3 -B tb/verilator/ctrl_service_budget/build.py "$O-build" "$SHAPE" "$N" > "$O-build.log" 2>&1
echo $? > "$O-build.rc"
/usr/bin/time -v -o "$O-run.time" python3 -B tb/verilator/ctrl_service_budget/run.py --point "$PT" --build-dir "$O-build" --reuse-build --record-budget-findings --out "$O-results" "$@" > "$O-run.log" 2>&1
echo $? > "$O-run.rc"
echo "TREE-AFTER $(git status --porcelain --untracked-files=all | wc -l)" >> "$O.head"

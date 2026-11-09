#!/bin/bash
# One harness point on a clean clone: the build, then every group, each timed with its peak memory.
# usage: hleg.sh CLONE POINT SHAPE N_IF OUT [run options...]
set -u
C=$1 P=$2 SHAPE=$3 N=$4 O=$5; shift 5
cd "$C" || exit 2
echo "HEAD $(git rev-parse HEAD) DIRTY $(git status --porcelain --untracked-files=all | wc -l) point $P" > "$O.head"
/usr/bin/time -v -o "$O-build.time" python3 -B tb/verilator/ctrl_service_budget/build.py "$O-build" "$SHAPE" "$N" > "$O-build.log" 2>&1
echo "build-rc=$?" >> "$O-build.time"
/usr/bin/time -v -o "$O-run.time" python3 -B tb/verilator/ctrl_service_budget/run.py --point "$P" --build-dir "$O-build" --reuse-build --record-budget-findings --out "$O-results" "$@" > "$O-run.log" 2>&1
echo "run-rc=$?" >> "$O-run.time"
echo "TREE-AFTER $(git status --porcelain --untracked-files=all | wc -l)" >> "$O.head"

#!/bin/bash
# One CPU budget harness point on a clean clone: build, then every group, each timed.
# usage: leg.sh CLONE POINT SHAPE N_IF OUTPREFIX JOBS
# Environment: source env.sh first (LiteX venv, pinned RV32 SDK, pinned Verilator, offline CPU generator).
set -u
C=$1 P=$2 SHAPE=$3 N=$4 O=$5 J=$6
cd "$C" || exit 2
echo "HEAD $(git rev-parse HEAD) DIRTY $(git status --porcelain --untracked-files=all | wc -l) point $P jobs $J" > "$O.head"
/usr/bin/time -v -o "$O-build.time" python3 -B tb/verilator/ctrl_service_budget/build.py "$O-build" "$SHAPE" "$N" > "$O-build.log" 2>&1
brc=$?
echo "build-rc=$brc" >> "$O-build.time"
if [ "$brc" -ne 0 ]; then echo "$brc" > "$O.rc"; exit "$brc"; fi
/usr/bin/time -v -o "$O-run.time" python3 -B tb/verilator/ctrl_service_budget/run.py --point "$P" --build-dir "$O-build" \
  --reuse-build --record-budget-findings --out "$O-results" --jobs "$J" > "$O-run.log" 2>&1
rrc=$?
echo "run-rc=$rrc" >> "$O-run.time"
echo "TREE-AFTER $(git status --porcelain --untracked-files=all | wc -l)" >> "$O.head"
echo "$rrc" > "$O.rc"

#!/bin/bash
# The two-placement twin on a clean clone, timed; keeps its report. usage: twin.sh CLONE OUT
set -u
C=$1 O=$2
. "$(dirname "$0")/env.sh"
cd "$C" || exit 2
echo "HEAD $(git rev-parse HEAD) DIRTY $(git status --porcelain --untracked-files=all | wc -l)" > "$O.head"
export MAKEFLAGS="-j4 --no-print-directory"
/usr/bin/time -v -o "$O-twin.time" make -C tb/verilator/milan_dp twin > "$O-twin.log" 2>&1
echo $? > "$O-twin.rc0"
cp tb/verilator/milan_dp/obj_twin/report.json "$O-report.json" 2>/dev/null
echo "TREE-AFTER $(git status --porcelain --untracked-files=all | wc -l)" >> "$O.head"
mv "$O-twin.rc0" "$O-twin.rc"

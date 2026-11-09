#!/bin/bash
# The two-placement twin (make -C tb/verilator/milan_dp twin) on a clean clone, timed, its report kept.
# usage: twin.sh CLONE OUTPREFIX JOBS
set -u
C=$1 O=$2 J=$3
cd "$C" || exit 2
echo "HEAD $(git rev-parse HEAD) DIRTY $(git status --porcelain --untracked-files=all | wc -l)" > "$O.head"
export MAKEFLAGS="-j$J --no-print-directory"
/usr/bin/time -v -o "$O-twin.time" make -C tb/verilator/milan_dp twin > "$O-twin.log" 2>&1
rc=$?
echo "twin-rc=$rc" >> "$O-twin.time"
cp tb/verilator/milan_dp/obj_twin/report.json "$O-report.json" 2>/dev/null
echo "TREE-AFTER $(git status --porcelain --untracked-files=all | wc -l)" >> "$O.head"
git status --porcelain --untracked-files=all > "$O-tree-after.txt"
echo "$rc" > "$O.rc"

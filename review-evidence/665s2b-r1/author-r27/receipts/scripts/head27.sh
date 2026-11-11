#!/bin/bash
# The harness at the final head: a leg's build (made on the clean clone K at e5baac61, which changes no recorded build
# input against the head; its images and sample logs byte-identical to round 26's, logs/<leg>-compare.txt) regraded
# from K moved to the head, every recorded group of the leg, with --reuse-build (refused unless every recorded input
# and tree digest resolves unchanged there). usage: head27.sh HEAD NAME POINT RESULTS [run.py args]
set -u
H=$1 NAME=$2 POINT=$3 RES=$4; shift 4
T=<scratch>
. $T/scripts/env.sh
C=$T/K B=$T/builds/$NAME R=$T/logs/head-$NAME.log
test "$(git -C "$C" rev-parse HEAD)" = "$H" || { echo "clone not at $H" > "$R"; echo 4 > "$R.rc"; exit 4; }
M=$B/results-head; rm -rf "$M"; mkdir -p "$M"; cp "$RES"/*.txt "$RES"/*.log "$M/"
echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=all | wc -l) regrade of every recorded group of $NAME ($(ls "$M"/*.log | wc -l) logs from $RES)" > "$R"
export TMPDIR=$T/tmp/head-$NAME PYTHONUNBUFFERED=1; mkdir -p "$TMPDIR"
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$B" --reuse-build --regrade \
    --out "$M" --record-budget-findings --record-share-findings "$@" >> "$R" 2>&1
rc=$?
echo "rc=$rc" >> "$R"
git -C "$C" status --porcelain --untracked-files=all > "$T/logs/head-$NAME-tree-after.txt"
sync
echo $rc > "$R.rc"

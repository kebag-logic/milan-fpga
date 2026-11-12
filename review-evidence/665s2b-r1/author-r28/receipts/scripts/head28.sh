#!/bin/bash
# The harness at the final head: a leg's build (made on its own clean clone at 71e905fb, whose recorded inputs the
# later commits do not change) regraded from that clone moved to the head, every recorded group of the leg, with
# --reuse-build (refused unless every recorded input and tree digest resolves unchanged there).
# usage: head28.sh HEAD NAME POINT [run.py args]
set -u
H=$1 NAME=$2 POINT=$3; shift 3
T=<scratch>
. $T/scripts/env.sh
C=$T/L-$NAME B=$T/builds/$NAME R=$T/logs/head-$NAME.log
git -C "$C" -c advice.detachedHead=false checkout -q "$H" || { echo "checkout failed" > "$R"; echo 5 > "$R.rc"; exit 5; }
test "$(git -C "$C" rev-parse HEAD)" = "$H" || { echo "clone not at $H" > "$R"; echo 4 > "$R.rc"; exit 4; }
M=$B/results-head; rm -rf "$M"; mkdir -p "$M"; cp "$B"/results-merged/*.txt "$B"/results-merged/*.log "$M/"
echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=all | wc -l) regrade of every recorded group of $NAME ($(ls "$M"/*.log | wc -l) logs)" > "$R"
export TMPDIR=$T/tmp/head-$NAME PYTHONUNBUFFERED=1; mkdir -p "$TMPDIR"
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$B" --reuse-build --regrade \
    --out "$M" --record-budget-findings --record-share-findings "$@" >> "$R" 2>&1
rc=$?
echo "rc=$rc" >> "$R"
git -C "$C" status --porcelain --untracked-files=all > "$T/logs/head-$NAME-tree-after.txt"
echo $rc > "$R.rc"

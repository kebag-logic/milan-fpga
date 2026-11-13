#!/bin/bash
# The harness at the final head: a leg's build, made on its own clean clone at the legs' head, regraded from that clone
# moved to the final head, every recorded group, with --reuse-build (refused unless every recorded input is unchanged).
# usage: head30.sh HEAD NAME CLONE POINT [run.py args]
set -u
H=$1 NAME=$2 CL=$3 POINT=$4; shift 4
T=/data-2/milan/tmp/665s2b-a683zo
. $T/scripts/env.sh
C=$T/L30-$CL B=$T/builds/$NAME R=$T/logs/head-$NAME.log
git -C "$C" fetch -q origin && git -C "$C" -c advice.detachedHead=false checkout -q "$H" && \
  git -C "$C" -c protocol.file.allow=always submodule update -q || { echo "checkout failed" > "$R"; echo 5 > "$R.rc"; exit 5; }
test "$(git -C "$C" rev-parse HEAD)" = "$H" || { echo "clone not at $H" > "$R"; echo 4 > "$R.rc"; exit 4; }
M=$B/results-head; mkdir -p "$M"; find "$M" -mindepth 1 -delete; cp -l "$B"/results/*.txt "$B"/results/*.log "$M/"
echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=all | wc -l) regrade of every recorded group of $NAME ($(ls "$M"/*.log | wc -l) logs)" > "$R"
export TMPDIR=$T/tmp/head-$NAME PYTHONUNBUFFERED=1; mkdir -p "$TMPDIR"
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$B" --reuse-build --regrade \
    --out "$M" --record-budget-findings --record-share-findings "$@" >> "$R" 2>&1
rc=$?
echo "rc=$rc" >> "$R"
git -C "$C" status --porcelain --untracked-files=all > "$T/logs/head-$NAME-tree-after.txt"
echo $rc > "$R.rc"

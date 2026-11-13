#!/bin/bash
# A 1x1 leg's fresh build at a head whose firmware digest moved and whose image must not: one sample group run on it, its
# images, inputs and the sample's log compared with the leg's old build (compare_builds.py), then every recorded group of
# the old leg regraded on the fresh build from its own clone (--reuse-build, --regrade).
# usage: sample33.sh CLONE NAME POINT SAMPLE OLD_BUILD OLD_RESULTS [run.py args]
set -u
C=$1 NAME=$2 POINT=$3 SAMPLE=$4 OLD=$5 OLDR=$6; shift 6
T=/data-2/milan/tmp/665s2b-a683zo
. $T/scripts/env.sh
NEW=$T/builds/$NAME R=$T/logs/$NAME.log
export TMPDIR=$T/tmp/$NAME MAKEFLAGS="-j8 --no-print-directory" PYTHONUNBUFFERED=1; mkdir -p "$TMPDIR"
echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=all | wc -l) $NAME: a fresh build with $SAMPLE, start $(date +%T)" > "$R"
rm -rf "$NEW"; mkdir -p "$NEW"
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$NEW" --groups "$SAMPLE" \
    --out "$NEW/results-sample" --record-budget-findings --record-share-findings --jobs 1 "$@" >> "$R" 2>&1
echo "sample rc=$?" >> "$R"
python3 $T/scripts/compare_builds.py "$OLD" "$NEW" "$OLDR/$SAMPLE.log" "$NEW/results-sample/$SAMPLE.log" > "$T/logs/$NAME-compare.txt" 2>&1
crc=$?
echo "compare rc=$crc" >> "$R"
M=$NEW/results-head; rm -rf "$M"; mkdir -p "$M"
for f in "$OLDR"/*.txt "$OLDR"/*.log; do cp -l "$f" "$M/" 2>/dev/null || cp "$f" "$M/"; done
groups=$(ls "$M"/*.log | xargs -n1 basename | sed 's/\.log$//' | paste -sd,)
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$NEW" --reuse-build --regrade \
    --out "$M" --groups "$groups" --record-budget-findings --record-share-findings "$@" > "$T/logs/$NAME-regrade.log" 2>&1
rc=$?
echo "regrade rc=$rc; $(grep -E 'groups graded' $T/logs/$NAME-regrade.log | tail -1)" >> "$R"
[ $crc = 0 ] || rc=$crc
git -C "$C" status --porcelain --untracked-files=all > "$T/logs/$NAME-tree-after.txt"
echo "end $(date +%T)" >> "$R"
echo $rc > "$R.rc"

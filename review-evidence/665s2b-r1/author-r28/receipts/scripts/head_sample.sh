#!/bin/bash
# The harness at the final head after a commit that changed the firmware digest's trees (the coverage ratchet) and no
# image: a fresh build of the leg's point on its own clone at the head, one sample group run on it, the images, inputs
# and the sample's log compared with the leg's build (compare_builds.py), then every recorded group of the leg regraded
# against the new build with --reuse-build. usage: head_sample.sh HEAD NAME POINT SAMPLE [run.py args]
set -u
H=$1 NAME=$2 POINT=$3 SAMPLE=$4; shift 4
T=<scratch>
. $T/scripts/env.sh
C=$T/L-$NAME OLD=$T/builds/$NAME NEW=$T/builds/$NAME-head R=$T/logs/headS-$NAME.log
export TMPDIR=$T/tmp/headS-$NAME MAKEFLAGS="-j8 --no-print-directory" PYTHONUNBUFFERED=1; mkdir -p "$TMPDIR"
git -C "$C" -c advice.detachedHead=false checkout -q "$H" || { echo 5 > "$R.rc"; exit 5; }
test "$(git -C "$C" rev-parse HEAD)" = "$H" || { echo 4 > "$R.rc"; exit 4; }
echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=all | wc -l) $NAME: a fresh build with $SAMPLE" > "$R"
rm -rf "$NEW"; mkdir -p "$NEW"
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$NEW" --groups "$SAMPLE" \
    --out "$NEW/results-sample" --record-budget-findings --record-share-findings --jobs 1 "$@" >> "$R" 2>&1
echo "sample rc=$?" >> "$R"
python3 $T/scripts/compare_builds.py "$OLD" "$NEW" "$OLD/results-merged/$SAMPLE.log" "$NEW/results-sample/$SAMPLE.log" > "$T/logs/headS-$NAME-compare.txt" 2>&1
crc=$?
echo "compare rc=$crc" >> "$R"
M=$NEW/results-head; rm -rf "$M"; mkdir -p "$M"; cp "$OLD"/results-merged/*.txt "$OLD"/results-merged/*.log "$M/"
groups=$(ls "$M"/*.log | xargs -n1 basename | sed 's/\.log$//' | paste -sd,)
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$NEW" --reuse-build --regrade \
    --out "$M" --groups "$groups" --record-budget-findings --record-share-findings "$@" > "$T/logs/headS-$NAME-regrade.log" 2>&1
rc=$?
echo "regrade rc=$rc; $(grep -E 'groups graded' $T/logs/headS-$NAME-regrade.log | tail -1)" >> "$R"
git -C "$C" status --porcelain --untracked-files=all > "$T/logs/headS-$NAME-tree-after.txt"
[ $crc = 0 ] || rc=$crc
echo $rc > "$R.rc"

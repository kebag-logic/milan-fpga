#!/bin/bash
# The harness at the final head, one leg: its build made at 6c284a97 on its own clean clone, regraded from that clone
# moved to the final head with --reuse-build (refused unless every recorded input is unchanged), every group.
# An 8x8 leg (MODE merge) regrades its runs merged (its own and its helpers'); a 1x1 leg (MODE sample) regrades the
# old leg's logs its sample build holds in results-head, after the image and sample byte-compare (sample33.sh).
# usage: head33.sh HEAD MODE CLONE BUILD_NAME POINT [run.py args]
set -u
H=$1 MODE=$2 C=$3 NAME=$4 POINT=$5; shift 5
T=/data-2/milan/tmp/665s2b-a683zo
. $T/scripts/env.sh
B=$T/builds/$NAME R=$T/logs/head-$NAME.log
git -C "$C" fetch -q origin && git -C "$C" -c advice.detachedHead=false checkout -q "$H" && \
  git -C "$C" -c protocol.file.allow=always submodule update -q || { echo "checkout failed" > "$R"; echo 5 > "$R.rc"; exit 5; }
test "$(git -C "$C" rev-parse HEAD)" = "$H" || { echo "clone not at $H" > "$R"; echo 4 > "$R.rc"; exit 4; }
test -z "$(git -C "$C" status --porcelain --untracked-files=all)" || { echo "clone dirty" > "$R"; echo 4 > "$R.rc"; exit 4; }
export TMPDIR=$T/tmp/head-$NAME PYTHONUNBUFFERED=1; mkdir -p "$TMPDIR"
mrc=0
if [ "$MODE" = merge ]; then
    M=$B/results-merged
    G=$(cd "$C/tb/verilator/ctrl_service_budget" && python3 -B -c "
import json, sys
sys.path[:0] = ['.', '../../../sw/mailbox']
import run, scenario
spec = json.load(open('$B/build.json'))
print(','.join(g.name for g in run.all_groups(scenario.point('$POINT', spec), spec)))")
    mkdir -p "$M"; find "$M" -mindepth 1 -delete
    python3 $T/scripts/merge_leg.py "$B" "$M" "$G" > "$T/logs/head-$NAME-merge.txt" 2>&1
    mrc=$?
    note="merge rc=$mrc, $(tail -n1 $T/logs/head-$NAME-merge.txt)"
else
    M=$B/results-head
    G=$(ls "$M"/*.log | xargs -n1 basename | sed 's/\.log$//' | paste -sd,)
    note="the old leg's $(ls "$M"/*.log | wc -l) logs on the sample build; $(cat $T/logs/$NAME-compare.txt | tail -1)"
fi
echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=all | wc -l) regrade of $NAME: $note" > "$R"
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$B" --reuse-build --regrade \
    --out "$M" --groups "$G" --record-budget-findings --record-share-findings "$@" >> "$R" 2>&1
rc=$?
[ $mrc = 0 ] || rc=$mrc
echo "rc=$rc" >> "$R"
git -C "$C" status --porcelain --untracked-files=all > "$T/logs/head-$NAME-tree-after.txt"
echo $rc > "$R.rc"

#!/bin/bash
# The harness at the final head: a leg's build, made on its own clean clone at the legs' head (da1869a3), its runs
# (the leg's own and its helpers') merged, regraded from that clone moved to the final head, every group of the leg,
# with --reuse-build (refused unless every recorded input is unchanged). usage: head32.sh HEAD NAME POINT [run.py args]
set -u
H=$1 NAME=$2 POINT=$3; shift 3
T=/data-2/milan/tmp/665s2b-a683zo
. $T/scripts/env.sh
C=$T/L32-$NAME B=$T/builds/$NAME R=$T/logs/head-$NAME.log M=$T/builds/$NAME/results-merged
git -C "$C" fetch -q origin && git -C "$C" -c advice.detachedHead=false checkout -q "$H" && \
  git -C "$C" -c protocol.file.allow=always submodule update -q || { echo "checkout failed" > "$R"; echo 5 > "$R.rc"; exit 5; }
test "$(git -C "$C" rev-parse HEAD)" = "$H" || { echo "clone not at $H" > "$R"; echo 4 > "$R.rc"; exit 4; }
test -z "$(git -C "$C" status --porcelain --untracked-files=all)" || { echo "clone dirty" > "$R"; echo 4 > "$R.rc"; exit 4; }
export TMPDIR=$T/tmp/head-$NAME PYTHONUNBUFFERED=1; mkdir -p "$TMPDIR"
G=$(cd "$C/tb/verilator/ctrl_service_budget" && python3 -B -c "
import json, sys
sys.path[:0] = ['.', '../../../sw/mailbox']
import run, scenario
spec = json.load(open('$B/build.json'))
groups = [g.name for g in run.all_groups(scenario.point('$POINT', spec), spec)]
wanted = sys.argv[1].split(',') if len(sys.argv) > 1 and sys.argv[1] else None
print(','.join(g for g in groups if wanted is None or g in wanted))" "${GROUPS_ONLY:-}")
mkdir -p "$M"; find "$M" -mindepth 1 -delete
python3 $T/scripts/merge_leg.py "$B" "$M" "$G" > "$T/logs/head-$NAME-merge.txt" 2>&1
mrc=$?
echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=all | wc -l) regrade of $NAME: merge rc=$mrc, $(tail -n1 $T/logs/head-$NAME-merge.txt)" > "$R"
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$B" --reuse-build --regrade \
    --out "$M" --groups "$G" --record-budget-findings --record-share-findings "$@" >> "$R" 2>&1
rc=$?
[ $mrc = 0 ] || rc=$mrc
echo "rc=$rc" >> "$R"
git -C "$C" status --porcelain --untracked-files=all > "$T/logs/head-$NAME-tree-after.txt"
echo $rc > "$R.rc"

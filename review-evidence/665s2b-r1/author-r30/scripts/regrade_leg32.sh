#!/bin/bash
# A leg's runs (its own and its helpers') merged into results-merged and regraded at the legs' head from the leg's own
# clone (da1869a3, the build's recorded paths), every group, for the full tally of its STATED lines.
# usage: regrade_leg32.sh NAME POINT [run.py args]
set -u
NAME=$1 POINT=$2; shift 2
T=/data-2/milan/tmp/665s2b-a683zo
. $T/scripts/env.sh
C=$T/L32-$NAME B=$T/builds/$NAME M=$T/builds/$NAME/results-merged R=$T/logs/merged-$NAME.log
export TMPDIR=$T/tmp/merged-$NAME PYTHONUNBUFFERED=1; mkdir -p "$TMPDIR"
G=$(cd "$C/tb/verilator/ctrl_service_budget" && python3 -B -c "
import json, sys
sys.path[:0] = ['.', '../../../sw/mailbox']
import run, scenario
spec = json.load(open('$B/build.json'))
print(','.join(g.name for g in run.all_groups(scenario.point('$POINT', spec), spec)))")
mkdir -p "$M"; find "$M" -mindepth 1 -delete
python3 $T/scripts/merge_leg.py "$B" "$M" "$G" > "$T/logs/merged-$NAME-merge.txt" 2>&1
mrc=$?
echo "HEAD $(git -C "$C" rev-parse HEAD) $NAME: merge rc=$mrc, $(tail -n1 $T/logs/merged-$NAME-merge.txt)" > "$R"
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$B" --reuse-build --regrade \
    --out "$M" --groups "$G" --record-budget-findings --record-share-findings "$@" >> "$R" 2>&1
echo "rc=$?" >> "$R"

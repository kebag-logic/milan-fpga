#!/bin/bash
# A leg's merge and regrade again, from its own clone, after its runs ended. usage: remerge.sh CLONE NAME POINT GROUPS [run.py args]
set -u
C=$1 NAME=$2 POINT=$3 GROUPS_=$4; shift 4
T=<scratch>
. $T/scripts/env.sh
B=$T/builds/$NAME L=$T/logs/$NAME.log H=$C/tb/verilator/ctrl_service_budget
rm -rf "$B/results-merged"
python3 $T/scripts/merge_leg.py "$B" "$B/results-merged" "$GROUPS_" > "$T/logs/$NAME-merge.txt" 2>&1
mrc=$?
echo "$(date +%T) re-merge rc=$mrc $(tail -n1 $T/logs/$NAME-merge.txt)" >> "$L"
TMPDIR=$T/tmp/$NAME-regrade PYTHONUNBUFFERED=1 python3 -B "$H/run.py" --point "$POINT" --build-dir "$B" --reuse-build --regrade \
    --out "$B/results-merged" --groups "$GROUPS_" --record-budget-findings --record-share-findings "$@" > "$T/logs/$NAME-regrade.log" 2>&1
rc=$?
[ $mrc = 0 ] || rc=$mrc
echo "$(date +%T) regrade rc=$rc; $(grep -E 'groups graded' $T/logs/$NAME-regrade.log | tail -1)" >> "$L"
echo $rc > "$L.rc"

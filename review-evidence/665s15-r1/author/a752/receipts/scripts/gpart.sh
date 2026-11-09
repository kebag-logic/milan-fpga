#!/bin/bash
# One part of a point's clean harness gate leg: every group of arm A, split by simulated time into NPARTS parts that
# share one build. Part 0 builds; the others wait for its build to finish, then reuse it. Each writes its own results
# directory; regrade.sh merges them and grades every group at once. usage: gpart.sh COMMIT NAME POINT PART NPARTS
set -u
H=$1 NAME=$2 POINT=$3 K=$4 N=$5
T=<scratch>
. $T/scripts/env.sh
C=$T/hleg-wt-$NAME
B=$T/builds/$NAME
L=$T/logs/$NAME-part$K.log
export TMPDIR=$T/tmp-$NAME-$K MAKEFLAGS="-j8 --no-print-directory"; mkdir -p "$TMPDIR"
if [ "$K" = 0 ]; then
    [ -d "$C" ] || bash $T/scripts/clone.sh "$C" "$H" > $T/logs/clone-$NAME.log 2>&1
else
    until [ -f "$B/build.done" ]; do sleep 60; done
fi
test "$(git -C "$C" rev-parse HEAD)" = "$H" || exit 4
echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=no | wc -l) part $K/$N" > "$L"
start=$(date +%s)
export TIMEFORMAT="harness part wall %R s"
if [ "$K" = 0 ] && [ ! -f "$B/build.done" ]; then
    # build first with one short group, then mark the build done for the other parts, then run this part's groups
    python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$B" --groups backlog \
        --out "$B/results-build" --record-budget-findings --record-share-findings --jobs 8 >> "$L" 2>&1
    echo "build rc=$?" >> "$L"; touch "$B/build.done"
fi
groups=$(cd "$C/tb/verilator/ctrl_service_budget" && python3 -B "$T/scripts/partition.py" "$B" "$POINT" "$K" "$N" "$K")
echo "groups: $groups" >> "$L"
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$B" --reuse-build --groups "$groups" \
    --out "$B/results-part$K" --record-budget-findings --record-share-findings --jobs 8 >> "$L" 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s" >> "$L"; echo "rc=$rc" >> "$L"

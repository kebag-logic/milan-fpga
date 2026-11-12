#!/bin/bash
# One measurement leg on its own clean clone: a build made with the first group, then each ALONE group by itself (one
# job) beside the rest (JOBS jobs), all on that one build; then every group's finished log merged (merge_leg.py) and the
# leg regraded from the same clone. GROUPS is a comma list, or "all" for every group of the arm at the point.
# usage: fleg.sh CLONE NAME POINT JOBS ALONE GROUPS [run.py args]     (logs/NAME.log, its rc in logs/NAME.log.rc)
set -u
C=$1 NAME=$2 POINT=$3 J=$4 ALONE=$5 GROUPS_=$6; shift 6
T=<scratch>
. $T/scripts/env.sh
B=$T/builds/$NAME L=$T/logs/$NAME.log H=$C/tb/verilator/ctrl_service_budget
export MAKEFLAGS="-j8 --no-print-directory" PYTHONUNBUFFERED=1
mkdir -p "$B"
echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=all | wc -l) point $POINT jobs $J alone $ALONE groups $GROUPS_ args $*" > "$L"
start=$(date +%s)
run1() {  # OUT GROUPS JOBS [extra run.py args]
    local out=$1 groups=$2 jobs=$3; shift 3
    TMPDIR=$T/tmp/$NAME-$(basename "$out") python3 -B "$H/run.py" --point "$POINT" --build-dir "$B" --groups "$groups" \
        --out "$out" --record-budget-findings --record-share-findings --jobs "$jobs" "$@"
}
mkdir -p $T/tmp/$NAME-results-build
first=${GROUPS_%%,*}
echo "$(date +%T) build with $first" >> "$L"
run1 "$B/results-build" "$first" 1 "$@" >> "$L" 2>&1
echo "$(date +%T) build rc=$?" >> "$L"
pids=()
[ "$ALONE" = "-" ] && ALONE=""
for g in ${ALONE//,/ }; do
    mkdir -p $T/tmp/$NAME-results-$g
    ( run1 "$B/results-$g" "$g" 1 --reuse-build "$@" > "$T/logs/$NAME-$g.log" 2>&1; echo "rc=$?" >> "$T/logs/$NAME-$g.log" ) &
    pids+=($!)
done
rest=$(python3 -c "import sys; a=sys.argv[1].split(','); s=set(sys.argv[2].split(',')) if sys.argv[2] else set(); print(','.join(g for g in a if g not in s and g != sys.argv[3]))" "$GROUPS_" "$ALONE" "$first")
if [ -n "$rest" ]; then
    mkdir -p $T/tmp/$NAME-results-rest
    ( run1 "$B/results-rest" "$rest" "$J" --reuse-build "$@" > "$T/logs/$NAME-rest.log" 2>&1; echo "rc=$?" >> "$T/logs/$NAME-rest.log" ) &
    pids+=($!)
fi
for p in "${pids[@]}"; do wait $p; done
echo "$(date +%T) runs ended" >> "$L"
python3 $T/scripts/merge_leg.py "$B" "$B/results-merged" "$GROUPS_" > "$T/logs/$NAME-merge.txt" 2>&1
mrc=$?
echo "$(date +%T) merge rc=$mrc $(tail -n1 $T/logs/$NAME-merge.txt)" >> "$L"
TMPDIR=$T/tmp/$NAME-regrade python3 -B "$H/run.py" --point "$POINT" --build-dir "$B" --reuse-build --regrade \
    --out "$B/results-merged" --groups "$GROUPS_" --record-budget-findings --record-share-findings "$@" > "$T/logs/$NAME-regrade.log" 2>&1
rc=$?
[ $mrc = 0 ] || rc=$mrc
echo "$(date +%T) regrade rc=$rc; $(grep -E 'groups graded' $T/logs/$NAME-regrade.log | tail -1)" >> "$L"
echo "elapsed=$(( $(date +%s) - start ))s rc=$rc" >> "$L"
git -C "$C" status --porcelain --untracked-files=all > "$T/logs/$NAME-tree-after.txt"
echo $rc > "$L.rc"

#!/bin/bash
# Finish a leg that has helper runs: wait until every one of its groups is finished by the leg or a helper
# (combine.py), stop the leg's own run.py if it is still running (its remaining groups are the helpers'), merge the
# helpers' scripts and logs into its results, and grade the whole leg there with run.py --regrade. Only groups the
# leg itself finished keep its logs; every other group's is a helper's.
# usage: finish_leg.sh LEG CHECKOUT HELPERS GROUPS|all POINT [run.py args]
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683u/scripts/env.sh
S=$MANAGEMENT/2026-09-23/665s2b-a683u/scripts
T=$VALIDATION_STORAGE/665s2b-a683u
LEG=$1 C=$T/$2 HELPERS=$3 GROUPS_ARG=$4 POINT=$5; shift 5
B=$T/builds/$LEG
until python3 -B $S/combine.py "$C" "$B" "$HELPERS" "$GROUPS_ARG" | grep -q " 0 by neither"; do sleep 30; done
python3 -B $S/combine.py "$C" "$B" "$HELPERS" "$GROUPS_ARG" | cut -c1-200 > "$T/logs/$LEG-finish.log"
for pid in $(pgrep -f "run.py --point $POINT --build-dir $B "); do
    if ! tr '\0' ' ' < /proc/$pid/cmdline | grep -q -- "--out"; then
        echo "$(date +%T) stop the leg's own run, pid $pid" >> "$T/logs/$LEG-finish.log"; kill "$pid"
    fi
done
# and the simulations it started, which write into its own results, so none writes into a log the merge replaces
sleep 5
pkill -f "$B/native/Vsim $B/results/" && echo "$(date +%T) stop the leg's own simulations" >> "$T/logs/$LEG-finish.log"
sleep 15
pgrep -f "$B/native/Vsim $B/results/" > /dev/null && { echo "simulations still running" >> "$T/logs/$LEG-finish.log"; exit 3; }
python3 -B $S/combine.py "$C" "$B" "$HELPERS" "$GROUPS_ARG" --merge | cut -c1-200 >> "$T/logs/$LEG-finish.log"
g=(); [ "$GROUPS_ARG" != all ] && g=(--groups "$GROUPS_ARG")
start=$(date +%s)
echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=no | wc -l)" > "$T/logs/$LEG-regrade.log"
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$B" --reuse-build --regrade \
  "${g[@]}" --record-budget-findings --record-share-findings "$@" >> "$T/logs/$LEG-regrade.log" 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s" >> "$T/logs/$LEG-regrade.log"
echo "rc=$rc" >> "$T/logs/$LEG-regrade.log"

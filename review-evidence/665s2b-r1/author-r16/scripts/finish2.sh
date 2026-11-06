#!/bin/bash
# Finish a split leg that has a helper run: wait until every one of its groups is finished by its long run, its rest
# run or the helper (combine.py), stop the rest run and its simulations if still running (the groups it has left are
# the helper's), merge the rest's and the helper's scripts and logs into the leg's results and grade the whole leg
# there with run.py --regrade. usage: finish2.sh LEG CHECKOUT POINT HELPER [run.py args]
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683u/scripts/env.sh
S=$MANAGEMENT/2026-09-23/665s2b-a683u/scripts
T=$VALIDATION_STORAGE/665s2b-a683u
LEG=$1 CK=$2 POINT=$3 HELPER=$4; shift 4
C=$T/$CK B=$T/builds/$LEG L=$T/logs
mapfile -t P < $T/plan-$LEG.txt
G="${P[0]},${P[1]}"
until python3 -B $S/combine.py "$C" "$B" "$LEG-rest,$HELPER" "$G" | grep -q " 0 by neither"; do sleep 30; done
echo "$(date +%T) every group finished" >> $L/$LEG-split.txt
python3 -B $S/combine.py "$C" "$B" "$LEG-rest,$HELPER" "$G" | cut -c1-300 >> $L/$LEG-split.txt
for pid in $(ps -eo pid,args | awk -v o="$B/results-$LEG-rest" 'index($0, "run.py") && index($0, o) && !/awk/ {print $1}'); do
    echo "$(date +%T) stop the rest run, pid $pid" >> $L/$LEG-split.txt; kill "$pid"
done
sleep 5
for pid in $(ps -eo pid,args | awk -v o="$B/results-$LEG-rest/" 'index($0, "native/Vsim") && index($0, o) && !/awk/ {print $1}'); do
    echo "$(date +%T) stop the rest run's simulation, pid $pid" >> $L/$LEG-split.txt; kill "$pid"
done
sleep 15
python3 -B $S/combine.py "$C" "$B" "$LEG-rest,$HELPER" "$G" --merge > $L/$LEG-merge.log 2>&1
echo "$(date +%T) merge rc=$?" >> $L/$LEG-split.txt
start=$(date +%s)
echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=no | wc -l)" > $L/$LEG-regrade.log
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$B" --reuse-build --regrade \
  --groups "$G" --record-budget-findings --record-share-findings "$@" >> $L/$LEG-regrade.log 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s" >> $L/$LEG-regrade.log
echo "rc=$rc" >> $L/$LEG-regrade.log
echo "$(date +%T) regrade rc=$rc" >> $L/$LEG-split.txt

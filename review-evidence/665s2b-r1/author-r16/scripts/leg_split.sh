#!/bin/bash
# One leg as two runs on one build: its LONG groups (which builds the point), then, once the build is done, the REST
# on the same build into results-rest; when both end, the rest's scripts and logs are merged into the leg's results
# (combine.py --merge) and the whole leg is graded there by run.py --regrade.
# usage: leg_split.sh LEG CHECKOUT POINT LONG_JOBS LONG_GROUPS REST_JOBS REST_GROUPS [run.py args]
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683u/scripts/env.sh
S=$MANAGEMENT/2026-09-23/665s2b-a683u/scripts
T=$VALIDATION_STORAGE/665s2b-a683u
LEG=$1 CK=$2 POINT=$3 LJ=$4 LG=$5 RJ=$6 RG=$7; shift 7
C=$T/$CK B=$T/builds/$LEG L=$T/logs
mkdir -p $L
echo "$(date +%T) start $LEG" >> $L/$LEG-split.txt
JOBS=$LJ $S/leg.sh "$C" "$LEG" "$POINT" "$LG" "$@" &
long=$!
until [ -f "$B/build.json" ] && [ -x "$B/native/Vsim" ] && grep -q "^COMMAND .*/native/Vsim" "$L/$LEG.log" 2>/dev/null; do
    kill -0 $long 2>/dev/null || { echo "$(date +%T) long run ended before its build was ready" >> $L/$LEG-split.txt; exit 3; }
    sleep 20
done
echo "$(date +%T) build ready; rest starts" >> $L/$LEG-split.txt
JOBS=$RJ $S/leg2.sh "$C" "$LEG-rest" "$LEG" "$POINT" "$RG" "$@" &
rest=$!
wait $long; echo "$(date +%T) long ended $(tail -1 $L/$LEG.log)" >> $L/$LEG-split.txt
wait $rest; echo "$(date +%T) rest ended $(tail -1 $L/$LEG-rest.log)" >> $L/$LEG-split.txt
python3 -B $S/combine.py "$C" "$B" "$LEG-rest" "$LG,$RG" --merge > $L/$LEG-merge.log 2>&1
echo "$(date +%T) merge rc=$?" >> $L/$LEG-split.txt
start=$(date +%s)
echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=no | wc -l)" > $L/$LEG-regrade.log
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$B" --reuse-build --regrade \
  --groups "$LG,$RG" --record-budget-findings --record-share-findings "$@" >> $L/$LEG-regrade.log 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s" >> $L/$LEG-regrade.log
echo "rc=$rc" >> $L/$LEG-regrade.log
echo "$(date +%T) regrade rc=$rc" >> $L/$LEG-split.txt

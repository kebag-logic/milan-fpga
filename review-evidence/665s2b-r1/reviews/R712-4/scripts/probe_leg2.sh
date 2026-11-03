#!/bin/bash
# usage: probe_leg2.sh NAME BUILD TREE GROUPS JOBS: reruns groups on an existing probe build into its own results dir.
set -u
. $REVIEWS/665s2b-r712-4-packet/scripts/probe_env.sh
NAME=$1 BUILD=$2 T=$3 GROUPS_ARG=$4 J=$5
start=$(date +%s)
echo "HEAD $(git -C $T rev-parse HEAD) DIRTY $(git -C $T status --porcelain --untracked-files=no | wc -l)" > $S/logs/$NAME.log
python3 -B $T/tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir $S/builds/$BUILD --reuse-build --out $S/builds/$BUILD/$NAME \
  --groups "$GROUPS_ARG" --record-budget-findings --record-share-findings --jobs $J >> $S/logs/$NAME.log 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s" >> $S/logs/$NAME.log
echo $rc > $S/logs/$NAME.rc

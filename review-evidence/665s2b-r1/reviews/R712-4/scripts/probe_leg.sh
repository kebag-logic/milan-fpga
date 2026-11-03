#!/bin/bash
# usage: probe_leg.sh NAME GROUPS JOBS [run.py args]; runs the scratch probe tree's harness at 8x8, logs and rc in scratch/logs.
set -u
. $REVIEWS/665s2b-r712-4-packet/scripts/probe_env.sh
NAME=$1 GROUPS_ARG=$2 J=$3; shift 3
T=${TREE:-$S/probe-tree}
start=$(date +%s)
echo "HEAD $(git -C $T rev-parse HEAD) DIRTY $(git -C $T status --porcelain --untracked-files=no | wc -l) verilator $(verilator --version)" > $S/logs/$NAME.log
python3 -B $T/tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir $S/builds/$NAME --groups "$GROUPS_ARG" \
  --record-budget-findings --record-share-findings --jobs $J "$@" >> $S/logs/$NAME.log 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s" >> $S/logs/$NAME.log
echo $rc > $S/logs/$NAME.rc

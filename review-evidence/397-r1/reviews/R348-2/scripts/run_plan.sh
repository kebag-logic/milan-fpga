#!/bin/bash
# Run one named plan at the exact head with the published arguments (foreground).
# usage: run_plan.sh <repo> <scratch> <1x1|8x8> <plan>
set -u
REPO=$1; S=$2; K=$3; PLAN=$4
. "$(dirname "$0")/env.sh"
case $K in 1x1) SHAPE=endstation_ax7101_1x1_tdm8;; 8x8) SHAPE=endstation_ax7101_8x8;; esac
W="--device-wait-us 0 --program-wait-us 0"
[ "$PLAN" = all ] && [ $K = 8x8 ] && W="--device-wait-us 1000 --program-wait-us 1000"
[ "$PLAN" = device-wait ] && W="--device-wait-us 3000000 --program-wait-us 5000"
cd "$REPO"
/usr/bin/time -f 'wall %e s' python -B tb/verilator/fw_service_budget/run.py --shape $SHAPE \
  --build-dir $S/build-$SHAPE --reuse-build --populated --plan $PLAN $W --record-budget-findings \
  > $S/run-$K-$PLAN.out 2>&1
echo "run $K $PLAN rc=$?" | tee -a $S/run-status.txt

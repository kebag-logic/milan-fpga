#!/bin/bash
# The R824-1 packet's matrix and CI run, unchanged, at the new head.
set -u
S=<scratch> P=<scratch>/r824
export TOOLS=<tools>
H=$(git -C $S/trees/head rev-parse HEAD)
( bash $P/scripts/matrix.sh $P/scratch $P/receipts/differential/matrix 20000 > $P/receipts/differential/matrix.driver.log 2>&1 ) &
( bash $P/scripts/ci_run.sh <lanes>/tsn-c-stack-32-walk $H $P/scratch/ci-head > $P/receipts/ci-run.driver.log 2>&1; echo $? > $P/receipts/ci-run.driver.rc ) &
wait
echo done > $P/receipts/PART2-DONE

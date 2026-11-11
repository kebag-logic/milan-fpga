#!/bin/bash
# The R823-1 packet's scripts, unchanged, at the new head. Its launch.sh writes receipts/NAME.log and NAME.rc.
set -u
S=<scratch> P=<scratch>/r823
export TSN_TOOLS=<tools>
H=$(git -C $S/trees/head rev-parse HEAD) R=$S/trees/head
cd $P
sh scripts/launch.sh differential-head-vs-main $P sh $P/scripts/differential.sh $S/trees/head $S/trees/main $P/scratch/differential 60
sh scripts/launch.sh probe-mutants $P python3 $P/scripts/probe_mutants.py $S/trees/probe $S/trees/main $P/scratch/mutants
python3 scripts/plant_merge.py $R ea4af6f fa31d4c8 9deb0ddb $H > receipts/plant-merge.txt 2>&1; echo $? > receipts/plant-merge.rc
python3 scripts/plant_delta.py $R 9deb0ddb $H > receipts/plant-delta.txt 2>&1; echo $? > receipts/plant-delta.rc
python3 scripts/plant_defects.py $R 9deb0ddb $H > receipts/plant-defects.txt 2>&1; echo $? > receipts/plant-defects.rc
( export PATH=<tools>/clang-tidy-18/bin:$PATH; sh scripts/sanitizers_standin.sh $S/trees/head $P/scratch/sanitizers 16 > receipts/sanitizers-standin.log 2>&1; echo $? > receipts/sanitizers-standin.rc )

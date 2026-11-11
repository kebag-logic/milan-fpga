#!/bin/bash
# The R824-1 packet's scripts, unchanged, at the new head (first part: everything but the matrix, the campaign
# kill words and the CI run). Outputs in r824/receipts.
set -u
S=<scratch> P=<scratch>/r824
export TOOLS=<tools>
R=$S/trees/head H=$(git -C $S/trees/head rev-parse HEAD) M=9deb0ddb299013fcf2d9df7ad3d31961a33013cd
O=$P/receipts; mkdir -p $O/differential $O/sanitizer-host $P/scratch/plants
for m in 16 32 33 64 255; do
  bash $P/scripts/build_dwalk.sh $R $H $M $P/scratch/dwalk-$m $m > $O/differential/dwalk-$m.build.log 2>&1; echo $? > $O/differential/dwalk-$m.build.rc
done
bash $P/scripts/merge_survival.sh $R ea4af6f fa31d4c8 9deb0ddb $H src/acmp.c include/acmp.h CMakeLists.txt scripts/mutation.py tests/test_acmp.cpp tests/test_acmp_walk.cpp tests/test_acmp_wide.cpp > $O/merge-survival.txt 2>&1; echo $? > $O/merge-survival.rc
python3 $P/scripts/plant_merge_audit.py $R ea4af6f fa31d4c8 9deb0ddb $H > $O/plant-merge-audit.txt 2>&1; echo $? > $O/plant-merge-audit.rc
git -C $R show $H:src/acmp.c > $P/scratch/plants/head.c
: > $O/probe-controls-dwalk.txt; : > $O/probe-controls-suite.txt
for d in <management>/2026-09-23/tsn32-r824-1/receipts/differential/plant-*.diff; do
  n=$(basename $d .diff); n=${n#plant-}
  patch -s -o $P/scratch/plants/$n.c $P/scratch/plants/head.c < $d || { echo "$n: patch failed" >> $O/probe-controls-dwalk.txt; continue; }
  bash $P/scripts/build_dwalk.sh $R $H $M $P/scratch/plant-$n 33 $P/scratch/plants/$n.c > $P/scratch/plant-$n.build.log 2>&1
  for l in 0 1; do
    echo "$n LIFT=$l 33 sinks: $(env LIFT=$l SINKS=33 STEPS=20000 SEED=1 $P/scratch/plant-$n/dwalk 2>&1 | head -1) (seed 1)" >> $O/probe-controls-dwalk.txt
  done
  echo "== $n" >> $O/probe-controls-suite.txt
  bash $P/scripts/suite_on_plant.sh $R $H $P/scratch/plants/$n.c $P/scratch/suite-$n >> $O/probe-controls-suite.txt 2>&1
done
bash $P/scripts/sanitizer_gate.sh $R $O/sanitizer-host /usr/bin/clang /usr/bin/clang++ > $O/sanitizer-host.driver.log 2>&1; echo $? > $O/sanitizer-host.driver.rc
echo done > $O/PART1-DONE

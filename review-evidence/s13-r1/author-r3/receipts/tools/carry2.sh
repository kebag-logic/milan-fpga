#!/bin/bash
# carry2.sh <head10>: carry.sh at both shapes for <head10>, then compare_inputs.py against the 822e3af0 builds.
set -u
S=<scratch>; G=$S/gate; H=$1; rc=0
for P in 1x1 8x8; do
  if [ $P = 1x1 ]; then STEM=endstation_ax7101_1x1_tdm8; else STEM=endstation_ax7101_8x8; fi
  echo "== carry $P at $H $(date +%T)"
  bash $G/tools/carry.sh $P $H > $S/logs2/carry-$P-$H.log 2>&1; echo "carry.sh rc=$? $(tail -n 1 $S/logs2/carry-$P-$H.log)"
  echo "# compare_inputs.py: the $P image's inputs at $H against the built image's at 822e3af0" > $S/logs2/inputs-carry-$P-$H.txt
  python3 -I $S/bin/compare_inputs.py $G/work/flip-$P $G/clones/flip-$P $G/work/carry-$H-$P $G/clones/carry-$H-$P $STEM >> $S/logs2/inputs-carry-$P-$H.txt 2>&1
  r=$?; echo "rc=$r" >> $S/logs2/inputs-carry-$P-$H.txt; tail -n 2 $S/logs2/inputs-carry-$P-$H.txt; [ $r = 0 ] || rc=1
done
echo "END rc=$rc $(date -Iseconds)"; exit $rc

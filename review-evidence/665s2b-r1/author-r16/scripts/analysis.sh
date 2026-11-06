#!/bin/bash
# Every table and analysis of this round from the legs' graded results, into the receipts. usage: analysis.sh
set -u
S=$MANAGEMENT/2026-09-23/665s2b-a683u/scripts
T=$VALIDATION_STORAGE/665s2b-a683u
R=$MANAGEMENT/2026-09-23/665s2b-a683u/receipts
mkdir -p $R/tables $R/analysis
python3 -B $S/rows15.py $T/C $T/builds $R/tables/section13-at-5e2651d5.md "1x1/1if=N-A1,N-B1" "1x1/1if, with both drafts=D-A1,D-B1" "8x8/2if=N-A8,N-B8" "8x8/2if, with both drafts=D-A8,D-B8" > $T/logs/rows.log 2>&1; echo "rows rc=$?"
python3 -B $S/drains.py $T/builds N-A1 N-B1 D-A1 D-B1 N-A8 N-B8 D-A8 D-B8 > $R/analysis/drains.txt 2>&1; echo "drains rc=$?"
python3 -B $S/agedpasses.py $T/builds N-A1 N-B1 D-A1 D-B1 N-A8 N-B8 D-A8 D-B8 > $R/analysis/aged-passes.txt 2>&1; echo "aged rc=$?"
python3 -B $S/estimate14.py $T/C $T/builds $R/tables/estimate-32x32.md N-A1,N-B1 N-A8,N-B8 P81-A8 > $T/logs/estimate.log 2>&1; echo "estimate rc=$?"
for l in N-A1 N-B1 D-A1 D-B1 N-A8 N-B8 D-A8 D-B8 AH-A8 P81-A8; do
    python3 $S/tight.py $T/builds/$l/results/results.json 5 > $R/analysis/tight-$l.txt 2>&1
done
echo done

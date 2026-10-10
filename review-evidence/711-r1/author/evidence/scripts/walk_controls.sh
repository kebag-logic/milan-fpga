#!/usr/bin/env bash
# Scratch walker controls; each line: name, checkout, lwSRP checkout.
export TMPDIR=$SCRATCH/tmp PYTHONDONTWRITEBYTECODE=1
cd $SCRATCH
for spec in "e1 walk-e1 cand/third_party/lwSRP" "e2 walk-e2 base/third_party/lwSRP" "e3 walk-e3 base/third_party/lwSRP" "e4 walk-e4 cand/third_party/lwSRP"; do
  set -- $spec
  python3 -B scripts/quick_latency.py "$2" "quick/walk-$1" "$3" > "quick/walk-$1.log" 2>&1
  echo "$1 rc=$?" >> quick/walk-summary.txt
done
echo done >> quick/walk-summary.txt

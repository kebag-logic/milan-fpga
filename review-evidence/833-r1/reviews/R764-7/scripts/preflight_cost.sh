#!/bin/bash
# Interleaved timing of the owner controls at two exported scripts/ trees (review probe).
# Usage: preflight_cost.sh <old_tree> <new_tree> <reps> CONTROL...
old=$1 new=$2 reps=$3; shift 3
for c in "$@"; do
  for i in $(seq "$reps"); do
    for t in old new; do
      d=${!t}
      s=$(date +%s.%N); python3 -B "$d/scripts/test_suite_cancellation.py" --control "$c" >/dev/null 2>&1; rc=$?
      e=$(date +%s.%N); echo "$c $t $i rc=$rc $(echo "$e - $s" | bc)"
    done
  done
done

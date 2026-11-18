#!/bin/bash
# grade.sh TREE: flip_grade.py --check at each point in TREE, its rows, load, holds and findings.
cd $1 && for p in 1x1/1if 8x8/1if 8x8/2if; do
  out=$(python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point $p 2>&1); rc=$?
  echo "##### $p rc=$rc"
  echo "$out" | grep -E "^\| ($(echo $p | sed 's|/|\\/|')|$p) \||^(HELD|OVER|RESULT)" | cut -c1-200
  echo "$out" | grep -E "^\| $p \| [0-9.]+ \| 0\.7" | cut -c1-120
done

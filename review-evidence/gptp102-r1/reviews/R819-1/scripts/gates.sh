#!/bin/bash
# Light source gates on an extracted copy of the exact head (not a bank).
# usage: gates.sh  (run from the extracted tree's root)
set -u
for g in "make contract" "make docs" "make diagrams-check" "make lint" \
         "python3 scripts/check_docs.py --selftest" \
         "python3 scripts/check_source_evidence.py --selftest" \
         "python3 scripts/generate_diagrams.py --selftest" \
         "python3 syn/ooc/check_ooc_clock.py --selftest" \
         "make -n -C tb/verilator/engine" \
         "make -n -C tb/verilator/engine mutants-jobs-test" \
         "make -n tb"; do
  out=$($g 2>&1); rc=$?
  echo "=== rc=$rc :: $g"
  printf '%s\n' "$out" | tail -n 8
done

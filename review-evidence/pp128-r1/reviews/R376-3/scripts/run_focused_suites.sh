#!/usr/bin/env bash
# Run named processor suites from an exported tree; one tally line per suite.
# Usage: run_focused_suites.sh <exported-tree> <receipt> suite...
# Expects `verilator` on PATH to be the pinned 5.050 (through verilator_j8.sh).
set -u
tree=$1 receipt=$2; shift 2
: > "$receipt"
for s in "$@"; do
  out=$(make -C "$tree/tb/$s" 2>&1); rc=$?
  tally=$(printf '%s\n' "$out" | grep -E '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' | tail -1)
  printf '%s rc=%d %s\n' "$s" "$rc" "${tally:-NO-TALLY}" | tee -a "$receipt"
done

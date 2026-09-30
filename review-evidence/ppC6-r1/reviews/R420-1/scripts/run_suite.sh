#!/usr/bin/env bash
# Run one processor tb suite the way scripts/run_suites.sh does, logging to
# receipts/suites/<tree>-<suite>.log and appending "<tree> <suite> rc tally" to
# receipts/suites/summary.txt. Usage: run_suite.sh <tree-dir> <tree-label> <suite>...
set -uo pipefail
PKT="$(cd "$(dirname "$0")/.." && pwd)"
tree="$1"; label="$2"; shift 2
export PATH="$PKT/scratch/bin:$PATH"   # pinned Verilator 5.050, -j capped at 8
mkdir -p "$PKT/receipts/suites"
for s in "$@"; do
  log="$PKT/receipts/suites/$label-$s.log"
  start=$(date +%s)
  (cd "$tree/tb/$s" && make) >"$log" 2>&1; rc=$?
  tally=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$log" | tail -1)
  echo "$label $s rc=$rc ${tally:-NO-TALLY} $(( $(date +%s) - start ))s" | tee -a "$PKT/receipts/suites/summary.txt"
done

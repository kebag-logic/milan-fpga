#!/usr/bin/env bash
# Run named Verilator suites in an exported tree with a given verilator.
# Usage: 01_run_suites.sh <tree> <verilator> <logdir> suite...
# Prints one line per suite: PASS|FAIL <suite> <tally>. Runs at most 4 at once.
set -uo pipefail
tree=$1; vl=$2; logdir=$3; shift 3
mkdir -p "$logdir"
run_one() {
  local s=$1
  ( cd "$tree/tb/$s" && make clean >/dev/null 2>&1; make VERILATOR="$vl" ) >"$logdir/$s.log" 2>&1
  local rc=$?
  local tally; tally=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$logdir/$s.log" | tail -1)
  if [ $rc -eq 0 ]; then echo "PASS $s ($tally)"; else echo "FAIL $s rc=$rc ($tally)"; fi
}
export -f run_one; export tree vl logdir
printf '%s\n' "$@" | xargs -P 4 -I{} bash -c 'run_one {}' | sort -k2

#!/usr/bin/env bash
# Run `make` in each named tb/ suite of an exported tree, one at a time, and
# print the suite's tally line (the run_suites.sh loop body).
# usage: suite_chunk.sh <tree> <suite>...   (VERILATOR on PATH)
set -uo pipefail
tree=$1; shift
rc_all=0
for s in "$@"; do
  log=$(mktemp)
  start=$(date +%s)
  (cd "$tree/tb/$s" && make) >"$log" 2>&1; rc=$?
  tally=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$log" | tail -1)
  echo "$s | rc=$rc | ${tally:-NO TALLY} | $(( $(date +%s) - start )) s"
  [ $rc -ne 0 ] && { tail -15 "$log" | sed 's/^/    /'; rc_all=1; }
  cp "$log" "${LOGDIR:-/tmp}/suite-$s.log" 2>/dev/null
  rm -f "$log"
done
exit $rc_all

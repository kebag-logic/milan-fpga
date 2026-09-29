#!/usr/bin/env bash
# Portable: run named tb/<suite> default targets in a tree; one log per suite.
# usage: run-suite.sh <tree> <logdir> <suite>...   (VERILATOR wrapper must be first on PATH)
set -u
tree=$1; logs=$2; shift 2; mkdir -p "$logs"
for s in "$@"; do
  start=$(date +%s)
  (cd "$tree/tb/$s" && make) >"$logs/$s.log" 2>&1; rc=$?
  tally=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$logs/$s.log" | tail -1)
  echo "$s rc=$rc ${tally:-NO-TALLY} $(( $(date +%s) - start ))s"
done

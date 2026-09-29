#!/usr/bin/env bash
# Run a list of processor suites (tb/<name>) in an exported tree, at most 8 in parallel.
# usage: run_suite_subset.sh <tree> <receipt_dir> <suite>...
set -uo pipefail
tree=$1; out=$2; shift 2
mkdir -p "$out"
run_one() {
  local tree=$1 out=$2 s=$3
  local t0=$(date +%s)
  (cd "$tree/tb/$s" && make -B) > "$out/$s.log" 2>&1
  local rc=$?
  local tally=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$out/$s.log" | tail -1)
  echo "$s rc=$rc ${tally:-NO-TALLY} $(( $(date +%s) - t0 ))s"
}
export -f run_one
printf '%s\n' "$@" | xargs -P 8 -I{} bash -c 'run_one "$0" "$1" "$2"' "$tree" "$out" {} | sort > "$out/SUMMARY.txt"
cat "$out/SUMMARY.txt"

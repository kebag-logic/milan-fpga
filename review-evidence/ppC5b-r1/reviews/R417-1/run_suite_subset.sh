#!/usr/bin/env bash
# Run the named tb/<suite> directories exactly as scripts/run_suites.sh does
# (`make` in each, tally line read from the log), one at a time, restricted to
# 8 CPUs. Usage: run_suite_subset.sh <repo> <logdir> <suite>...
# Prints one PASS/FAIL line per suite with its tally; exit = failing suites.
set -uo pipefail
repo=$1; logdir=$2; shift 2
mkdir -p "$logdir"
fails=0
for name in "$@"; do
  d="$repo/tb/$name"
  [ -f "$d/Makefile" ] || { echo "MISSING $name"; fails=$((fails + 1)); continue; }
  log="$logdir/suite-$name.log"
  start=$(date +%s)
  if (cd "$d" && taskset -c 0-7 make) >"$log" 2>&1; then rc=0; else rc=$?; fi
  secs=$(( $(date +%s) - start ))
  tally=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$log" | tail -1) || tally=""
  if [ "$rc" -eq 0 ] && [ -n "$tally" ]; then
    echo "PASS $name rc=0 ($tally) ${secs}s"
  else
    echo "FAIL $name rc=$rc (${tally:-no tally}) ${secs}s"; fails=$((fails + 1))
  fi
done
exit "$fails"

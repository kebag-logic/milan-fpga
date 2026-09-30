#!/usr/bin/env bash
# Run the named tb/ suites the way scripts/run_suites.sh does (make in the suite dir,
# read the last tally line), one at a time, logging each to $OUT/suite-<name>.log.
# usage: suites_subset.sh <tree> <outdir> name...
set -uo pipefail
tree=$1; out=$2; shift 2; mkdir -p "$out"
for name in "$@"; do
  log="$out/suite-$name.log"
  start=$(date +%s)
  if (cd "$tree/tb/$name" && make) >"$log" 2>&1; then rc=0; else rc=$?; fi
  tally=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$log" | tail -1) || tally=""
  echo "$name rc=$rc tally=[$tally] secs=$(( $(date +%s) - start ))" | tee -a "$out/suites-summary.txt"
done

#!/usr/bin/env bash
# The scripts/run_suites.sh loop over a named subset of tb/ suites, same PASS and
# tally lines; run from the repository root. usage: run_subset.sh SUITE...
set -uo pipefail
fails=0; total=0
for name in "$@"; do
  d=tb/$name
  log=$(mktemp)
  if (cd "$d" && make) >"$log" 2>&1; then
    tally=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$log" | tail -1) || tally=""
    n=${tally%% *}; total=$((total + ${n:-0}))
    echo "PASS $name ($tally)"
  else
    echo "FAIL $name"; tail -20 "$log" | sed 's/^/    /'; fails=$((fails + 1))
  fi
  sed "s/^/    [$name] /" "$log" | tail -40
  rm -f "$log"
done
echo "suites: $total checks total, $fails failing"
exit "$fails"

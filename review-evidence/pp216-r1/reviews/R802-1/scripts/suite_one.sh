#!/usr/bin/env bash
# suite_one.sh TREE SUITE: the loop body of scripts/run_suites.sh for one suite
# (make in tb/SUITE; PASS with its last tally line, FAIL, or UNREADABLE).
tree=$1; name=$2; log=${3:-$(mktemp)}
if (cd "$tree/tb/$name" && make) >"$log" 2>&1; then
  tally=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$log" | tail -1) || tally=""
  if [ -z "$tally" ]; then echo "UNREADABLE $name (passed but no tally line)"; else echo "PASS $name ($tally)"; fi
else
  echo "FAIL $name"; tail -5 "$log" | sed 's/^/    /'
fi

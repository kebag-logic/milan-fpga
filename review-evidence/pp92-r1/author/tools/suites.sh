#!/usr/bin/env bash
# run_suites.sh's per-suite logic over the named suites (split for time)
set -uo pipefail
cd $LANES/pp92-93-boot-restore
export PATH=$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin:$PATH
fails=0; total=0
for name in "$@"; do
  d=tb/$name
  log=$MANAGEMENT/2026-09-23/pp92-a218/logs/suite-$name.log
  if (cd "$d" && make) >"$log" 2>&1; then
    tally=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$log" | tail -1) || tally=""
    if [ -z "$tally" ]; then echo "UNREADABLE $name"; fails=$((fails+1));
    else n=${tally%% *}; total=$((total+n)); echo "PASS $name ($tally)"; fi
  else
    echo "FAIL $name"; tail -5 "$log" | sed 's/^/    /'; fails=$((fails+1))
  fi
done
echo "batch: $total checks, $fails failing"
exit $fails

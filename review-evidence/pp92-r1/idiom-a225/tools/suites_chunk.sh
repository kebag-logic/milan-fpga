#!/usr/bin/env bash
# suites_chunk.sh SUITE... — clean-build and run each named suite exactly as
# scripts/run_suites.sh does (`cd tb/SUITE && make`), one log per suite, and
# print the suite's tally line and its compiler-warning count. Chunked so each
# call stays inside one foreground session limit; run_suites.sh itself is run
# afterwards as the gate of record.
set -uo pipefail
export PATH=$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin:$PATH
lane=$LANES/pp92-93-boot-restore
out=$REVIEWS/pp92-a225-packet/logs/suites
mkdir -p "$out"
cd "$lane" || exit 1
for name in "$@"; do
  d="tb/$name"
  (cd "$d" && make clean) > /dev/null 2>&1
  (cd "$d" && make) > "$out/suite-$name.log" 2>&1
  rc=$?
  tally=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$out/suite-$name.log" | tail -1)
  warn=$(grep -c "warning:" "$out/suite-$name.log")
  echo "rc=$rc $name ($tally) compiler-warnings=$warn" | tee -a "$out/summary.txt"
done

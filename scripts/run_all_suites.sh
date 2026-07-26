#!/usr/bin/env bash
#
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Run every Verilator testbench suite under tb/verilator/ and summarise.
#
#   scripts/run_all_suites.sh [outdir]
#
# Each suite is a directory with its own Makefile; the default target builds
# and runs every shape that suite owns (several own more than one - milan_dp
# runs legacy + N=4 + N=8, csr runs three windows). Per-suite output is written
# to <outdir>/<suite>.log so a failure can be read after the fact; the summary
# is the only thing on stdout.
#
# Exit status = number of failing suites, so CI can gate on it directly.
#
# NOTE: a run is NOT read-only on the tree. Some suites regenerate their
# `doc/TEST_RESULTS.md` evidence file, which carries a timestamp, so `git
# status` will show those as modified afterwards even when every count is
# unchanged. Commit them when the counts move; revert them when only the
# timestamp did.
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="${1:-$ROOT/.suite-logs}"
mkdir -p "$OUT"

pass=0; fail=0; failed=""
for d in "$ROOT"/tb/verilator/*/; do
  suite=$(basename "$d")
  [ -f "$d/Makefile" ] || continue
  if timeout 1800 make -C "$d" > "$OUT/$suite.log" 2>&1; then
    pass=$((pass + 1)); printf 'PASS  %s\n' "$suite"
  else
    fail=$((fail + 1)); failed="$failed $suite"; printf 'FAIL  %s\n' "$suite"
  fi
done

checks=$(grep -ho 'checks: *[0-9]*'   "$OUT"/*.log 2>/dev/null | awk '{s+=$2} END {print s+0}')
infail=$(grep -ho 'failures: *[0-9]*' "$OUT"/*.log 2>/dev/null | awk '{s+=$2} END {print s+0}')

echo "----------------------------------------------------------------"
echo "suites: $((pass + fail))   passed: $pass   failed: $fail"
echo "checks: $checks   in-suite failures: $infail"
[ -n "$failed" ] && echo "failing suites:$failed"
echo "logs: $OUT"
exit $fail

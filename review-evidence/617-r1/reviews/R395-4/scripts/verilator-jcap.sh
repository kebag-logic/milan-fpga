#!/usr/bin/env bash
# Review wrapper: the CI-pinned Verilator 5.050 with the suites' "-j 0" (all
# cores) capped at JCAP (default 2), so a 4-worker mutation arm stays within
# 8 concurrent compile jobs. REAL_VERILATOR must be a Verilator 5.050 bin/verilator.
set -euo pipefail
real="${REAL_VERILATOR:?set REAL_VERILATOR to a Verilator 5.050 bin/verilator}"
args=(); prev=""
for a in "$@"; do
  if [[ "$prev" == "-j" && "$a" == "0" ]]; then a="${JCAP:-2}"; fi
  args+=("$a"); prev="$a"
done
exec "$real" "${args[@]}"

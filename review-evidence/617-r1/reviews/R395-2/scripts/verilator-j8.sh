#!/usr/bin/env bash
# Review wrapper: run the CI-pinned Verilator 5.050 with its build parallelism
# capped at 4 jobs (two concurrent streams stay within 8) (the suite's recipes pass "-j 0" = all cores).
# REAL_VERILATOR must point at a Verilator 5.050 "bin/verilator".
set -euo pipefail
real="${REAL_VERILATOR:?set REAL_VERILATOR to a Verilator 5.050 bin/verilator}"
args=()
prev=""
for a in "$@"; do
  if [[ "$prev" == "-j" && "$a" == "0" ]]; then a=4; fi
  args+=("$a"); prev="$a"
done
exec "$real" "${args[@]}"

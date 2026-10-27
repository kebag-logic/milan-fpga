#!/usr/bin/env bash
# Run the pinned Verilator with its build parallelism capped: the bench
# Makefile passes "-j 0" (all cores); this replaces it with -j ${VL_JOBS:-4}
# so several mutant builds fit a memory cap. Usage: VERILATOR=vl-capped.sh
real=${VL_REAL:-verilator}   # this round: the pinned 5.050 (receipts/VERILATOR-IDENTITY.txt)
args=()
while [ $# -gt 0 ]; do
  if [ "$1" = "-j" ] && [ "${2:-}" = "0" ]; then args+=("-j" "${VL_JOBS:-4}"); shift 2; continue; fi
  args+=("$1"); shift
done
exec "$real" "${args[@]}"

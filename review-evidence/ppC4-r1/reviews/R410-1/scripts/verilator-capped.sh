#!/usr/bin/env bash
# Verilator wrapper for this review: rewrites a "-j 0" build-parallelism request
# to "-j ${VL_JOBS:-8}" so no build exceeds the review's job cap, then execs the
# Verilator named by VL_REAL (default: verilator on PATH).
args=(); prev=""
for a in "$@"; do
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a="${VL_JOBS:-8}"; fi
  args+=("$a"); prev="$a"
done
exec "${VL_REAL:-verilator}" "${args[@]}"

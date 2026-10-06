#!/usr/bin/env bash
# Reviewer memory guard: forward to the pinned simulator, but cap any
# "--build -j 0" (all hardware threads) at VWRAP_JOBS (default 2).
V="${PINNED_VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}"
args=(); prev=""
for a in "$@"; do
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a="${VWRAP_JOBS:-2}"; fi
  args+=("$a"); prev="$a"
done
exec "$V" "${args[@]}"

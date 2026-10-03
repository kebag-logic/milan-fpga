#!/usr/bin/env bash
# Pinned simulator with its "-j 0" (all cores) replaced by $CAPJ, so concurrent builds stay within a job budget.
PIN=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
args=(); prev=
for a in "$@"; do
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then args+=("${CAPJ:-4}"); else args+=("$a"); fi
  prev=$a
done
exec "$PIN" "${args[@]}"

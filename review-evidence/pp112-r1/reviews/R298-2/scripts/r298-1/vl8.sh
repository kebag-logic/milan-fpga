#!/usr/bin/env bash
# Pinned Verilator with build parallelism capped at 8 (rewrites "-j 0").
# Receipts were produced with VL_PINNED set to the pinned 5.050 wrapper.
VL=${VL_PINNED:?set VL_PINNED to the pinned Verilator 5.050 binary}
args=(); prev=""
for a in "$@"; do
  if [ "$prev" = "-j" ] && { [ "$a" = "0" ] || [ "$a" -gt 8 ] 2>/dev/null; }; then a=8; fi
  args+=("$a"); prev=$a
done
exec "$VL" "${args[@]}"

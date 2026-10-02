#!/bin/sh
# Pinned Verilator 5.050 with every "-j 0" capped at 8 build jobs (reviewer cap).
# VL_PIN overrides the pinned wrapper's path.
VL_PIN=${VL_PIN:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
out=""
prev=""
for a in "$@"; do
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a=8; fi
  prev="$a"
  set -- "$@" "$a"
  shift
done
exec "$VL_PIN" "$@"

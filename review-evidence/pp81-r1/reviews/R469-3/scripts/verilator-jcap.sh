#!/bin/sh
# Calls the pinned Verilator 5.050 with its build parallelism capped at $VJ
# (default 4) in place of a bench's "-j 0", so concurrent builds stay within
# the review's 16-job budget. Install as "verilator" first on PATH.
PIN=${PIN_VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
VJ=${VJ:-4}
prev=""
for a in "$@"; do
  shift
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a=$VJ; fi
  set -- "$@" "$a"
  prev=$a
done
exec "$PIN" "$@"

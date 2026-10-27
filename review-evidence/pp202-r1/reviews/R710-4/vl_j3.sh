#!/bin/sh
# Pinned Verilator 5.050 with its build parallelism capped at 3, so several
# concurrent suite builds stay within the 16-job budget.
# usage: VL_PINNED=/path/to/verilator vl_j3.sh <verilator args...>
pinned=${VL_PINNED:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
prev=""
for a in "$@"; do
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a=3; fi
  prev=$a
  set -- "$@" "$a"
  shift
done
exec "$pinned" "$@"

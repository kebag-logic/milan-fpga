#!/bin/sh
# Pinned Verilator 5.050 with its build parallelism capped (replaces "-j 0").
# VL_REAL: the pinned launcher; VL_J: threads per build (default 3).
VL_REAL=${VL_REAL:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
VL_J=${VL_J:-3}
n=$#; i=0; prev=""
for a in "$@"; do
  i=$((i+1))
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a=$VL_J; fi
  set -- "$@" "$a"; prev=$a
done
shift $n
exec "$VL_REAL" "$@"

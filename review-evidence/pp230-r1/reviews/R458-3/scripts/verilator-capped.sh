#!/bin/sh
# Pinned Verilator 5.050 with its build parallelism capped at 2 (replaces "-j 0" / "-j N").
# usage: put a symlink named "verilator" to this file first on PATH; set PINNED_VERILATOR.
V=${PINNED_VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
out=""; skip=0
for a in "$@"; do
  if [ $skip = 1 ]; then set -- "$@" 2; skip=0; shift; continue; fi
  if [ "$a" = "-j" ]; then set -- "$@" -j; skip=1; shift; continue; fi
  set -- "$@" "$a"; shift
done
exec "$V" "$@"

#!/bin/sh
# Pinned Verilator 5.050 with any "-j N" build-jobs request capped at 4.
V=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
out=""
skip=0
for a in "$@"; do
  if [ "$skip" = 1 ]; then set -- "$@" 4; skip=0; shift; continue; fi
  if [ "$a" = "-j" ]; then set -- "$@" "-j"; skip=1; shift; continue; fi
  set -- "$@" "$a"; shift
done
exec "$V" "$@"

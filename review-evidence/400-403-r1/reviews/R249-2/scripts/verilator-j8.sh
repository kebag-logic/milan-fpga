#!/bin/sh
# Calls the scoped Verilator 5.050 (path in $PINNED_VERILATOR) with any
# "-j 0" build parallelism capped at 8, so a probe never exceeds 8 jobs.
set -u
: "${PINNED_VERILATOR:?set PINNED_VERILATOR to the scoped verilator 5.050}"
n=$#; i=0; prev=""
for a in "$@"; do
  i=$((i+1))
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a=8; fi
  set -- "$@" "$a"; prev=$a
done
shift "$n"
exec "$PINNED_VERILATOR" "$@"

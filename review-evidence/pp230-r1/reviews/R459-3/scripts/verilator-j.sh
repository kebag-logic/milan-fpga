#!/bin/sh
# Pinned Verilator 5.050 with the build's "-j 0" (all cores) replaced by
# -j ${VJ:-2}, so concurrent suite builds stay inside the job budget.
V=${PINNED_VERILATOR:?set PINNED_VERILATOR to the pinned Verilator 5.050}
n=$#; i=0; prev=
for a in "$@"; do
  i=$((i+1))
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a=${VJ:-2}; fi
  set -- "$@" "$a"; prev=$a
done
shift $n
exec "$V" "$@"

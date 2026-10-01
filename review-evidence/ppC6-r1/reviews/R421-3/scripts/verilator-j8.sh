#!/bin/sh
# Pinned Verilator 5.050 with the build parallelism capped: rewrites "-j 0"
# (all cores) to "-j ${VJOBS:-8}"; every other argument passes through.
# PIN_VERILATOR must name the pinned verilator executable.
PIN="${PIN_VERILATOR:?set PIN_VERILATOR to the pinned verilator}"
n=$#; prev=""
for a in "$@"; do
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a="${VJOBS:-8}"; fi
  set -- "$@" "$a"; prev="$a"
done
shift $n
exec "$PIN" "$@"

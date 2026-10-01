#!/bin/sh
# Pinned Verilator 5.050 with the build parallelism capped at 8 jobs:
# rewrites "-j 0" (all cores) to "-j ${VJOBS:-8}"; every other argument passes through.
PIN="${PIN_VERILATOR:-$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator}"
n=$#; i=0; prev=""
for a in "$@"; do
  i=$((i+1))
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a="${VJOBS:-8}"; fi
  set -- "$@" "$a"; prev="$a"
done
shift $n
exec "$PIN" "$@"

#!/bin/sh
# Run the pinned Verilator ($PINNED_VERILATOR) with any "-j 0" build-jobs
# request capped at $VL_JOBS (default 8) parallel jobs.
: "${PINNED_VERILATOR:?set PINNED_VERILATOR to the pinned verilator wrapper}"
n=$#; i=0; prev=""
for a in "$@"; do
  i=$((i+1))
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a="${VL_JOBS:-8}"; fi
  set -- "$@" "$a"; prev="$a"
done
shift "$n"
exec "$PINNED_VERILATOR" "$@"

#!/bin/sh
# Run the pinned Verilator with every "-j 0" build capped at ${VCAP:-8} jobs.
# REAL_VERILATOR must name the pinned binary (verified by version and sha256).
real="${REAL_VERILATOR:?set REAL_VERILATOR}"
cap="${VCAP:-8}"
n=$#; i=0; prev=""
for a in "$@"; do
  i=$((i+1))
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a="$cap"; fi
  set -- "$@" "$a"; prev="$a"
done
shift "$n"
exec "$real" "$@"

#!/bin/sh
# Reviewer wrapper: run the pinned Verilator 5.050, capping its build make at 8
# jobs, or VERILATOR_BUILD_JOBS (rewrites "-j 0"); every other argument passes through.
REAL="${PINNED_VERILATOR:?set PINNED_VERILATOR to the pinned verilator}"
n=$#; i=0; prev=""
for a in "$@"; do
  i=$((i+1))
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a="${VERILATOR_BUILD_JOBS:-8}"; fi
  set -- "$@" "$a"; prev="$a"
done
shift "$n"
exec "$REAL" "$@"

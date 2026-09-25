#!/bin/sh
# Forward to the pinned Verilator 5.050 wrapper, capping its build parallelism
# at 8 jobs (rewrites "-j 0" or "-j N>8" to "-j 8"). Path of the pinned wrapper
# comes from PINNED_VERILATOR.
: "${PINNED_VERILATOR:?set PINNED_VERILATOR}"
out=""
prev=""
for a in "$@"; do
  if [ "$prev" = "-j" ]; then
    case "$a" in 0|9|1[0-9]|[2-9][0-9]) a=8 ;; esac
  fi
  set -- "$@" "$a"
  prev="$a"
done
# drop the original arguments (first half)
n=$(( $# / 2 )); shift $n
exec "$PINNED_VERILATOR" "$@"

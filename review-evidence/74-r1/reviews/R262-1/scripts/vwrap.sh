#!/bin/sh
# Reviewer wrapper: calls the pinned Verilator 5.050 and caps its --build
# parallelism at 8 (rewrites "-j 0" to "-j 8"). PINNED_VERILATOR must be set.
: "${PINNED_VERILATOR:?set PINNED_VERILATOR to the pinned verilator}"
out=""
prev=""
for a in "$@"; do
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a=8; fi
  prev="$a"
  set -- "$@" "$a"
done
# drop the original argument copy (first half)
n=$(( $# / 2 ))
shift $n
exec "$PINNED_VERILATOR" "$@"

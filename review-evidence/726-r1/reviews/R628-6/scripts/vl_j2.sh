#!/bin/sh
# Pinned Verilator with any "-j N" build-parallelism argument forced to 2.
out=""
for a in "$@"; do
  if [ "$prev" = "-j" ]; then a=2; fi
  prev=$a
  set -- "$@" "$a"
done
# drop the original arguments (first half)
n=$(( $# / 2 )); shift $n
exec "${PINNED_VERILATOR:?set PINNED_VERILATOR to the verified 5.050 executable}" "$@"

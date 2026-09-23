#!/bin/sh
# Verilator wrapper: forwards to the pinned 5.050 wrapper, replacing the
# suites' "--build -j 0" (all cores) with "-j 2" so four concurrent suites
# stay within eight jobs. Set PINNED_VERILATOR to the pinned wrapper path.
: "${PINNED_VERILATOR:?set PINNED_VERILATOR}"
out=""
skip=0
for a in "$@"; do
  if [ "$skip" = 1 ]; then skip=0; set -- "$@" "2"; continue; fi
  if [ "$a" = "-j" ]; then skip=1; set -- "$@" "-j"; continue; fi
  set -- "$@" "$a"
done
# drop the original arguments (first half)
n=$(( $# / 2 ))
shift "$n"
exec "$PINNED_VERILATOR" "$@"

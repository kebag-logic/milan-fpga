#!/bin/sh
# Reviewer wrapper: forwards to the pinned Verilator 5.050 and caps build
# parallelism at 8 (the harness Makefile passes "-j 0", meaning all CPUs).
# Set PINNED_VERILATOR to the pinned executable.
: "${PINNED_VERILATOR:?set PINNED_VERILATOR}"
prev=""
for a in "$@"; do
  shift
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a=8; fi
  set -- "$@" "$a"
  prev="$a"
done
exec "$PINNED_VERILATOR" "$@"

#!/bin/sh
# Pinned-Verilator wrapper that caps the build's parallelism at 8 jobs
# (the suites pass "-j 0", meaning every core). PINNED_VERILATOR must name
# the pinned Verilator 5.050 launcher.
set -eu
: "${PINNED_VERILATOR:?set PINNED_VERILATOR}"
n=$#; i=0; prev=
for a in "$@"; do
  i=$((i+1))
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a=8; fi
  set -- "$@" "$a"; prev=$a
done
shift "$n"
exec "$PINNED_VERILATOR" "$@"

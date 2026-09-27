#!/usr/bin/env bash
# Pinned Verilator 5.050 launcher that caps a "-j 0" (all cores) build request to 8 jobs.
# Set VERILATOR_PREFIX to the install prefix holding bin/verilator and share/verilator.
: "${VERILATOR_PREFIX:?set VERILATOR_PREFIX to a Verilator 5.050 install prefix}"
args=(); prev=
for a in "$@"; do
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a=8; fi
  args+=("$a"); prev=$a
done
exec env VERILATOR_ROOT="$VERILATOR_PREFIX/share/verilator" "$VERILATOR_PREFIX/bin/verilator" "${args[@]}"

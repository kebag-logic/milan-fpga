#!/bin/sh
# Verilator wrapper that caps the recipe's `-j 0` (all cores) at 8 jobs.
# Usage: VERILATOR=/path/to/verilator_cap8.sh make -C <suite>
# REAL_VERILATOR names the identified binary (default: `verilator` on PATH).
real=${REAL_VERILATOR:-verilator}
out=""
prev=""
for a in "$@"; do
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a=8; fi
  out="$out '$(printf %s "$a" | sed "s/'/'\\\\''/g")'"
  prev=$a
done
eval "exec \"\$real\" $out"

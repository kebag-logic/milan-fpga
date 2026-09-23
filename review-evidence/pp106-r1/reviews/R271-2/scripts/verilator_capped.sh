#!/bin/sh
# Pass-through wrapper for the pinned simulator that caps its build
# parallelism: any "-j <n>" becomes "-j ${VL_JOBS:-2}". Set REAL_VERILATOR.
: "${REAL_VERILATOR:?set REAL_VERILATOR to the pinned simulator wrapper}"
j=${VL_JOBS:-2}
out=""
prev=""
for a in "$@"; do
  if [ "$prev" = "-j" ]; then a=$j; fi
  prev=$a
  out="$out$(printf '%s' "$a" | sed "s/'/'\\\\''/g; s/^/'/; s/\$/'/") "
done
eval "exec \"\$REAL_VERILATOR\" $out"

#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Run the pinned simulator with its build parallelism capped: every suite
# Makefile passes "--build -j 0" (all host cores); this rewrites that to
# "-j $VL_JOBS" (default 8) so a probe never exceeds the round's job budget.
# PINNED_VERILATOR must name the pinned 5.050 launcher.
set -eu
: "${PINNED_VERILATOR:?set PINNED_VERILATOR to the pinned simulator launcher}"
jobs="${VL_JOBS:-8}"
out=""
prev=""
for a in "$@"; do
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a="$jobs"; fi
  out="$out $(printf '%s' "$a" | sed "s/'/'\\\\''/g; s/^/'/; s/\$/'/")"
  prev="$a"
done
eval "exec \"\$PINNED_VERILATOR\" $out"

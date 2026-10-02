#!/bin/sh
# Pinned Verilator 5.050 with every "-j N" build-jobs request capped at 8.
REAL=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
out=""
prev=""
for a in "$@"; do
  if [ "$prev" = "-j" ] || [ "$prev" = "--build-jobs" ]; then
    if [ "$a" = "0" ] || [ "$a" -gt 8 ] 2>/dev/null; then a=8; fi
  fi
  out="$out$(printf '%s' "$a" | sed "s/'/'\\\\''/g; s/^/'/; s/\$/'/") "
  prev="$a"
done
eval "exec \"\$REAL\" $out"

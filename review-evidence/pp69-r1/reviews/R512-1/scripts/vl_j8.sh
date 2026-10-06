#!/bin/bash
# Pinned Verilator 5.050 with "-j 0" rewritten to "-j 8" (memory budget only;
# no other argument changes). PINNED_VERILATOR overrides the binary path.
V=${PINNED_VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
args=()
prev=""
for a in "$@"; do
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a=8; fi
  args+=("$a"); prev="$a"
done
exec "$V" "${args[@]}"

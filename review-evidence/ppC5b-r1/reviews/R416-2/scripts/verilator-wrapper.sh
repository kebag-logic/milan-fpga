#!/usr/bin/env bash
# Pinned-Verilator wrapper used for every build in this packet. Set
# VERILATOR_PINNED_ROOT to the install prefix of the scoped Verilator 5.050
# (it holds bin/verilator and share/verilator). The bench Makefiles pass
# Verilator `-j 0` (every core); this wrapper caps that at 8 jobs.
: "${VERILATOR_PINNED_ROOT:?set VERILATOR_PINNED_ROOT}"
args=(); prev=""
for a in "$@"; do
  if [ "$prev" = "-j" ] && { [ "$a" = "0" ] || [ "$a" -gt 8 ] 2>/dev/null; }; then a=8; fi
  args+=("$a"); prev="$a"
done
exec env VERILATOR_ROOT="$VERILATOR_PINNED_ROOT/share/verilator" \
  "$VERILATOR_PINNED_ROOT/bin/verilator" "${args[@]}"

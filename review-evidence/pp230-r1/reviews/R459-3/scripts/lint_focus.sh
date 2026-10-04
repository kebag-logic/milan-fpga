#!/usr/bin/env bash
# Verilator lint (the repository's flags) of the changed SRP modules at shapes
# 1, 2, 3, 5, 9 and the default, with the whole hdl/ tree visible.
# usage: lint_focus.sh <tree> <log>
set -u
T=$1; LOG=$(readlink -f "$2"); V=${PINNED_VERILATOR:?set PINNED_VERILATOR to the pinned Verilator 5.050}
cd "$T" || exit 2
pkgs=$(find hdl -name '*_pkg.sv' | sort); all=$(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort)
rc=0; : > "$LOG"
for top in KL_srp_talker_fsm:N_SOURCES_P KL_srp_listener_fsm:N_SINKS_P KL_srp_admission:N_SOURCES_P KL_srp_top:N_SOURCES_P,N_SINKS_P; do
  m=${top%%:*}; ps=${top#*:}
  for n in default 1 2 3 5 9; do
    g=""; if [ $n != default ]; then for p in ${ps//,/ }; do g="$g -G$p=$n"; done; fi
    out=$($V --lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --top-module $m $g $pkgs $all 2>&1); r=$?
    if [ $r -ne 0 ] || grep -qE '%(Warning|Error)' <<<"$out"; then echo "LINT FAIL $m $n rc=$r" >> "$LOG"; echo "$out" | head -8 >> "$LOG"; rc=1
    else echo "LINT OK $m $n" >> "$LOG"; fi
  done
done
echo "rc=$rc" >> "$LOG"; exit $rc

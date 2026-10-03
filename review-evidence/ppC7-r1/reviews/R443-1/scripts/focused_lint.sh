#!/usr/bin/env bash
# Focused lint (the flags of scripts/lint_hdl.sh) of the two RTL modules this PR changes
set -uo pipefail
cd "$1" || exit 2
pkgs=$(find hdl -name '*_pkg.sv' | sort); all=$(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort)
rc=0
for top in KL_adp_engine protocol_processor_top; do
  out=$(verilator --lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --top-module "$top" $pkgs $all 2>&1); r=$?
  if [ $r -ne 0 ] || grep -qE '%(Warning|Error)' <<<"$out"; then echo "LINT FAIL $top rc=$r"; echo "$out" | head; rc=1; else echo "LINT OK $top"; fi
done
exit $rc

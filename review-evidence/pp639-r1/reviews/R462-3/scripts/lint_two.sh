#!/bin/bash
# Scoped lint of the two modules the lane changes, with lint_hdl.sh's exact
# flags and file set, using the verilator given as $2. Usage: lint_two.sh TREE VERILATOR
set -uo pipefail
cd "$1"; V=$2
pkgs=$(find hdl -name '*_pkg.sv' | sort); all=$(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort)
rc=0
for top in KL_pp_acmp_listener protocol_processor_top; do
  out=$($V --lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --top-module "$top" $pkgs $all 2>&1); r=$?
  if [ $r -ne 0 ] || grep -qE '%(Warning|Error)' <<<"$out"; then echo "LINT FAIL $top (rc $r)"; grep -E '%(Warning|Error)' <<<"$out" | head -5; rc=1; else echo "LINT OK  $top"; fi
done
exit $rc

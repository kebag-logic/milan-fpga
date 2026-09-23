#!/usr/bin/env bash
# Verilator --lint-only (the donor lint flags, whole tree visible) over the six
# RTL files this PR changes, each elaborated as its own top. Focused, not the
# full lint bank. Usage: 07_lint_changed.sh <tree> <verilator>
set -uo pipefail
tree=$1; vl=$2; cd "$tree" || exit 2
pkgs=$(find hdl -name '*_pkg.sv' | sort)
all=$(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort)
rc=0
for top in KL_srp_decoder KL_srp_encoder KL_srp_listener_fsm KL_srp_talker_fsm KL_srp_top; do
  # shellcheck disable=SC2086
  if ! out=$("$vl" --lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
             -Wno-UNUSEDPARAM --top-module "$top" $pkgs $all 2>&1); then
    echo "LINT ERROR $top"; echo "$out" | tail -5; rc=1
  elif grep -qE '%(Warning|Error)' <<<"$out"; then
    echo "LINT FAIL $top"; grep -E '%(Warning|Error)' <<<"$out" | head -5; rc=1
  else
    echo "LINT OK  $top"
  fi
done
# srp_pkg.sv is linted through every top above (it is in $pkgs)
exit "$rc"

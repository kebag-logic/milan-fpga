#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Focused lint of the SRP modules this PR changes, with the flags of
# scripts/lint_hdl.sh (whole hdl/ tree visible, each module its own top).
# The verdict is the tool's exit status plus the absence of %Warning/%Error.
# usage: focused_srp_lint.sh TREE   (env PINNED_VERILATOR required)
set -euo pipefail
: "${PINNED_VERILATOR:?set PINNED_VERILATOR}"
cd "$1"
"$PINNED_VERILATOR" --version
pkgs=$(find hdl -name '*_pkg.sv' | sort)
all=$(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort)
rc=0
for top in KL_srp_decoder KL_srp_encoder KL_srp_top KL_srp_talker_fsm KL_srp_listener_fsm; do
  # shellcheck disable=SC2086 # deliberate word split of the file lists
  if ! out=$("$PINNED_VERILATOR" --lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
             -Wno-UNUSEDPARAM --top-module "$top" $pkgs $all 2>&1); then
    echo "LINT ERROR $top"; echo "$out" | tail -5; rc=1
  elif grep -qE '%(Warning|Error)' <<<"$out"; then
    echo "LINT FAIL $top"; grep -E '%(Warning|Error)' <<<"$out" | head -5 || true; rc=1
  else
    echo "LINT OK  $top"
  fi
done
echo "exit $rc"
exit "$rc"

#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reviewer receipt script: the donor's zero-tolerance lint (the exact flags of
# scripts/lint_hdl.sh, whole tree visible) scoped to the modules PR #107
# changes. Usage: lint_changed.sh <tree> <verilator-wrapper-dir>
set -uo pipefail
tree=${1:?tree}; vbin=${2:?verilator dir}
export PATH="$vbin:$PATH"
cd "$tree" || exit 2
verilator --version
pkgs=$(find hdl -name '*_pkg.sv' | sort)
all=$(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort)
rc=0
for top in KL_srp_decoder KL_srp_encoder KL_srp_talker_fsm KL_srp_listener_fsm KL_srp_top; do
  # shellcheck disable=SC2086 # deliberate word split of the file lists
  out=$(verilator --lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
        -Wno-UNUSEDPARAM --top-module "$top" $pkgs $all 2>&1); st=$?
  if [ "$st" -ne 0 ]; then echo "LINT ERROR $top"; echo "$out" | tail -5; rc=1
  elif grep -qE '%(Warning|Error)' <<<"$out"; then
    echo "LINT FAIL $top"; grep -E '%(Warning|Error)' <<<"$out" | head -5; rc=1
  else echo "LINT OK  $top"; fi
done
exit "$rc"

#!/usr/bin/env bash
# R294 scoped lint: the repository's own lint flags (scripts/lint_hdl.sh),
# restricted to the modules this PR changes, at the default shape and with
# shape overrides (-G) for the top at 1x1 and 8x8 and the sink-parameterised
# modules at one sink. Verdict = tool exit status AND no %Warning/%Error.
# Usage: scoped_lint.sh <extracted-tree>
set -uo pipefail
tree=$1
V=${PINNED_VERILATOR:-$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator}
cd "$tree" || exit 2
pkgs=$(find hdl -name '*_pkg.sv' | sort)
all=$(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort)
rc=0
lint() {  # <label> <top> [-G...]
  local label=$1 top=$2; shift 2
  # shellcheck disable=SC2086
  if ! out=$("$V" --lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
             -Wno-UNUSEDPARAM --top-module "$top" "$@" $pkgs $all 2>&1); then
    echo "LINT ERROR $label"; echo "$out" | tail -5; rc=1
  elif grep -qE '%(Warning|Error)' <<<"$out"; then
    echo "LINT FAIL $label"; grep -E '%(Warning|Error)' <<<"$out" | head -5; rc=1
  else
    echo "LINT OK  $label"
  fi
}
lint "protocol_processor_top default" protocol_processor_top
lint "protocol_processor_top 1x1" protocol_processor_top -GN_STREAM_IN_P=1 -GN_STREAM_OUT_P=1
lint "protocol_processor_top 8x8" protocol_processor_top -GN_STREAM_IN_P=8 -GN_STREAM_OUT_P=8
lint "KL_srp_listener_fsm default" KL_srp_listener_fsm
lint "KL_srp_listener_fsm 1 sink" KL_srp_listener_fsm -GN_SINKS_P=1
lint "KL_srp_top default" KL_srp_top
lint "KL_srp_top 1 sink" KL_srp_top -GN_SINKS_P=1
lint "KL_pp_acmp_listener default" KL_pp_acmp_listener
lint "KL_pp_acmp_listener 1 sink" KL_pp_acmp_listener -GN_SINKS_P=1
lint "KL_aecp_engine default" KL_aecp_engine
echo "scoped lint rc=$rc"
exit "$rc"

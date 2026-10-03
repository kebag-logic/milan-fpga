#!/usr/bin/env bash
# lint_hdl.sh's flags (verilator --lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL
# -Wno-UNUSEDPARAM, every hdl file) on the port and the top at the head, at the
# default deadline and at legal and refused values. usage: lint_changed.sh EXPORT VERILATOR
set -u
cd "$1"; V=$2
pkgs=$(find hdl -name '*_pkg.sv' | sort); all=$(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort)
run() { # tag top extra
  out=$($V --lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --top-module "$2" $3 $pkgs $all 2>&1); rc=$?
  n=$(printf '%s\n' "$out" | grep -c '%Warning\|%Error')
  echo "$1 rc=$rc warnings_or_errors=$n $(printf '%s\n' "$out" | grep -m1 'USERERROR' | sed 's/^.*USERERROR: //' | cut -c1-120)"
}
run port_default KL_pp_nvm_port ""
for t in 1 2 3 37 2147483647; do run port_tmo$t KL_pp_nvm_port "-GMEM_TIMEOUT_CYC_P=$t"; done
run port_tmo2p31_refused KL_pp_nvm_port "-GMEM_TIMEOUT_CYC_P=2147483648"
run port_maxp65527 KL_pp_nvm_port "-GMAX_PAYLOAD_P=65527"
run top_default protocol_processor_top ""
run arb_default KL_pp_nvm_mgr_arb ""

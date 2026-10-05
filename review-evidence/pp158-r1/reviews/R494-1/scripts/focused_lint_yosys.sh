#!/bin/bash
# Focused lint (lint_hdl.sh's exact verilator command) of KL_aecp_notify and
# protocol_processor_top at a tree, and a focused yosys synth_xilinx of
# KL_aecp_notify alone (default parameters) for a LUT/FF proxy.
# Usage: focused_lint_yosys.sh TREE OUTPREFIX VERILATOR
set -u
T=$1 O=$2 V=$3
cd "$T"
pkgs=$(find hdl -name '*_pkg.sv' | sort); all=$(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort)
for top in KL_aecp_notify protocol_processor_top; do
  out=$("$V" --lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --top-module $top $pkgs $all 2>&1); rc=$?
  if [ $rc -ne 0 ]; then echo "LINT ERROR $top"; elif grep -qE '%(Warning|Error)' <<<"$out"; then echo "LINT FAIL $top"; grep -E '%(Warning|Error)' <<<"$out" | head; else echo "LINT OK  $top"; fi
done > "$O-lint.log"
sv2v hdl/common/pp_pkg.sv hdl/aecp/KL_aecp_notify.sv > "$O-notify.v"
yosys -q -p "read_verilog -sv $O-notify.v; synth_xilinx -top KL_aecp_notify -flatten; tee -o $O-yosys-stat.txt stat" > "$O-yosys.log" 2>&1; echo "yosys rc $?" >> "$O-yosys.log"

#!/usr/bin/env bash
# Usage: area.sh TREE TOP NSRC NSNK OUTDIR
# sv2v every hdl source of TREE, then yosys 0.66 synth_xilinx -family xc7 -flatten on TOP
# with N_SOURCES_P / N_SINKS_P set (KL_srp_top) or N_SINKS_P only (KL_srp_listener_fsm).
set -euo pipefail
tree=$1; top=$2; ns=$3; nk=$4; out=$5
mkdir -p "$out"
cd "$tree"
sv2v $(find hdl -name '*_pkg.sv' | sort) $(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort) > "$out/all.v"
if [ "$top" = KL_srp_top ]; then cp="chparam -set N_SOURCES_P $ns -set N_SINKS_P $nk $top"; else cp="chparam -set N_SINKS_P $nk $top"; fi
yosys -q -l "$out/yosys.log" -p "read_verilog -sv -defer $out/all.v; $cp; hierarchy -top $top; synth_xilinx -family xc7 -flatten -top $top; tee -o $out/stat.txt stat" >/dev/null
grep -E "LUT|FD|INV|RAM|MUXF|CARRY|cells" "$out/stat.txt" | head -40

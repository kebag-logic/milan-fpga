#!/bin/bash
# yosys_fsm_area_1x1.sh TREE : as yosys_fsm_area.sh, with N_SOURCES_P / N_SINKS_P = 1
# (the shipping 1x1 shape). Indicative only (generic synth_xilinx, not Vivado OOC).
set -euo pipefail
tree=$1; work=$(mktemp -d "${TMPDIR:-/tmp}/r488-ys-XXXX")
cd "$tree"
sv2v hdl/common/pp_pkg.sv hdl/srp/srp_pkg.sv hdl/srp/KL_srp_talker_fsm.sv hdl/srp/KL_srp_listener_fsm.sv > "$work/fsm.v"
for spec in KL_srp_talker_fsm:N_SOURCES_P KL_srp_listener_fsm:N_SINKS_P; do
  top=${spec%%:*}; par=${spec##*:}
  yosys -q -p "read_verilog $work/fsm.v; chparam -set $par 1 $top; synth_xilinx -top $top -flatten; tee -o $work/$top.stat stat" >/dev/null
  luts=$(awk '$2 ~ /^LUT[1-6]$/ {s+=$1} END{print s+0}' "$work/$top.stat")
  ffs=$(awk '$2 ~ /^FD[CPRS]E?$/ {s+=$1} END{print s+0}' "$work/$top.stat")
  echo "$top($par=1) LUT=$luts FF=$ffs"
done
rm -rf "$work"

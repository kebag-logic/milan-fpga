#!/bin/bash
# yosys_fsm_area.sh TREE : sv2v + yosys synth_xilinx of the two SRP stream FSMs at
# default parameters; prints LUT/FF cell totals. Indicative only (not Vivado OOC).
set -euo pipefail
tree=$1; work=$(mktemp -d "${TMPDIR:-/tmp}/r488-ys-XXXX")
cd "$tree"
sv2v hdl/common/pp_pkg.sv hdl/srp/srp_pkg.sv hdl/srp/KL_srp_talker_fsm.sv hdl/srp/KL_srp_listener_fsm.sv > "$work/fsm.v"
for top in KL_srp_talker_fsm KL_srp_listener_fsm; do
  yosys -q -p "read_verilog $work/fsm.v; synth_xilinx -top $top -flatten; tee -o $work/$top.stat stat" >/dev/null
  luts=$(awk '$2 ~ /^LUT[1-6]$/ {s+=$1} END{print s+0}' "$work/$top.stat")
  ffs=$(awk '$2 ~ /^FD[CPRS]E?$/ {s+=$1} END{print s+0}' "$work/$top.stat")
  echo "$top LUT=$luts FF=$ffs"
done
rm -rf "$work"

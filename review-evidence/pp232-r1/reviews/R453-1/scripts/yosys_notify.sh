#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# yosys_notify.sh TREE OUTDIR : sv2v + yosys synth_xilinx of KL_aecp_notify alone
# (default parameters), printing the cell census. A portability cross-check of RAM
# inference only; it is not the Vivado measurement the issue's criteria name.
set -eu
tree=$1; out=$2
mkdir -p "$out"
sv2v "$tree/hdl/common/pp_pkg.sv" "$tree/hdl/aecp/KL_aecp_notify.sv" > "$out/notify.v"
yosys -q -l "$out/yosys.log" -p "read_verilog -sv $out/notify.v; synth_xilinx -top KL_aecp_notify -family xc7 -noiopad; tee -o $out/stat.txt stat" > /dev/null
grep -E 'RAM|FDRE|FDSE|FDCE|FDPE|LUT[1-6]|MUXF|CARRY|cells' "$out/stat.txt"

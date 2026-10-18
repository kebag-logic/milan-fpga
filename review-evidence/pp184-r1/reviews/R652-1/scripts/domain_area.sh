#!/bin/sh
# Module-only area of KL_srp_domain at a git revision (sv2v + yosys
# synth_xilinx -family xc7 -flatten, as the processor's OOC flow prices).
# usage: domain_area.sh <repo> <rev> <workdir>
set -eu
REPO=$1; REV=$2; W=$3; mkdir -p "$W"
git -C "$REPO" show "$REV:hdl/srp/KL_srp_domain.sv" > "$W/KL_srp_domain.sv"
sv2v "$W/KL_srp_domain.sv" > "$W/dom.v"
cd "$W" && yosys -q -p "read_verilog $W/dom.v; synth_xilinx -family xc7 -flatten -top KL_srp_domain; tee -o $W/stat.txt stat" > "$W/yosys.log" 2>&1
grep -E "LUT[1-6]|FD[RSCPE]+|CARRY4|cells" "$W/stat.txt"

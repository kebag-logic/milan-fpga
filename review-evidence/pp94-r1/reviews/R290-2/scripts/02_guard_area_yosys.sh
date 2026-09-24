#!/usr/bin/env bash
# Independent single-module area cross-check of the guard (not the repository's Yosys bank).
# Usage: PACKET=<packet> bash 02_guard_area_yosys.sh
set -eu
T=$PACKET/scratch/head; O=$PACKET/scratch/area; R=$PACKET/receipts
mkdir -p "$O"
sv2v "$T/hdl/aecp/KL_aecp_desc_mem_guard.sv" > "$O/guard.v"
yosys -V > "$R/09-yosys-version.txt"; sv2v --version >> "$R/09-yosys-version.txt"
yosys -q -p "read_verilog $O/guard.v; synth_xilinx -family xc7 -top KL_aecp_desc_mem_guard -flatten; tee -o $R/09-guard-area-stat.txt stat" \
  > "$R/09-guard-area-yosys.log" 2>&1
grep -E "LUT|FD|cells" "$R/09-guard-area-stat.txt"

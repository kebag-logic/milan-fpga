#!/usr/bin/env bash
# Reviewer cross-check (R514-1, #667): flattened xc7 area of KL_aaf_packetizer
# alone at the shipping 1x1 TDM8 shape (N_TALKERS_P=1, WIRE_CHANS_P=8).
# usage: yosys_area.sh RTL OUTDIR
set -euo pipefail
rtl="$1"; out="$2"; mkdir -p "$out"
sha256sum "$rtl"
sv2v "$rtl" > "$out/pk.v"
yosys -q -l "$out/yosys.log" -p "read_verilog $out/pk.v; chparam -set N_TALKERS_P 1 -set WIRE_CHANS_P 8 KL_aaf_packetizer; synth_xilinx -family xc7 -flatten -top KL_aaf_packetizer; tee -o $out/stat.txt stat" >/dev/null
grep -E "LUT[1-6]|FD[CPRS]E|RAMB|Number of cells|cells$" "$out/stat.txt"

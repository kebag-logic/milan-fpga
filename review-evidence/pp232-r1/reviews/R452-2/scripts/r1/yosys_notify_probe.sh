#!/usr/bin/env bash
# Focused cross-check (not the repository's Yosys gate): synthesize KL_aecp_notify
# alone for Xilinx 7-series with Yosys at the 16/2/2 shape, from one commit, and
# print the cell census, so the row table's and the index's primitives can be
# compared with the Vivado figures the author reports.
# Usage: yosys_notify_probe.sh REPO COMMIT OUTDIR
set -euo pipefail
repo=$1; commit=$2; out=$3
mkdir -p "$out"
git -C "$repo" show "$commit:hdl/common/pp_pkg.sv" >"$out/pp_pkg.sv"
git -C "$repo" show "$commit:hdl/aecp/KL_aecp_notify.sv" >"$out/KL_aecp_notify.sv"
sv2v "$out/pp_pkg.sv" "$out/KL_aecp_notify.sv" >"$out/all.v"
yosys -q -l "$out/yosys.log" -p "read_verilog $out/all.v; \
  chparam -set N_CTRL_P 16 -set N_STREAM_IN_P 2 -set N_STREAM_OUT_P 2 KL_aecp_notify; \
  synth_xilinx -family xc7 -top KL_aecp_notify -flatten; \
  tee -o $out/stat.txt stat"
grep -E 'RAM|FD[RSCP]E|LUT[1-6]|CARRY4|cells' "$out/stat.txt"

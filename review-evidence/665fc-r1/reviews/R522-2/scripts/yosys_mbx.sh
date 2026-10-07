#!/usr/bin/env bash
# Reviewer probe: sv2v + Yosys generic synth of the mailbox tops from an exported tree.
# usage: yosys_mbx.sh <tree> <outdir>
set -eu
T=$1; O=$2; mkdir -p "$O"
M=$T/hdl/milan/mailbox
for top in KL_mbx KL_mbx_wb KL_mbx_axil; do
  sv2v $M/KL_mbx_pkg.sv $M/KL_mbx_ring.sv $M/KL_mbx_rx.sv $M/KL_mbx_tx.sv $M/KL_mbx_evt.sv $M/KL_mbx.sv $M/KL_mbx_wb.sv $M/KL_mbx_axil.sv > "$O/mbx_$top.v"
  rc=0; yosys -q -p "read_verilog -sv $O/mbx_$top.v; hierarchy -check -top $top; proc; flatten; synth -top $top; check -assert; tee -q -o $O/stat_$top.txt stat" > "$O/yosys_$top.log" 2>&1 || rc=$?
  echo "$top rc=$rc"
done

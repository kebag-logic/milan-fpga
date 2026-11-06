#!/bin/sh
# ltp.sh <tree> <tag> <outdir>: logic-depth estimate of KL_srp_encoder (Yosys ltp after synth_xilinx)
T=$1; G=$2; O=$3
sv2v --top=KL_srp_encoder "$T/hdl/common/pp_pkg.sv" "$T/hdl/srp/KL_srp_encoder.sv" > "$O/$G.v" 2> "$O/$G.sv2v.err" || exit 1
yosys -q -l "$O/$G.yosys.log" -p "read_verilog $O/$G.v; synth_xilinx -top KL_srp_encoder -flatten -noiopad; ltp -noff; stat" > /dev/null 2>&1
grep -E 'Longest topological path|Number of cells|^ +[0-9]+ cells|LUT6' "$O/$G.yosys.log" | tail -6

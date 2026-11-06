#!/bin/bash
# usage: ltp.sh <tree> <tag>: longest topological path of KL_srp_encoder after synth_xilinx
PKT=${PKT:-$(cd "$(dirname "$0")/.." && pwd)}
t=$1; g=$2; o=$PKT/scratch/ltp; 
sv2v --top=KL_srp_encoder "$t/hdl/common/pp_pkg.sv" "$t/hdl/srp/KL_srp_encoder.sv" > "$o/$g.v" 2> "$o/$g.sv2v.log"
yosys -q -l "$o/$g.yosys.log" -p "read_verilog $o/$g.v; synth_xilinx -family xc7 -flatten -top KL_srp_encoder; ltp -noff; stat" > /dev/null 2>&1
echo $? > "$o/$g.rc"

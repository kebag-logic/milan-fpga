#!/usr/bin/env bash
# usage: synth_wt.sh <label> <N>: the lane's working-tree listener FSM alone
set -eu
label=$1; n=$2
d=$(pwd)/t-$label-$n; rm -rf $d; mkdir -p $d/hdl/srp
cp <lane>/hdl/srp/srp_pkg.sv <lane>/hdl/srp/KL_srp_listener_fsm.sv $d/hdl/srp/
sv2v $d/hdl/srp/srp_pkg.sv $d/hdl/srp/KL_srp_listener_fsm.sv > $d/all.v
yosys -q -p "read_verilog $d/all.v; chparam -set N_SINKS_P $n KL_srp_listener_fsm; synth_xilinx -family xc7 -flatten -top KL_srp_listener_fsm; tee -o $d/stat.txt stat" > $d/yosys.log 2>&1
awk -v w=$label -v n=$n '$2 ~ /^LUT[1-6]$/{l+=$1} $2 ~ /^FD/{f+=$1} END{printf "%s N=%s LUT=%d FF=%d\n", w, n, l, f}' $d/stat.txt

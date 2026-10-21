#!/usr/bin/env bash
# usage: synth_listener_r3.sh <label> <src dir holding hdl/srp> <N_SINKS_P>:
# KL_srp_listener_fsm alone, sv2v then synth_xilinx -family xc7 -flatten (the
# parent's OOC recipe, Yosys 0.66), chparam N_SINKS_P; prints LUT1-6 and FD* sums
set -eu
label=$1; src=$2; n=$3
. <scratch>/r3/scripts/env-parent.sh
d=<scratch>/r3/area/w-$label-$n; rm -rf $d; mkdir -p $d
cp $src/hdl/srp/srp_pkg.sv $src/hdl/srp/KL_srp_listener_fsm.sv $d/
sv2v $d/srp_pkg.sv $d/KL_srp_listener_fsm.sv > $d/all.v
yosys -q -p "read_verilog $d/all.v; chparam -set N_SINKS_P $n KL_srp_listener_fsm; synth_xilinx -family xc7 -flatten -top KL_srp_listener_fsm; tee -o $d/stat.txt stat" > $d/yosys.log 2>&1
awk -v w=$label -v n=$n '$2 ~ /^LUT[1-6]$/{l+=$1} $2 ~ /^FD/{f+=$1} $2 ~ /^RAM/{r+=$1} END{printf "%s N=%s LUT=%d FF=%d RAM=%d\n", w, n, l, f, r}' $d/stat.txt | tee $d/sum.txt

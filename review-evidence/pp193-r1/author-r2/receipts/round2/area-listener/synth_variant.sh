#!/usr/bin/env bash
# usage: synth_variant.sh <label> <patch|-> <N>: the head listener FSM with one
# mutation patch applied (or none), synthesized alone as synth_listener.sh does
set -eu
label=$1; patch=$2; n=$3
d=$(pwd)/v-$label-$n; rm -rf $d; mkdir -p $d
git -C <lane> archive c7c8825f hdl/srp tb/srp_top/mutations | tar -x -C $d
[ "$patch" = "-" ] || (cd $d && git apply tb/srp_top/mutations/$patch.patch)
sv2v $d/hdl/srp/srp_pkg.sv $d/hdl/srp/KL_srp_listener_fsm.sv > $d/all.v
yosys -q -p "read_verilog $d/all.v; chparam -set N_SINKS_P $n KL_srp_listener_fsm; synth_xilinx -family xc7 -flatten -top KL_srp_listener_fsm; tee -o $d/stat.txt stat" > $d/yosys.log 2>&1
awk -v w=$label -v n=$n '/LUT[1-6]/{l+=$2} /FDRE|FDSE/{f+=$2} END{printf "%s N=%s LUT=%d FF=%d\n", w, n, l, f}' $d/stat.txt

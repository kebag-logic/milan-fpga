#!/usr/bin/env bash
# usage: synth_listener.sh <rev> <N_SINKS_P>: KL_srp_listener_fsm alone, the
# lane's revision, sv2v then synth_xilinx -family xc7 -flatten (the parent's
# OOC recipe), stat
set -eu
rev=$1; n=$2
d=$(pwd)/w-$rev-$n; rm -rf $d; mkdir -p $d
git -C <lane> archive $rev hdl/srp | tar -x -C $d
sv2v $d/hdl/srp/srp_pkg.sv $d/hdl/srp/KL_srp_listener_fsm.sv > $d/all.v
yosys -q -p "read_verilog $d/all.v; chparam -set N_SINKS_P $n KL_srp_listener_fsm; synth_xilinx -family xc7 -flatten -top KL_srp_listener_fsm; tee -o $d/stat.txt stat" > $d/yosys.log 2>&1
grep -E "LUT[1-6]|FDRE|FDSE|FDCE|RAM|MUXF|CARRY|Number of cells" $d/stat.txt | sed "s/^/$rev N=$n /"

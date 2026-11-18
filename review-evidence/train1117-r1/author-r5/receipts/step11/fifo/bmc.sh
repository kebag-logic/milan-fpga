#!/bin/bash
# bmc.sh: cdc_pair_fifo's default branch at p11 against the candidate's module, Yosys, each parameter set a
# default-branch instance takes: both clocks free (clk2fflogic: any interleaving of write and read edges), both designs
# from the zero state (the storage has no reset), every output equal at every one of 40 steps (sat -seq 40).
O=<scratch>/r5fifo; rc=0
for pw in "48 3" "52 3" "48 4" "192 2"; do set -- $pw; tag=w$1l$2
cat > $O/bmc-$tag.ys <<YS
read_verilog -sv $O/gold.sv
read_verilog -sv $O/gate.sv
chparam -set WIDTH $1 -set LOG2D $2 gold_fifo
chparam -set WIDTH $1 -set LOG2D $2 gate_fifo
proc; opt_clean; memory -nomap; memory_map; opt -full
miter -equiv -flatten -make_assert -ignore_gold_x gold_fifo gate_fifo miter
hierarchy -top miter
clk2fflogic
opt_clean
sat -verify -prove-asserts -set-init-zero -seq 40 -timeout 3000 miter
YS
yosys -q -l $O/bmc-$tag.log -s $O/bmc-$tag.ys > /dev/null 2>&1; r=$?; [ $r = 0 ] || rc=1
echo "$tag: rc=$r $(grep -E 'SUCCESS|FAIL|timeout|Timeout' $O/bmc-$tag.log | tail -1 | cut -c1-160) $(date +%T)"
done; exit $rc

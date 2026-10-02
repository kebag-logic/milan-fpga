#!/bin/bash
# Scratch: the parent's heavy consumer gates in sequence, one log and rc file each.
cd $VALIDATION_STORAGE/c8-a501/parent-dev || exit 2
G=$VALIDATION_STORAGE/c8-a501/gates-dev
run() { name=$1; shift; "$@" > "$G/$name.log" 2>&1; echo $? > "$G/$name.rc"; echo "$name rc=$(cat $G/$name.rc) $(date +%T)"; }
run pp_shadow make -C tb/verilator/pp_shadow -j16
run nvm_cosim_lint make -C tb/verilator/nvm_cosim lint
run nvm_cosim_quick make -C tb/verilator/nvm_cosim quick
run milan_dp make -C tb/verilator/milan_dp -j16
run milan_dp_render make -C tb/verilator/milan_dp_render -j16

#!/bin/sh
# usage: run_mutants.sh <tree> <logdir>   runs the leg's own mutant campaign with the pinned simulator
cd "$1/tb/verilator/milan_dp" || exit 90
start=$(date +%s)
make bootsa-mutants VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator VERILATOR_JOBS=4 > "$2/bootsa_mutants_head.log" 2>&1
echo "$? $(( $(date +%s) - start ))s" > "$2/bootsa_mutants_head.rc"

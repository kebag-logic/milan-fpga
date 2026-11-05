#!/bin/sh
# usage: run_leg.sh <tree> <logdir> <name>   builds and runs the bootsa leg in <tree> with the pinned simulator
tree=$1; logs=$2; name=$3
cd "$tree/tb/verilator/milan_dp" || exit 90
start=$(date +%s)
make bootsa VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator VERILATOR_JOBS=3 > "$logs/$name.log" 2>&1
rc=$?
echo "$rc $(( $(date +%s) - start ))s" > "$logs/$name.rc"

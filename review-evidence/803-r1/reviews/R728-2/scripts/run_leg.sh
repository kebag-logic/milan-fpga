#!/bin/sh
# Build and run one milan_dp sim_gptp leg in a disposable tree.
# usage: run_leg.sh <tree> <gptp|gptp-lat> <log> <rcfile> [verilator] [jobs]
# verilator defaults to $VERILATOR, then to `verilator` on PATH.
tree=$1; leg=$2; log=$3; rc=$4
vl=${5:-${VERILATOR:-verilator}}; jobs=${6:-3}
cd "$tree/tb/verilator/milan_dp" || exit 2
make VERILATOR="$vl" VERILATOR_JOBS="$jobs" "$leg" > "$log" 2>&1
echo $? > "$rc"

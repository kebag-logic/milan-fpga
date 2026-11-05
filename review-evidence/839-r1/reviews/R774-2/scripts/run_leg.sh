#!/usr/bin/env bash
# usage: run_leg.sh <tree (clone copy with .git)> <logfile>  - build and run the bootsa leg with the pinned Verilator
T=$1; L=$2; V=${VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
cd "$T/tb/verilator/milan_dp" || exit 90
s=$(date +%s); make bootsa VERILATOR="$V" VERILATOR_JOBS=4 > "$L" 2>&1; rc=$?
echo "$rc $(( $(date +%s) - s ))s" > "${L%.log}.rc"

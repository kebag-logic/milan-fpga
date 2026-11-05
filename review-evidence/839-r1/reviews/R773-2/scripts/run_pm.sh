#!/bin/sh
# Build and run the leg against one reviewer mutant: run_pm.sh <tree> <objdir> <mutant.sv> <name> <receipts>
T=$1; MD=$2; DP=$3; N=$4; R=$5; export VERILATOR=${VERILATOR:-verilator} VERILATOR_JOBS=${VERILATOR_JOBS:-3}
cd "$T/tb/verilator/milan_dp"
make -s BOOTSA_MDIR="$MD" DP_SRC="$DP" bootsa-build > "$R/build-$N.log" 2>&1; b=$?
if [ $b -ne 0 ]; then echo "build $b" > "$R/run-$N.rc"; exit; fi
"$MD/Vmilan_dp_bootsa" > "$R/run-$N.log" 2>&1; echo $? > "$R/run-$N.rc"

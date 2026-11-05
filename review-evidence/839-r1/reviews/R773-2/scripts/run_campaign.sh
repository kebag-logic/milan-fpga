#!/bin/sh
# Clean bootsa leg, then the author's bootsa-mutants driver, in tree $1; receipts to $2.
T=$1; R=$2; export VERILATOR=${VERILATOR:-verilator} VERILATOR_JOBS=${VERILATOR_JOBS:-4}
cd "$T/tb/verilator/milan_dp"
( time make -s bootsa ) > "$R/bootsa-head.log" 2>&1; echo $? > "$R/bootsa-head.rc"
( time python3 bootsa_mutants.py ) > "$R/bootsa-mutants.log" 2>&1; echo $? > "$R/bootsa-mutants.rc"

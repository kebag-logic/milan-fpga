#!/bin/bash
# One traced group run from a leg's build: committed PCs and fetch refills from AFTER for PCS PCs (sim_main.cpp's
# BUDGET_TRACE_AFTER and BUDGET_TRACE_PCS), the CPU at 100 MHz.
# usage: trace.sh CHECKOUT LEG POINT GROUP AFTER PCS [run.py args...]
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683k/scripts/env.sh
C=$1 LEG=$2 POINT=$3 G=$4 AFTER=$5 PCS=$6; shift 6
B=$VALIDATION_STORAGE/665s2b-a683k/builds/$LEG
O=$VALIDATION_STORAGE/665s2b-a683k/traces/$LEG-$G
mkdir -p "$O"
start=$(date +%s)
CSB_CPU_HZ=100000000 BUDGET_TRACE_AFTER=$AFTER BUDGET_TRACE_PCS=$PCS python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" \
  --point "$POINT" --build-dir "$B" --reuse-build --groups "$G" --out "$O" --jobs 1 "$@" > "$O/driver.log" 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s rc=$rc" >> "$O/driver.log"

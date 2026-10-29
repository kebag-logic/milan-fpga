#!/bin/sh
# usage: run_leg.sh <tree> <target> <log> <rcfile>
# Builds and/or runs one milan_dp gPTP leg (gptp, gptp-lat, build-gptp,
# exec-gptp, ...) in <tree>. Set VERILATOR to the pinned Verilator 5.050
# entry point; JOBS sets VERILATOR_JOBS (default 2).
T="$1"; TGT="$2"; LOG="$3"; RC="$4"
V=${VERILATOR:-verilator}
cd "$T/tb/verilator/milan_dp" || { echo 99 > "$RC"; exit 99; }
make VERILATOR="$V" VERILATOR_JOBS=${JOBS:-2} "$TGT" > "$LOG" 2>&1
echo $? > "$RC"

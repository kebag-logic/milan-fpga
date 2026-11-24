#!/usr/bin/env bash
# milan_dp gPTP legs at the head: the writable key's leg, then the default
# (constant-pair) leg the AX7101 ships. usage: milan_dp_runs.sh <head-tree> <receipts> <verilator>
set -u
H=$1 R=$2 V=$3
cd "$H/tb/verilator/milan_dp"
make VERILATOR="$V" VERILATOR_JOBS=8 gptp-latw > "$R/milan-dp-gptp-latw.log" 2>&1; echo $? > "$R/milan-dp-gptp-latw.rc"
make VERILATOR="$V" VERILATOR_JOBS=8 gptp-lat > "$R/milan-dp-gptp-lat.log" 2>&1; echo $? > "$R/milan-dp-gptp-lat.rc"

#!/usr/bin/env bash
# Build and run the milan_dp CRF talker licence leg (it parses the DUT's
# MSRP MRPDUs: LeaveAll flags and Talker Advertise TSpecs) at the clone's head.
# usage: run_crflic.sh <clone-at-head> <out-dir> <jobs>
set -u
C=$1; OUT=$2; J=$3
VERILATOR=${VERILATOR:?set VERILATOR}
mkdir -p "$OUT"
git -C "$C" rev-parse HEAD > "$OUT/crflic.head"
git -C "$C" submodule status > "$OUT/crflic.submodules"
make -C "$C/tb/verilator/milan_dp" crflic VERILATOR="$VERILATOR" VERILATOR_JOBS="$J" > "$OUT/crflic.log" 2>&1
echo $? > "$OUT/crflic.rc"
